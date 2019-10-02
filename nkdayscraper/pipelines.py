# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Nkdayraces, db_connect, create_table, mongo_connect
import datetime as dt

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.engine = db_connect()
        if self.engine.has_table('nkdayraces'): Nkdayraces.__table__.drop(self.engine)
        create_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        self.mongoerr = False
        mongo = mongo_connect(query={'serverSelectionTimeoutMS': 3000})
        self.mongodb = mongo.netkeiba
        self.collection = self.mongodb.nkdayraces

        try: self.collection.drop()
        except: self.mongoerr = True

    # def open_spider(self, spider: scrapy.Spider):# コネクションの開始
    #     DATABASE_URL = nkdayscraper.settings.get('DATABASE_URL')
    #     self.conn = psycopg2.connect(DATABASE_URL)
    #
    # def close_spider(self, spider: scrapy.Spider):# コネクションの終了
    #     self.conn.close()

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        session = self.Session()
        if self.engine.name not in ['postgresql', 'mongodb']:
            item['addedmoneylist'] = str(item['addedmoneylist'])
            item['positionlist'] = str(item['positionlist'])

        nkdbraces = Nkdayraces(**item)

        try:
            session.add(nkdbraces)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        if not self.mongoerr:
            posttimeorig = item['posttime']
            timeorig = item['time']
            item['posttime'] = str(item['posttime'])
            item['time'] = str(item['time'])
            self.collection.insert_one(dict(item))
            item['posttime'] = posttimeorig
            item['time'] = timeorig


        return item
