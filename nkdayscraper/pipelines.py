# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Nkdayraces, db_connect, create_table, mongo_connect

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        self.engine = db_connect()
        if self.engine.has_table('nkdayraces'): Nkdayraces.__table__.drop(self.engine)
        create_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        mongo = mongo_connect()
        mongodb = mongo.netkeiba
        clct = mongodb.nkdayraces
        clct.drop()

    # def open_spider(self, spider: scrapy.Spider):# コネクションの開始
    #     DATABASE_URL = nkdayscraper.settings.get('DATABASE_URL')
    #     self.conn = psycopg2.connect(DATABASE_URL)
    #
    # def close_spider(self, spider: scrapy.Spider):# コネクションの終了
    #     self.conn.close()

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        session = self.Session()
        if self.engine.name != 'postgresql':
            item['raceaddedmoney'] = str(item['raceaddedmoney'])
            item['position'] = str(item['position'])

        nkdbraces = Nkdayraces(**item)

        try:
            session.add(nkdbraces)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
