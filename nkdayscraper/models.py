# %%
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, Text, Date, DateTime, Time, Boolean, ForeignKeyConstraint#, ForeignKey, UniqueConstraint, outerjoin, and_, LargeBinary, SmallInteger
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import copy as cp

# from sqlalchemy.sql import Select

DATABASE_URL = get_project_settings().get('DATABASE_URL')
# SQLITE_URL = get_project_settings().get('SQLITE_URL')
MONGO_URL = get_project_settings().get('MONGO_URL')
engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)
meta = MetaData()
meta.reflect(bind=engine)
# hrs = meta.tables['horseresults'].alias('hrs')
# jrr = meta.tables['jrarecords'].alias('jrr')
# hrs = Table('horseresults', meta, autoload=True)
# jrr = Table('jrarecords', meta, autoload=True)
# sql = outerjoin(hrs, jrr).select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
# sql = hrs.select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
# sql = outerjoin(hrs, jrr, and_(jrr.c.place == hrs.c.place, jrr.c.distance == hrs.c.distance, jrr.c.coursetype == hrs.c.coursetype, jrr.c.courseinfo1 == hrs.c.courseinfo1, jrr.c.courseinfo2 == hrs.c.courseinfo2)).select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
# sql = Select([hrs, jrr]).outerjoin(jrr, and_(jrr.c.place == hrs.c.place, jrr.c.distance == hrs.c.distance, jrr.c.coursetype == hrs.c.coursetype, jrr.c.courseinfo1 == hrs.c.courseinfo1, jrr.c.courseinfo2 == hrs.c.courseinfo2))#.order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
# con = engine.connect()
# racesdf = pd.read_sql(sql, con)
# print(sql, racesdf.columns, '\n', racesdf.time.iloc[:,0], type(racesdf.time.iloc[:,0]))

# %%
class RBase():
    def __repr__(self):
        columns = ', '.join([
            f'{key}={repr(self.__dict__[key])}'
            for key in self.__dict__.keys() if not key.startswith('_')
        ])
        return f'<{self.__class__.__name__}({columns})>'

Base = declarative_base(cls=RBase)

def mongo_connect(url=MONGO_URL, query=None):
    if url is None: url = 'mongodb://localhost:27017'
    if type(query) is dict:
        if not url.endswith('/'): url += '/'
        url += '?'
        for key, val in query.items():
            url += key + '=' + str(val)

    client = MongoClient(url)
    return client

def create_tables(engine):
    Base.metadata.create_all(engine)

class Race(Base):
    __tablename__ = 'races'
    __table_args__ = (ForeignKeyConstraint(
        ['place', 'coursetype', 'generation', 'distance', 'courseinfo1', 'courseinfo2'],
        ['jrarecords.place', 'jrarecords.coursetype', 'jrarecords.generation', 'jrarecords.distance', 'jrarecords.courseinfo1', 'jrarecords.courseinfo2']),
        {}
    )
    raceid = Column(Text, primary_key=True, comment='レースID')
    year = Column(Integer, comment='年')
    place = Column(Text, comment='場所')
    racenum = Column(Integer, comment='R')
    title = Column(Text, comment='タイトル')
    coursetype = Column(Text, comment='形式')
    distance = Column(Integer, comment='距離')
    courseinfo1 = Column(Text, comment='情報1')
    courseinfo2 = Column(Text, comment='情報2')
    weather = Column(Text, comment='天候')
    condition = Column(Text, comment='状態')
    datetime = Column(DateTime(timezone=True), comment='日時')
    date = Column(Date, comment='日程')
    posttime = Column(Time(timezone=True), comment='時刻')
    generation = Column(Text, comment='世代')
    if engine.name in ['postgresql', 'mongodb']: racegrade = Column(pg.ARRAY(Text), comment='グレード')
    else: racegrade = Column(Text, comment='グレード')
    starters = Column(Integer, comment='頭数')
    if engine.name in ['postgresql', 'mongodb']: addedmoneylist = Column(pg.ARRAY(Integer), comment='賞金')
    else: addedmoneylist = Column(Text, comment='賞金')
    requrl = Column(Text, comment='raceurl')

    jrarecord = relationship('Jrarecord')

class Payback(Base):
    __tablename__ = 'paybacks'
    __table_args__ = (
        ForeignKeyConstraint(['raceid'], ['races.raceid']),
        {}
    )
    raceid = Column(Text, primary_key=True, comment='レースID')
    tansho = Column(pg.ARRAY(Integer), comment='単勝')
    tanshopay = Column(pg.ARRAY(Integer), comment='単勝払戻')
    tanshofav = Column(pg.ARRAY(Integer), comment='単勝人気')
    fukusho = Column(pg.ARRAY(Integer), comment='複勝')
    fukushopay = Column(pg.ARRAY(Integer), comment='複勝払戻')
    fukushofav = Column(pg.ARRAY(Integer), comment='複勝人気')
    wakuren = Column(pg.ARRAY(Integer), comment='枠連')
    wakurenpay = Column(pg.ARRAY(Integer), comment='枠連払戻')
    wakurenfav = Column(pg.ARRAY(Integer), comment='枠連人気')
    umaren = Column(pg.ARRAY(Integer), comment='馬連')
    umarenpay = Column(pg.ARRAY(Integer), comment='馬連払戻')
    umarenfav = Column(pg.ARRAY(Integer), comment='馬連人気')
    wide = Column(pg.ARRAY(Integer), comment='ワイド')
    widepay = Column(pg.ARRAY(Integer), comment='ワイド払戻')
    widefav = Column(pg.ARRAY(Integer), comment='ワイド人気')
    umatan = Column(pg.ARRAY(Integer), comment='馬単')
    umatanpay = Column(pg.ARRAY(Integer), comment='馬単払戻')
    umatanfav = Column(pg.ARRAY(Integer), comment='馬単人気')
    fuku3 = Column(pg.ARRAY(Integer), comment='3連複')
    fuku3pay = Column(pg.ARRAY(Integer), comment='3連複払戻')
    fuku3fav = Column(pg.ARRAY(Integer), comment='3連複人気')
    tan3 = Column(pg.ARRAY(Integer), comment='3連単')
    tan3pay = Column(pg.ARRAY(Integer), comment='3連単払戻')
    tan3fav = Column(pg.ARRAY(Integer), comment='3連単人気')

    race = relationship('Race')

class HorseResult(Base):
    __tablename__ = 'horseresults'
    __table_args__ = (
        ForeignKeyConstraint(['raceid'], ['races.raceid']),
        {}
    )
    raceid = Column(Text, primary_key=True, comment='レースID')

    ranking = Column(Integer, comment='着順')
    postnum = Column(Integer, comment='枠番')
    horsenum = Column(Integer, primary_key=True, comment='馬番')
    horsename = Column(Text, comment='馬名')
    sex = Column(Text, comment='性')
    age = Column(Integer, comment='齢')
    jockeyweight = Column(Float, comment='斤量')
    jockey = Column(Text, comment='騎手')
    time = Column(Time(timezone=False), comment='タイム')
    margin = Column(Text, comment='着差')

    fav = Column(Integer, comment='人気')
    odds = Column(Float, comment='オッズ')
    last3f = Column(Float, comment='上り')
    if engine.name in ['postgresql', 'mongodb']: passageratelist = Column(pg.ARRAY(Integer), comment='通過')
    else: passageratelist = Column(Text, comment='通過')
    affiliate = Column(Text, comment='所属')
    trainer = Column(Text, comment='調教師')
    horseweight = Column(Float, comment='馬体重')
    horseweightdiff = Column(Integer, comment='増減')

    race = relationship('Race')

    def getRaceResults(session):
        data = {}
        con = engine.connect()
        # sql = hrs.select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
        # sql = outerjoin(hrs, jrr).select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
        hrs = aliased(HorseResult, name='hrs')
        jrr = aliased(Jrarecord, name='jrr')
        sql = session\
            .query(Race.raceid, Race.place, Race.racenum, Race.title, Race.coursetype, Race.distance, Race.courseinfo1, Race.courseinfo2, jrr.time.label('record'), Race.weather, Race.condition, Race.datetime, Race.date, Race.posttime, Race.racegrade, Race.starters, Race.addedmoneylist, hrs.ranking, hrs.postnum, hrs.horsenum, hrs.horsename, hrs.sex, hrs.age, hrs.jockeyweight, hrs.jockey, hrs.time, hrs.margin, hrs.fav, hrs.odds, hrs.last3f, hrs.passageratelist, hrs.affiliate, hrs.trainer, hrs.horseweight, hrs.horseweightdiff)\
            .join(hrs).outerjoin(jrr).order_by(Race.place, Race.racenum, hrs.ranking).statement
        racesdf = pd.read_sql(sql, con)
        # if len(racesdf) == 0: return {'racesdf': pd.DataFrame(),'jockeys': pd.DataFrame(), 'racesgp2': pd.DataFrame()}

        racesdf.title = racesdf.title.apply(lambda x: x.rstrip('タイトル'))
        racesdf.posttime = racesdf.posttime.apply(lambda x: x.strftime('%H:%M'))
        racesdf.time = racesdf.time.apply(lambda x: x.strftime('%M:%S %f')[1:].rstrip('0') if x is not None else None)
        racesdf.record = racesdf.record.apply(lambda x: x.strftime('%M:%S %f')[1:].rstrip('0'))
        racesdf.fav = racesdf.fav.fillna(99).astype(int)
        racesdf.horseweight = racesdf.horseweight.fillna(0).astype(int)
        racesdf.horseweightdiff = racesdf.horseweightdiff.fillna(0).astype(int)

        racesdf = racesdf.sort_values(['place', 'racenum', 'ranking']).reset_index(drop=True)
        racesdf.ranking = racesdf[['place', 'racenum', 'ranking']].groupby(['place', 'racenum']).rank(method='dense', na_option='bottom').astype(int)
        racesdf['last3frank'] = racesdf[['place', 'racenum', 'last3f']].groupby(['place', 'racenum']).rank(method='dense', na_option='bottom').astype(int)

        racesdf['nextracerank'] = pd.concat([racesdf.ranking[1:], racesdf.ranking[0:1]]).reset_index(drop=True)
        racesdf['prevracerank'] = pd.concat([racesdf.ranking[-1:], racesdf.ranking[:-1]]).reset_index(drop=True)
        racesdf.loc[racesdf.ranking <= 3, 'rankinfo'] = 'initdisp_mid'
        racesdf.loc[(racesdf.ranking <= 3) & (racesdf.nextracerank > 3), 'rankinfo'] = 'initdisp_end'
        racesdf.loc[racesdf.ranking > 3, 'rankinfo'] = 'initnone_mid'
        racesdf.loc[racesdf.ranking - racesdf.prevracerank < 0, 'rankinfo'] = 'initdisp_top'
        racesdf.loc[(racesdf.rankinfo == 'initdisp_top') & (racesdf.nextracerank == 1), 'rankinfo'] = 'initdisp_topend'
        racesdf.loc[racesdf.nextracerank - racesdf.ranking < 0, 'rankinfo'] = 'initnone_end'

        sql = "SELECT psat.relname as TABLE_NAME, pa.attname as COLUMN_NAME, pd.description as COLUMN_COMMENT "
        sql += "FROM pg_stat_all_tables psat, pg_description pd, pg_attribute pa "
        sql += "WHERE psat.schemaname = (select schemaname from pg_stat_user_tables where relname = 'horseresults') "
        sql += "AND psat.relname IN ('races', 'horseresults') AND psat.relid=pd.objoid "
        sql += "AND pd.objsubid != 0 AND pd.objoid=pa.attrelid AND pd.objsubid=pa.attnum "
        sql += "ORDER BY pd.objsubid"

        jplabels = {}
        comments = pd.read_sql(sql, con)
        con.close()

        jockeyct = pd.crosstab([racesdf.place, racesdf.jockey], racesdf.ranking, margins=True)
        jockeyct.columns = [int(x) if type(x) is float else x for x in jockeyct.columns]
        ranges = [list(range(1, x+1)) for x in range(1, 4)]
        jockeyct['単勝率'], jockeyct['連対率'], jockeyct['複勝率'] = [round(100 * jockeyct[ranknum].sum(axis=1) / jockeyct.All, 1) for ranknum in ranges]

        jockeyct = jockeyct[[1,2,3, '単勝率', '連対率', '複勝率', 'All']].sort_values(['place',1,2,3], ascending=False)
        lastplace = ''
        lastindex = ''
        for index in jockeyct.index:
            if index[0] != lastplace:
                jockeyct.at[index, 'dispmode'] = 'place1st'
                jockeyct.at[lastindex, 'dispmode'] = 'placelast'

            lastplace = index[0]
            lastindex = index

        jockeyct = jockeyct.drop([('All', ''), ('', '')])
        for ranknum in ranges: jockeyct[ranknum] = jockeyct[ranknum].astype(int)
        jockeyct = jockeyct.rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})
        jockeysindex = list(jockeyct.columns)
        jockeysindex.remove('騎乗数')
        jockeysindex.insert(0,'騎乗数')
        jockeyct['騎乗数'] = jockeyct['騎乗数'].astype(int)
        jockeys = jockeyct[jockeysindex]
        for targetcol in ['1着', '2着', '3着', '単勝率', '連対率', '複勝率']:
            for place in jockeys.index.get_level_values(0).unique():
                tmprank = jockeys.loc[place, targetcol].rank(method='dense', ascending=False, na_option='bottom')
                tmprank.index = pd.MultiIndex.from_product([(place, ), tmprank.index])
                jockeys.loc[place, targetcol + '順'] = tmprank

            jockeys.loc[:, targetcol + '順'] = jockeys.loc[:, targetcol + '順'].astype(int)
            # jockeys[targetcol + '順'] = jockeys[targetcol + '順'].astype(int)

        data['jockeys'] = jockeys

        for comment in comments.loc[:, 'column_name':'column_comment'].iterrows():
            jplabels.update({comment[1].column_name: comment[1].column_comment})

        jplabels.update({'record': 'レコード'})
        data['racesdf'] = racesdf.rename(columns=jplabels)

        racesgp = cp.deepcopy(data['racesdf'])
        racesgp['R2'] = racesgp.R
        racesgp[['グレード', '賞金', '通過']] = racesgp[['グレード', '賞金', '通過']].applymap(str)
        racesgp = racesgp.query('着順 < 4').groupby(['場所','R','レースID','タイトル','形式','距離','天候','状態','情報1','日時','日程','時刻','グレード','頭数','賞金'])
        racesgp2 = racesgp.agg(list)
        racesgp2.R2 = racesgp2.R2.apply(set)
        racesgp2 = racesgp2.applymap(lambda x: '(' + ', '.join(map(str, x)) + ')')
        racesgp2 = racesgp2.groupby(['場所','形式']).agg(list).applymap(lambda x: '[' + ', '.join(map(str, x)) + ']')
        racesgp2 = racesgp2.applymap(lambda x: x.strip('['']'))
        racesgp2.R2 = racesgp2.R2.apply(lambda x: x.replace('(', '').replace(')', ''))
        data['racesgp2'] = racesgp2[['R2','枠番','馬番','人気','騎手']].rename(columns={'R2':'R'})

        return data

class Jrarecord(Base):
    __tablename__ = 'jrarecords'
    # __table_args__ = (UniqueConstraint(
    #     'place', 'coursetype', 'generation', 'distance', 'courseinfo1', 'courseinfo2'),
    #     {}
    # )
    # __mapper_args__ = {'column_prefix': 'jrarecords_'}
    place = Column(Text, primary_key=True, comment='場所')
    coursetype = Column(Text, primary_key=True, comment='形式')
    generation = Column(Text, primary_key=True, comment='世代')
    distance = Column(Integer, primary_key=True, comment='距離')
    courseinfo1 = Column(Text, primary_key=True, comment='情報1')
    courseinfo2 = Column(Text, primary_key=True, comment='情報2')
    time = Column(Time(timezone=False), comment='タイム')
    horsename = Column(Text, comment='馬名')
    sire = Column(Text, comment='父馬')
    dam = Column(Text, comment='母馬')
    sex = Column(Text, comment='性')
    age = Column(Integer, comment='齢')
    jockeyweight = Column(Float, comment='斤量')
    jockey = Column(Text, comment='騎手')
    jockeyfullname = Column(Text, comment='騎手姓名')
    date = Column(Date, comment='日程')
    weather = Column(Text, comment='天候')
    condition = Column(Text, comment='状態')
    reference = Column(Boolean, comment='基準')
