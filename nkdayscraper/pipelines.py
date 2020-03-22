# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Nkdayraces, db_connect, create_table, mongo_connect
import datetime as dt
import copy as cp

class NkdayscraperPipeline():
    cnt = 0
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.engine = db_connect(echo=False)
        if self.engine.has_table('nkdayraces'): Nkdayraces.__table__.drop(self.engine)
        create_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        self.is_mongoerr = False
        self.mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = self.mongo.netkeiba
        self.collection = self.mongodb.nkdayraces

        try: self.collection.drop()
        except: self.is_mongoerr = True

    def open_spider(self, spider):
        # DATABASE_URL = nkdayscraper.settings.get('DATABASE_URL')
        # self.conn = psycopg2.connect(DATABASE_URL)
        pass

    def close_spider(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        session = self.Session()
        if self.engine.name not in ['postgresql', 'mongodb']:
            item['addedmoneylist'] = str(item['addedmoneylist'])
            item['passageratelist'] = str(item['passageratelist'])
        nkdbraces = Nkdayraces(**item)
        try:
            session.add(nkdbraces)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        if not self.is_mongoerr:
            mongoitem = cp.deepcopy(item)
            mongoitem['posttime'] = str(mongoitem['posttime'])
            mongoitem['time'] = str(mongoitem['time'])
            self.collection.insert_one(dict(mongoitem))

        return item
