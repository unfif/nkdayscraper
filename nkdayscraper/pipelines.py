# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Nkdayraces, db_connect, create_table

class NkdayscraperPipeline():
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        engine = db_connect(False)
        if engine.has_table('nkdayraces'): Nkdayraces.__table__.drop(engine)
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        session = self.Session()
        # session.query(Nkdayraces).delete()
        session.commit()
        model = Nkdayraces()

    # def open_spider(self, spider: scrapy.Spider):# コネクションの開始
    #     DATABASE_URL = nkdayscraper.settings.get('DATABASE_URL')
    #     self.conn = psycopg2.connect(DATABASE_URL)
    #
    # def close_spider(self, spider: scrapy.Spider):# コネクションの終了
    #     self.conn.close()

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        session = self.Session()
        nkdbraces = Nkdayraces(**item)

        try:
            session.add(nkdbraces)
            session.commit()
            pass
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
