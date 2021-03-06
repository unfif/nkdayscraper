# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import engine, mongo_connect
from nkdayscraper.items import RaceItem, PaybackItem, HorseResultItem
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import copy as cp
import datetime as dt
from time import perf_counter
from functools import singledispatch

jst = dt.timezone(dt.timedelta(hours=9))

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.schema = 'nkday'
        self.tables = ['races', 'paybacks', 'horseresults']
        self.records = []
        self.nkdayDict = {}
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)
        self.es = Elasticsearch(http_compress = True)

        if self.es.indices.exists(index=f'{self.schema}.{self.schema}'): self.es.indices.delete(index=f'{self.schema}.{self.schema}')

        self.mongo = Mongo(
            conn=mongo_connect(query={'serverSelectionTimeoutMS': 3000}),
            db=self.schema,
            has_error=False
        )

        for table in self.tables:
            try: getattr(self.mongo.db, table).drop()
            except: self.mongo.has_error = True
            index = f'{self.schema}.{table}'
            if self.es.indices.exists(index=index): self.es.indices.delete(index=index)

    def open_spider(self, spider):
        self.open_time = perf_counter()

    def close_spider(self, spider):
        self.mongo.conn.close()
        bulk(self.es, makeEsRecords(self.nkdayDict))
        self.es.indices.put_settings(index=f'{self.schema}.{self.schema}', body={"number_of_replicas": 0})

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
        if isinstance(item, RaceItem) and copyItem['posttime'] is not None: copyItem['posttime'] = copyItem['posttime'].isoformat()
        if isinstance(item, HorseResultItem) and copyItem['time'] is not None: copyItem['time'] = copyItem['time'].isoformat()

        if not self.mongo.has_error:
            getattr(self.mongo.db, table).insert_one(makeMongoRecord(dict(copyItem)))

        esRecord = dict(copyItem)
        for target in ['date', 'datetime']:
            if target in esRecord and esRecord[target] is not None: esRecord[target] = esRecord[target].isoformat()

        raceid = esRecord['raceid']
        if isinstance(item, (RaceItem, PaybackItem)):
            esRecord['_index'] = f'{self.schema}.{self.schema}'
            if not raceid in self.nkdayDict: self.nkdayDict[raceid] = {}
            self.nkdayDict[raceid].update(esRecord)

        elif isinstance(item, (HorseResultItem)):
            if not raceid in self.nkdayDict:
                self.nkdayDict[raceid] = {'_index': f'{self.schema}.{self.schema}', 'results': []}
            else:
                if not 'results' in self.nkdayDict[raceid]: self.nkdayDict[raceid]['results'] = []

            self.nkdayDict[raceid]['results'].append(esRecord)

        return item

class JrarecordsscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.schema = 'nkday'
        self.tables = ['jrarecords']
        self.records = []
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)
        self.es = Elasticsearch(http_compress = True)

        self.mongo = Mongo(
            conn=mongo_connect(query={'serverSelectionTimeoutMS': 3000}),
            db=self.schema,
            has_error=False
        )

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
        if copyItem['time'] is not None: copyItem['time'] = copyItem['time'].isoformat()
        if not self.mongo.has_error:
            getattr(self.mongo.db, table).insert_one(makeMongoRecord(dict(copyItem)))

        esRecord = dict(copyItem)
        esRecord['_index'] = f'{self.schema}.{table}'
        if esRecord['_index'] is not None: self.records.append(esRecord)

        return item

@singledispatch
def makeEsRecords():
    yield None

@makeEsRecords.register(list)
def _(records):
    for record in records:
        yield record

@makeEsRecords.register(dict)
def _(records):
    for key in records:
        yield records[key]

def makeMongoRecord(item):
    for key in item:
        if type(item[key]) == dt.date:
            item[key] = dt.datetime.combine(item[key], dt.time()).astimezone(jst)

    return item

class Mongo():
    def __init__(self, conn, db, has_error):
        self.conn = conn
        self.db = getattr(self.conn, db)
        self.has_error = has_error
