# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import engine, mongo_connect
from nkdayscraper.items import HorseResultItem, RaceItem
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import copy as cp
import datetime as dt
from time import perf_counter

jst = dt.timezone(dt.timedelta(hours=9))

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.schema = 'nkday'
        self.tables = ['races', 'paybacks', 'horseresults']
        # self.indices = [f'{self.schema}.{table}' for table in self.tables]
        self.records = []
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.mongo = Mongo(
            conn=mongo_connect(query={'serverSelectionTimeoutMS': 3000}),
            db=self.schema,
            has_error=False
        )
        self.es = Elasticsearch(http_compress = True)

        for table in self.tables:
            try: getattr(self.mongo.db, table).drop()
            except: self.mongo.has_error = True
            index = f'{self.schema}.{table}'
            if self.es.indices.exists(index=index): self.es.indices.delete(index=index)

    def open_spider(self, spider):
        self.open_time = perf_counter()

    def close_spider(self, spider):
        self.mongo.conn.close()
        bulk(self.es, makeEsRecords(self.records))
        for table in self.tables:
            index = f'{self.schema}.{table}'
            self.es.indices.put_settings(index=index, body={"number_of_replicas": 0})

        self.es.close()
        print(f'【spider_time: {str(perf_counter() - self.open_time)}】')

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        if self.engine.name not in ['postgresql', 'mongodb']:
            for columnName in ['addedmoneylist', 'passageratelist']:
                item[columnName] = str(item[columnName])

        record = item.model(**item)

        with self.Session() as session:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise

        table = item.model.__table__.name
        copyItem = cp.deepcopy(item)
        if isinstance(copyItem, RaceItem): copyItem['posttime'] = str(copyItem['posttime'])
        if isinstance(copyItem, HorseResultItem): copyItem['time'] = str(copyItem['time'])

        if not self.mongo.has_error:
            getattr(self.mongo.db, table).insert_one(makeMongoRecord(dict(copyItem)))

        esRecord = dict(copyItem)
        esRecord['_index'] = f'{self.schema}.{table}'
        if esRecord['_index'] is not None: self.records.append(esRecord)

        return item

class JrarecordsscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.schema = 'nkday'
        self.tables = ['jrarecords']
        # self.indices = [f'{self.schema}.{table}' for table in self.tables]
        self.records = []
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.mongo = Mongo(
            conn=mongo_connect(query={'serverSelectionTimeoutMS': 3000}),
            db=self.schema,
            has_error=False
        )
        self.es = Elasticsearch(http_compress = True)

        for table in self.tables:
            try: getattr(self.mongo.db, table).drop()
            except: self.mongo.has_error = True
            index = f'{self.schema}.{table}'
            if self.es.indices.exists(index=index): self.es.indices.delete(index=index)

    def open_spider(self, spider):
        self.open_time = perf_counter()

    def close_spider(self, spider):
        self.mongo.conn.close()
        bulk(self.es, makeEsRecords(self.records))
        for table in self.tables:
            index = f'{self.schema}.{table}'
            self.es.indices.put_settings(index=index, body={"number_of_replicas": 0})

        self.es.close()
        print(f'【spider_time: {str(perf_counter() - self.open_time)}】')

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        record = item.model(**item)

        with self.Session() as session:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise

        table = item.model.__table__.name
        copyItem = cp.deepcopy(item)
        if not self.mongo.has_error:
            getattr(self.mongo.db, table).insert_one(makeMongoRecord(dict(copyItem)))

        esRecord = dict(copyItem)
        esRecord['_index'] = f'{self.schema}.{table}'
        if esRecord['_index'] is not None: self.records.append(esRecord)

        return item

def makeEsRecords(records):
    for record in records:
        yield record

def makeMongoRecord(item):
    for key in item.keys():
        if type(item[key]) == dt.date:
            item[key] = dt.datetime.combine(item[key], dt.time()).astimezone(jst)

    return item

class Mongo():
    def __init__(self, conn, db, has_error):
        self.conn = conn
        self.db = getattr(self.conn, db)
        self.has_error = has_error
