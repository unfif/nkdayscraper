# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from .models import HorseResult, Jrarecord, Race, Payback, engine, mongo_connect
from .items import HorseResultItem, PaybackItem, RaceItem#, JrarecordItem
import copy as cp

from time import perf_counter

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.has_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.nkday
        self.collection = self.mongodb.horseresults

        try: self.collection.drop()
        except: self.has_mongoerr = True

    def open_spider(self, spider):
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
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.has_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.nkday
        self.collection = self.mongodb.jrarecords

        try: self.collection.drop()
        except: self.has_mongoerr = True

    def open_spider(self, spider):
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
