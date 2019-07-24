from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import re

db = SQLAlchemy()
engine = db.create_engine("postgresql+psycopg2://postgres:marehito@localhost:5432/postgres", {})
meta = db.MetaData()
meta.reflect(bind=engine)
table = meta.tables['nkthedayraces']
cols = table.c

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:marehito@localhost:5432/postgres"#?charset=utf8"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

class ToDoItem(db.Model):
    __tablename__ = "todoitems"
    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default=False)
    done = db.Column(db.Boolean, nullable=False)

class NkTheDayRaces():
    def getRaces():
        data = {}
        con = engine.connect()
        # sql = table.select().where(cols.raceid.like('20190302____')).order_by(cols.racenum, cols.placenum)
        sql = table.select().order_by(cols.place, cols.racenum, cols.placenum)
        racesdf = pd.read_sql(sql, con)
        racesdf.title = racesdf.title.apply(lambda x: x.rstrip('クラス'))
        racesdf.posttime = racesdf.posttime.apply(lambda x: x.strftime('%H:%M'))
        racesdf.time = racesdf.time.apply(lambda x: x.strftime('%M:%S %f').strip('0'))

        # racesdf = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
        racesdf = racesdf.sort_values(['place', 'racenum', 'placenum']).reset_index(drop=True)
        racesdf['racerank'] = racesdf[['place', 'racenum', 'placenum']].groupby(['place', 'racenum']).rank()
        racesdf['nextracerank'] = racesdf.loc[1:, 'racerank'].reset_index(drop=True)
        racesdf.loc[racesdf['racerank'] < 4.0, 'rankinfo'] = 'initdisp'
        racesdf.loc[(racesdf['racerank'] < 4.0) & (racesdf['nextracerank'] >= 4.0), 'rankinfo'] = 'initend'
        racesdf.loc[racesdf['racerank'] >= 4.0, 'rankinfo'] = 'initnone'
        racesdf.loc[racesdf['nextracerank'] - racesdf['racerank'] < 0, 'rankinfo'] = 'raceend'

        sql = "SELECT psat.relname as TABLE_NAME, pa.attname as COLUMN_NAME, pd.description as COLUMN_COMMENT "
        sql += "FROM pg_stat_all_tables psat, pg_description pd, pg_attribute pa "
        sql += "WHERE psat.schemaname = (select schemaname from pg_stat_user_tables where relname = 'nkthedayraces') "
        sql += "and psat.relname = 'nkthedayraces' and psat.relid=pd.objoid "
        sql += "and pd.objsubid != 0 and pd.objoid=pa.attrelid and pd.objsubid=pa.attnum "
        sql += "ORDER BY pd.objsubid"

        colnames = {}
        comments = pd.read_sql(sql, con)
        con.close()

        jockeyct = pd.crosstab([racesdf.place, racesdf.jockey], racesdf.placenum, margins=True)
        rates = [round(100 * jockeyct[rank] / jockeyct.All, 2) for rank in range(1, 4)]
        jockeyct['単勝率'], jockeyct['連対率'], jockeyct['複勝率'] = rates
        jockeyct = jockeyct.loc[:, [1,2,3, '単勝率', '連対率', '複勝率', 'All']].sort_values(['place',1,2,3], ascending=False)
        # intsrs = [jockeyct[sr].astype('int8') for sr in [1,2,3,'All']]
        # jockeyct[1], jockeyct[2], jockeyct[3], jockeyct['All'] = intsrs
        data['jockeys'] = jockeyct.rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})
        # print(jockeyct[1])
        # print(data['jockeys'].loc[('福島')])


        for comment in comments.loc[:, 'column_name':'column_comment'].iterrows():
            colnames.update({comment[1].column_name: comment[1].column_comment})

        # racesdf = racesdf.sort_values(['place', 'racenum', 'placenum']).dataet_index(drop=True)
        data['racesdf'] = racesdf.rename(columns = colnames)
        # print(racesdf.iloc[[0]])
        # for place in racesdf.場所.unique(): print(place)
        # print(racesdf.場所)

        return data

class ToDoList:
  def add(self, title):
    item = ToDoItem(title=title, done=False)
    db.session.add(item)
    db.session.commit()

  def delete(self, item_id):
    item = ToDoItem.query.filter_by(item_id=item_id).first()
    db.session.delete(item)
    db.session.commit()

  def get_all(self):
    items = ToDoItem.query.all()
    return items

  def delete_doneitem(self):
    ToDoItem.query.filter_by(done=True).delete()
    db.session.commit()

  def update_done(self, items):
    for item in self.get_all():
      if item.item_id in items:
        item.done = True
      else:
        item.done = False
    db.session.commit()
