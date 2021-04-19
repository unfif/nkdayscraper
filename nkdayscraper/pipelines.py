# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from .models import HorseResult, Jrarecord, Race, Payback, engine, create_tables, drop_tables, drop_race_tables, mongo_connect
from .items import HorseResultItem, PaybackItem, RaceItem#, JrarecordItem
import copy as cp

from time import perf_counter

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.engine = engine
        # if self.engine.has_table('horseresults'): HorseResult.__table__.drop(self.engine)
        # drop_race_tables(self.engine)
        # create_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)
        # session = self.Session()
        # try:
        #     session.query(Payback).delete()
        #     session.query(HorseResult).delete()
        #     session.query(Race).delete()
        #     # session.query(Jrarecord).delete()
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        self.has_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.nkday
        self.collection = self.mongodb.horseresults

        try: self.collection.drop()
        except: self.has_mongoerr = True

    def open_spider(self, spider):
        # DATABASE_URL = nkdayscraper.settings.get('DATABASE_URL')
        # self.conn = psycopg2.connect(DATABASE_URL)
        pass
        self.time_start = perf_counter()

    def close_spider(self, spider):
        self.mongo.close()
        print('【spider_time: ' + str(perf_counter() - self.time_start) + '】')

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
        # elif isinstance(item, JrarecordItem): record = Jrarecord(**item)

        with self.Session() as session:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise

        if not self.has_mongoerr:
            mongoitem = cp.deepcopy(item)
            if isinstance(mongoitem, RaceItem): mongoitem['posttime'] = str(mongoitem['posttime'])
            if isinstance(mongoitem, HorseResultItem): mongoitem['time'] = str(mongoitem['time'])
            self.collection.insert_one(dict(mongoitem))

        return item

class JrarecordsscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.engine = engine
        # if self.engine.has_table('jrarecords'): Jrarecord.__table__.drop(self.engine)
        # Jrarecord.__table__.create(self.engine)
        # drop_tables(self.engine)
        # create_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)
        # with self.Session() as session:
        #     session.query(Jrarecord.__table__).delete()

        # session = self.Session()
        # try:
        #     session.query(Jrarecord).delete()
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        self.has_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.nkday
        self.collection = self.mongodb.jrarecords

        try: self.collection.drop()
        except: self.has_mongoerr = True

    def open_spider(self, spider):
        # DATABASE_URL = nkdayscraper.settings.get('DATABASE_URL')
        # self.conn = psycopg2.connect(DATABASE_URL)
        pass

    def close_spider(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        if self.engine.name not in ['postgresql', 'mongodb']:
            # item['addedmoneylist'] = str(item['addedmoneylist'])
            # item['passageratelist'] = str(item['passageratelist'])
            pass

        record = Jrarecord(**item)
        with self.Session() as session:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise

        if not self.has_mongoerr:
            mongoitem = cp.deepcopy(item)
            # mongoitem['posttime'] = str(mongoitem['posttime'])
            # mongoitem['time'] = str(mongoitem['time'])
            self.collection.insert_one(dict(mongoitem))

        return item
