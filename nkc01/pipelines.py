# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from nkc01.models import nkthedayraces, db_connect, create_table
import pandas as pd

class Nkc01Pipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker. Creates deals table."""
        engine = db_connect(False)
        # drop_table(engine, nkthedayraces)
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        session = self.Session()
        session.query(nkthedayraces).delete()
        session.commit()
        model = nkthedayraces()
        # print(model.getCommentList())

    # def open_spider(self, spider: scrapy.Spider):# コネクションの開始
    #     URI = nkc01.settings.get('URI')
    #     self.conn = psycopg2.connect(URI)
    #
    # def close_spider(self, spider: scrapy.Spider):# コネクションの終了
    #     self.conn.close()

    def process_item(self, item, spider):
        """Save deals in the database. This method is called for every item pipeline component."""
        session = self.Session()
        nkdbraces = nkthedayraces(**item)

        try:
            session.add(nkdbraces)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
