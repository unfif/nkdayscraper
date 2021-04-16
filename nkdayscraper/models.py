# %%
from sqlalchemy import create_engine, Column, Integer, Float, Text, Date, DateTime, Time, Boolean, ForeignKeyConstraint#, ForeignKey, UniqueConstraint, outerjoin, and_, LargeBinary, SmallInteger
from sqlalchemy.future import select
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import declarative_base, relationship, aliased
from .spiders.nkday import getTargetDate
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
import pandas as pd
# pd.set_option('display.max_columns', 100);pd.set_option('display.max_rows', 500)

DATABASE_URL = get_project_settings().get('DATABASE_URL')
MONGO_URL = get_project_settings().get('MONGO_URL')
# ES_URL = get_project_settings().get('ES_URL')
# SQLITE_URL = get_project_settings().get('SQLITE_URL')
engine = create_engine(DATABASE_URL, echo=False, future=False)

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
            url += f'{key}={str(val)}'

    client = MongoClient(url)
    return client

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_race_tables(engine):
    if engine.has_table('paybacks'): Payback.__table__.drop(engine)
    if engine.has_table('horseresults'): HorseResult.__table__.drop(engine)
    if engine.has_table('races'): Race.__table__.drop(engine)

def drop_tables(engine):
    drop_race_tables(engine)
    if engine.has_table('jrarecords'): Jrarecord.__table__.drop(engine)

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
    requrl = Column(Text, comment='結果URL')

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

class Jrarecord(Base):
    __tablename__ = 'jrarecords'
    # __table_args__ = (ForeignKeyConstraint(
    #     ['place', 'coursetype', 'generation', 'distance', 'courseinfo1', 'courseinfo2'],
    #     ['races.place', 'races.coursetype', 'races.generation', 'races.distance', 'races.courseinfo1', 'races.courseinfo2']),
    #     {}
    # )
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

    # race = relationship('Race')

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
    horseurl = Column(Text, comment='馬URL')
    sex = Column(Text, comment='性')
    age = Column(Integer, comment='齢')
    jockeyweight = Column(Float, comment='斤量')
    jockey = Column(Text, comment='騎手')
    jockeyurl = Column(Text, comment='騎手URL')
    time = Column(Time(timezone=False), comment='タイム')
    margin = Column(Text, comment='着差')

    fav = Column(Integer, comment='人気')
    odds = Column(Float, comment='オッズ')
    last3f = Column(Float, comment='上り')
    if engine.name in ['postgresql', 'mongodb']: passageratelist = Column(pg.ARRAY(Integer), comment='通過')
    else: passageratelist = Column(Text, comment='通過')
    affiliate = Column(Text, comment='所属')
    trainer = Column(Text, comment='調教師')
    trainerurl = Column(Text, comment='調教師URL')
    horseweight = Column(Float, comment='馬体重')
    horseweightdiff = Column(Integer, comment='増減')

    race = relationship('Race')

    def getRaceResults(self):
        data = {}
        targetDate = getTargetDate()
        with engine.connect() as conn:
            records = pd.read_sql(self.makeRecordsQuery(targetDate), conn)
            comments = pd.read_sql(self.makeCommentsQuery(), conn)

        jpLabels = self.makeJpLabels(comments)
        records = self.makeRecords(records)
        data['jockeys'] = self.makeJockeys(records)
        data['records'] = records.rename(columns=jpLabels).copy(deep=True)
        data['racesinfo'] = pd.DataFrame({'date': records.date[0], 'places': [records.place.unique()]})
        data['racesgp2'] = self.makeRacesgp2(data['records'])
        data['json'] = self.makeJsonDict(data)
        
        return data

    def makeRecordsQuery(self, date):
        hrs = aliased(HorseResult, name='hrs')
        jrr = aliased(Jrarecord, name='jrr')
        pay = aliased(Payback, name='pay')
        query = select(
            Race.raceid, Race.place, Race.racenum, Race.title, Race.coursetype, Race.distance, Race.courseinfo1, Race.courseinfo2, jrr.time.label('record'), Race.weather, Race.condition, Race.datetime, Race.date, Race.posttime, Race.racegrade, Race.starters, Race.addedmoneylist, Race.requrl,
            hrs.ranking, hrs.postnum, hrs.horsenum, hrs.horsename, hrs.sex, hrs.age, hrs.jockeyweight, hrs.jockey, hrs.time, hrs.margin, hrs.fav, hrs.odds, hrs.last3f, hrs.passageratelist, hrs.affiliate, hrs.trainer, hrs.horseweight, hrs.horseweightdiff, hrs.horseurl, hrs.jockeyurl, hrs.trainerurl,
            pay.tansho, pay.tanshopay, pay.tanshofav, pay.fukusho, pay.fukushopay, pay.fukushofav, pay.wakuren, pay.wakurenpay, pay.wakurenfav, pay.umaren, pay.umarenpay, pay.umarenfav, pay.wide, pay.widepay, pay.widefav, pay.umatan, pay.umatanpay, pay.umatanfav, pay.fuku3, pay.fuku3pay, pay.fuku3fav, pay.tan3, pay.tan3pay, pay.tan3fav
        )\
        .join(hrs)\
        .outerjoin(pay)\
        .outerjoin(jrr)\
        .filter(Race.date == date)\
        .order_by(Race.place, Race.racenum, hrs.ranking)

        return query

    def makeCommentsQuery(self):
        query = "SELECT psat.relname as TABLE_NAME, pa.attname as COLUMN_NAME, pd.description as COLUMN_COMMENT "
        query += "FROM pg_stat_all_tables psat, pg_description pd, pg_attribute pa "
        query += "WHERE psat.schemaname = (select schemaname from pg_stat_user_tables where relname = 'horseresults') "
        query += "AND psat.relname IN ('races', 'horseresults', 'jrarecords', 'paybacks') AND psat.relid=pd.objoid "
        query += "AND pd.objsubid != 0 AND pd.objoid=pa.attrelid AND pd.objsubid=pa.attnum "
        query += "ORDER BY pd.objsubid"

        return query

    def makeJpLabels(self, comments):
        jpLabels = {}
        for comment in comments.loc[:, 'column_name':'column_comment'].iterrows():
            jpLabels.update({comment[1].column_name: comment[1].column_comment})

        jpLabels.update({'record': 'レコード'})

        return jpLabels

    def makeRecords(self, records):
        records.title = records.title.apply(lambda x: x.rstrip('タイトル'))
        records.posttime = records.posttime.apply(lambda x: x.strftime('%H:%M'))
        records.time = records.time.apply(lambda x: x.strftime('%M:%S %f')[1:].rstrip('0') if x is not None else None)
        records.record = records.record.apply(lambda x: x.strftime('%M:%S %f')[1:].rstrip('0'))
        records.fav = records.fav.fillna(99).astype(int)
        records.horseweight = records.horseweight.fillna(0).astype(int)
        records.horseweightdiff = records.horseweightdiff.fillna(0).astype(int)

        records = records.sort_values(['place', 'racenum', 'ranking']).reset_index(drop=True)
        records.ranking = records[['place', 'racenum', 'ranking']].groupby(['place', 'racenum']).rank(method='dense', na_option='bottom').astype(int)
        records['last3frank'] = records[['place', 'racenum', 'last3f']].groupby(['place', 'racenum']).rank(method='dense', na_option='bottom').astype(int)

        records.loc[records.ranking <= 3, 'rankinfo'] = 'initdisp_mid'
        records.loc[records.ranking > 3, 'rankinfo'] = 'initnone_mid'
        records.loc[records.racenum.diff().fillna(12) != 0, 'rankinfo'] = 'initdisp_top'

        return records

    def makeJockeys(self, records):
        jockeyct = pd.crosstab([records.place, records.jockey], records.ranking, margins=True)
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
        jockeyct = jockeyct.rename(columns={1: '1着', 2: '2着', 3: '3着', 'All': '騎乗数'})
        jockeysindex = list(jockeyct.columns)
        jockeysindex.remove('騎乗数')
        jockeysindex.insert(0,'騎乗数')
        jockeyct['騎乗数'] = jockeyct['騎乗数'].astype(int)
        jockeys = jockeyct[jockeysindex].copy(deep=True)
        for targetcol in ['1着', '2着', '3着', '単勝率', '連対率', '複勝率']:
            for place in jockeys.index.get_level_values(0).unique():
                tmprank = jockeys.loc[place, targetcol].rank(method='dense', ascending=False, na_option='bottom')
                tmprank.index = pd.MultiIndex.from_product([(place, ), tmprank.index])
                jockeys.loc[place, f'{targetcol}順'] = tmprank

            jockeys.loc[:, f'{targetcol}順'] = jockeys.loc[:, f'{targetcol}順'].astype(int)

        return jockeys

    def makeRacesgp2(self, records):
        racesgp = records
        racesgp['R2'] = racesgp.R
        racesgp[['グレード', '賞金', '通過']] = racesgp[['グレード', '賞金', '通過']].applymap(str)
        racesgp = racesgp.query('着順 < 4').groupby(['場所','R','レースID','タイトル','形式','距離','天候','状態','情報1','日時','日程','時刻','グレード','頭数','賞金'])
        racesgp2 = racesgp.agg(list)
        racesgp2.R2 = racesgp2.R2.apply(set)
        racesgp2 = racesgp2.applymap(lambda x: '(' + ', '.join(map(str, x)) + ')')
        racesgp2 = racesgp2.groupby(['場所','形式']).agg(list).applymap(lambda x: '[' + ', '.join(map(str, x)) + ']')
        racesgp2 = racesgp2.applymap(lambda x: x.strip('['']'))
        racesgp2.R2 = racesgp2.R2.apply(lambda x: x.replace('(', '').replace(')', ''))

        return racesgp2[['R2','枠番','馬番','人気','騎手']].rename(columns={'R2':'R'})

    def makeJsonDict(self, data):
        jsonDict = {}
        for key, df in data.items():
            jsonDict[key] = df.to_json(orient='table', force_ascii=False)
            # jsonDict[key] = df.to_dict(orient='records')

        return jsonDict
