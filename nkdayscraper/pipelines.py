# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from .models import HorseResult, Jrarecord, Race, Payback, engine, mongo_connect
from .items import HorseResultItem, PaybackItem, RaceItem#, JrarecordItem
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import copy as cp
import datetime as dt
import re
from time import perf_counter

jst = dt.timezone(dt.timedelta(hours=9))

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.table = HorseResult.__table__.name
        self.indices = ['nkday.races', 'nkday.paybacks', 'nkday.horseresults']
        self.records = []
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.has_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.nkday
        self.collection = getattr(self.mongodb, self.table)

        try: self.collection.drop()
        except: self.has_mongoerr = True

        self.es = Elasticsearch(http_compress = True)
        for index in self.indices:
            if self.es.indices.exists(index=index): self.es.indices.delete(index=index)

    def open_spider(self, spider):
        self.open_time = perf_counter()

    def close_spider(self, spider):
        self.mongo.close()
        bulk(self.es, makeEsRecords(self.records))
        for index in self.indices:
            self.es.indices.put_settings(index=index, body={"number_of_replicas": 0})

        self.es.close()
        print(f'【spider_time: {str(perf_counter() - self.open_time)}】')

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        if self.engine.name not in ['postgresql', 'mongodb']:
            for columnName in ['addedmoneylist', 'passageratelist']:
                item[columnName] = str(item[columnName])

        if isinstance(item, RaceItem):
            record = Race(**item)
        elif isinstance(item, PaybackItem):
            record = Payback(**item)
        elif isinstance(item, HorseResultItem):
            record = HorseResult(**item)

        with self.Session() as session:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise

        copyItem = cp.deepcopy(item)
        if not self.has_mongoerr:
            if isinstance(copyItem, RaceItem): copyItem['posttime'] = str(copyItem['posttime'])
            if isinstance(copyItem, HorseResultItem): copyItem['time'] = str(copyItem['time'])
            self.collection.insert_one(dict(copyItem))

        esRecord = dict(copyItem)
        esRecord['_index'] = f'nkday.{getEsIndexName(copyItem)}'
        if esRecord['_index'] is not None: self.records.append(esRecord)

        return item

class JrarecordsscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.table = Jrarecord.__table__.name
        self.indices = ['nkday.jrarecords']
        self.records = []
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.has_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.nkday
        self.collection = getattr(self.mongodb, self.table)

        try: self.collection.drop()
        except: self.has_mongoerr = True

        self.es = Elasticsearch(http_compress = True)
        for index in self.indices:
            if self.es.indices.exists(index=index): self.es.indices.delete(index=index)

    def open_spider(self, spider):
        self.open_time = perf_counter()

    def close_spider(self, spider):
        self.mongo.close()
        bulk(self.es, makeEsRecords(self.records))
        for index in self.indices:
            self.es.indices.put_settings(index=index, body={"number_of_replicas": 0})

        self.es.close()
        print(f'【spider_time: {str(perf_counter() - self.open_time)}】')

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        record = Jrarecord(**item)

        with self.Session() as session:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise

        copyItem = cp.deepcopy(item)
        if not self.has_mongoerr:
            self.collection.insert_one(makeMongoRecord(dict(copyItem)))

        esRecord = dict(copyItem)
        esRecord['_index'] = f'nkday.{getEsIndexName(copyItem)}'
        if esRecord['_index'] is not None: self.records.append(esRecord)

        return item

def getEsIndexName(instance):
    match = re.match(r"^<class 'nkdayscraper.items.(.+)Item'>$", str(instance.__class__))
    return f'{match.groups()[0].lower()}s' if match else None


def makeEsRecords(records):
    for record in records:
        yield record

def makeMongoRecord(item):
    for key in item.keys():
        if type(item[key]) == dt.date:
            item[key] = dt.datetime.combine(item[key], dt.time()).astimezone(jst)

    return item
