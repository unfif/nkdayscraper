# %%
from sqlalchemy import create_engine, ForeignKeyConstraint, func, text
from sqlalchemy.types import Integer, SmallInteger, Float, Text, Date, DateTime, Time, Boolean
from sqlalchemy.future import select
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import declarative_base, aliased, relationship, Mapped, mapped_column
from typing import Optional, List, Any
from nkdayscraper.utils.functions import getTargetDate
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
import datetime as dt
import pandas as pd
# pd.set_option('display.max_columns', 100); pd.set_option('display.max_rows', 500)

DATABASE_URL = get_project_settings().get('DATABASE_URL')
MONGO_URL = get_project_settings().get('MONGO_URL')
# ES_URL = get_project_settings().get('ES_URL')
# SQLITE_URL = get_project_settings().get('SQLITE_URL')
engine = create_engine(DATABASE_URL, echo=False, future=True)

class RBase():
    def __repr__(self):
        columns = [
            f'{column.name}={repr(self.__dict__[column.name])}'
            for column in self.__table__.c
        ]
        relationships = [
            f'{relation.key}={repr(self.__dict__.get(relation.key, {}))}'
            for relation in self.__mapper__.relationships
        ]
        key_values = ', '.join(columns + relationships)
        return f'<{self.__class__.__name__}({key_values})>'


    @staticmethod
    def makeCommentsQuery():
        schema = 'postgres'
        query = "SELECT psat.relname as table_name, pa.attname as column_name, pd.description as column_comment "
        query += "FROM pg_stat_all_tables psat "
        query += "JOIN pg_description pd ON psat.relid = pd.objoid "
        query += "JOIN pg_attribute pa ON pd.objoid = pa.attrelid AND pd.objsubid = pa.attnum "
        query += f"WHERE psat.schemaname = '{schema}' AND pd.objsubid != 0 "
        query += f"AND psat.relname IN (select relname from pg_stat_user_tables where schemaname = '{schema}') "
        query += "ORDER BY pd.objsubid"

        return text(query)

    @staticmethod
    def makeJpLabels(comments):
        jpLabels = {}
        for comment in comments.loc[:, 'column_name':'column_comment'].iterrows():
            jpLabels.update({comment[1].column_name: comment[1].column_comment})

        jpLabels.update({'record': 'レコード'})

        return jpLabels

    @staticmethod
    def makeJsonDict(data):
        jsonDict = {}
        for key, df in data.items():
            jsonDict[key] = df.to_json(orient='table', force_ascii=False)

        return jsonDict

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

def drop_race_tables(engine):
    if engine.has_table('paybacks'): Payback.__table__.drop(engine)
    if engine.has_table('horseresults'): HorseResult.__table__.drop(engine)
    if engine.has_table('races'): Race.__table__.drop(engine)

def drop_race_related_tables(engine):
    drop_race_tables(engine)
    if engine.has_table('jrarecords'): Jrarecord.__table__.drop(engine)

class Race(Base):
    __tablename__ = 'races'
    __table_args__ = (
        ForeignKeyConstraint(
            ['place', 'coursetype', 'generation', 'distance', 'courseinfo1', 'courseinfo2'],
            ['jrarecords.place', 'jrarecords.coursetype', 'jrarecords.generation', 'jrarecords.distance', 'jrarecords.courseinfo1', 'jrarecords.courseinfo2']
        ),
        {'comment': 'レース'}
    )
    raceid: Mapped[str] = mapped_column(Text, primary_key=True, unique=True, comment='レースID')
    year: Mapped[Optional[int]] = mapped_column(Integer, comment='年')
    place: Mapped[Optional[str]] = mapped_column(Text, comment='場所')
    holdtimesnum: Mapped[Optional[int]] = mapped_column(Integer, comment='開催回数')
    holddaysnum: Mapped[Optional[int]] = mapped_column(Integer, comment='開催日数')
    racenum: Mapped[Optional[int]] = mapped_column(Integer, comment='R')
    title: Mapped[Optional[str]] = mapped_column(Text, comment='タイトル')
    coursetype: Mapped[Optional[str]] = mapped_column(Text, comment='形式')
    distance: Mapped[Optional[int]] = mapped_column(Integer, comment='距離')
    courseinfo1: Mapped[Optional[str]] = mapped_column(Text, comment='情報1')
    courseinfo2: Mapped[Optional[str]] = mapped_column(Text, comment='情報2')
    agecondition: Mapped[Optional[str]] = mapped_column(Text, comment='馬齢条件')
    classcondition: Mapped[Optional[str]] = mapped_column(Text, comment='クラス')
    racecondition: Mapped[Optional[str]] = mapped_column(Text, comment='条件')
    weight: Mapped[Optional[str]] = mapped_column(Text, comment='重量')
    weather: Mapped[Optional[str]] = mapped_column(Text, comment='天候')
    coursecondition: Mapped[Optional[str]] = mapped_column(Text, comment='状態')
    date: Mapped[Optional[dt.date]] = mapped_column(Date, comment='日程')
    datetime: Mapped[Optional[dt.datetime]] = mapped_column(DateTime(timezone=True), comment='日時')
    posttime: Mapped[Optional[dt.time]] = mapped_column(Time(timezone=True), comment='時刻')
    generation: Mapped[Optional[str]] = mapped_column(Text, comment='世代')
    starters: Mapped[Optional[int]] = mapped_column(Integer, comment='頭数')
    addedmoney_1st: Mapped[Optional[int]] = mapped_column(Integer, comment='1着賞金')
    addedmoney_2nd: Mapped[Optional[int]] = mapped_column(Integer, comment='2着賞金')
    addedmoney_3rd: Mapped[Optional[int]] = mapped_column(Integer, comment='3着賞金')
    addedmoney_4th: Mapped[Optional[int]] = mapped_column(Integer, comment='4着賞金')
    addedmoney_5th: Mapped[Optional[int]] = mapped_column(Integer, comment='5着賞金')
    requrl: Mapped[Optional[str]] = mapped_column(Text, comment='結果URL')

    jrarecord = relationship('Jrarecord', back_populates='races')
    horseresults = relationship('HorseResult', back_populates='race')
    payback = relationship('Payback', back_populates='race')

    def getRecords(self, date=None):
        with engine.connect() as conn:
            records = pd.read_sql(self.makeRecordsQuery(date), conn)
            comments = pd.read_sql(self.makeCommentsQuery(), conn)

        jpLabels = self.makeJpLabels(comments)
        data = {
            'records': records.rename(columns=jpLabels).copy(deep=True),
        }
        data['json'] = self.makeJsonDict(data)

        return data

    @staticmethod
    def makeRecordsQuery(date=None):
        filterQuery = Race.date == date if date else True
        query = select(Race)\
        .filter(filterQuery)\
        .order_by(Race.date, Race.place, Race.racenum)

        return query

class Payback(Base):
    __tablename__ = 'paybacks'
    __table_args__ = (
        ForeignKeyConstraint(
            ['raceid'], ['races.raceid']
        ),
        {'comment': '払戻し'}
    )
    raceid: Mapped[str] = mapped_column(Text, primary_key=True, unique=True, comment='レースID')
    tansho: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='単勝')
    tanshopay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='単勝払戻')
    tanshofav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='単勝人気')
    fukusho: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='複勝')
    fukushopay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='複勝払戻')
    fukushofav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='複勝人気')
    wakuren: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='枠連')
    wakurenpay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='枠連払戻')
    wakurenfav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='枠連人気')
    umaren: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='馬連')
    umarenpay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='馬連払戻')
    umarenfav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='馬連人気')
    wide: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='ワイド')
    widepay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='ワイド払戻')
    widefav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='ワイド人気')
    umatan: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='馬単')
    umatanpay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='馬単払戻')
    umatanfav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='馬単人気')
    fuku3: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='3連複')
    fuku3pay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='3連複払戻')
    fuku3fav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='3連複人気')
    tan3: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='3連単')
    tan3pay: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='3連単払戻')
    tan3fav: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='3連単人気')

    race = relationship('Race', back_populates='payback')

class Jrarecord(Base):
    __tablename__ = 'jrarecords'
    __table_args__ = (
        ForeignKeyConstraint(['place'], ['racecourses.place']),
        {'comment': 'JRAレコード'}
    )
    place: Mapped[str] = mapped_column(Text, primary_key=True, comment='場所')
    coursetype: Mapped[str] = mapped_column(Text, primary_key=True, comment='形式')
    distance: Mapped[int] = mapped_column(Integer, primary_key=True, comment='距離')
    courseinfo1: Mapped[str] = mapped_column(Text, primary_key=True, comment='情報1')
    courseinfo2: Mapped[str] = mapped_column(Text, primary_key=True, comment='情報2')
    time: Mapped[Optional[dt.time]] = mapped_column(Time(timezone=False), comment='タイム')
    horsename: Mapped[Optional[str]] = mapped_column(Text, comment='馬名')
    sire: Mapped[Optional[str]] = mapped_column(Text, comment='父馬')
    dam: Mapped[Optional[str]] = mapped_column(Text, comment='母馬')
    sex: Mapped[Optional[str]] = mapped_column(Text, comment='性')
    age: Mapped[Optional[int]] = mapped_column(Integer, comment='齢')
    jockeyweight: Mapped[Optional[float]] = mapped_column(Float, comment='斤量')
    jockey: Mapped[Optional[str]] = mapped_column(Text, comment='騎手')
    jockeyfullname: Mapped[Optional[str]] = mapped_column(Text, comment='騎手姓名')
    date: Mapped[Optional[dt.date]] = mapped_column(Date, comment='日程')
    generation: Mapped[str] = mapped_column(Text, primary_key=True, comment='世代')
    weather: Mapped[Optional[str]] = mapped_column(Text, comment='天候')
    coursecondition: Mapped[Optional[str]] = mapped_column(Text, comment='状態')
    reference: Mapped[Optional[bool]] = mapped_column(Boolean, comment='基準')

    races = relationship('Race', back_populates='jrarecord')

class HorseResult(Base):
    __tablename__ = 'horseresults'
    __table_args__ = (
        ForeignKeyConstraint(['raceid'], ['races.raceid']),
        {'comment': '結果'}
    )
    raceid: Mapped[str] = mapped_column(Text, primary_key=True, comment='レースID')

    ranking: Mapped[Optional[int]] = mapped_column(Integer, comment='着順')
    postnum: Mapped[Optional[int]] = mapped_column(Integer, comment='枠番')
    horseid: Mapped[Optional[int]] = mapped_column(Integer, comment='馬ID')
    horsenum: Mapped[int] = mapped_column(Integer, primary_key=True, comment='馬番')
    horsename: Mapped[Optional[str]] = mapped_column(Text, comment='馬名')
    horseurl: Mapped[Optional[str]] = mapped_column(Text, comment='馬URL')
    sex: Mapped[Optional[str]] = mapped_column(Text, comment='性')
    age: Mapped[Optional[int]] = mapped_column(Integer, comment='齢')
    jockeyweight: Mapped[Optional[float]] = mapped_column(Float, comment='斤量')
    jockey: Mapped[Optional[str]] = mapped_column(Text, comment='騎手')
    jockeyurl: Mapped[Optional[str]] = mapped_column(Text, comment='騎手URL')
    time: Mapped[Optional[dt.time]] = mapped_column(Time(timezone=False), comment='タイム')
    margin: Mapped[Optional[str]] = mapped_column(Text, comment='着差')

    fav: Mapped[Optional[int]] = mapped_column(Integer, comment='人気')
    odds: Mapped[Optional[float]] = mapped_column(Float, comment='オッズ')
    last3f: Mapped[Optional[float]] = mapped_column(Float, comment='上り')
    if engine.name in ['postgresql', 'mongodb']: passageratelist: Mapped[Optional[List[int]]] = mapped_column(pg.ARRAY(Integer), comment='通過')
    else: passageratelist: Mapped[Optional[str]] = mapped_column(Text, comment='通過')
    passageratelist: Mapped[Optional[str]] = mapped_column(Text, comment='通過')
    passagerate_1st: Mapped[Optional[int]] = mapped_column(Integer, comment='通過1')
    passagerate_2nd: Mapped[Optional[int]] = mapped_column(Integer, comment='通過2')
    passagerate_3rd: Mapped[Optional[int]] = mapped_column(Integer, comment='通過3')
    passagerate_4th: Mapped[Optional[int]] = mapped_column(Integer, comment='通過4')
    affiliate: Mapped[Optional[str]] = mapped_column(Text, comment='所属')
    trainer: Mapped[Optional[str]] = mapped_column(Text, comment='調教師')
    trainerurl: Mapped[Optional[str]] = mapped_column(Text, comment='調教師URL')
    horseweight: Mapped[Optional[float]] = mapped_column(Float, comment='馬体重')
    horseweightdiff: Mapped[Optional[int]] = mapped_column(Integer, comment='増減')

    race = relationship('Race', back_populates='horseresults')

    def getRecords(self, date=None):
        if date is None: date = getTargetDate()
        elif type(date) == 'str': date = dt.date(*[int(str) for str in date.split('-')])
        with engine.connect() as conn:
            records = pd.read_sql(self.makeRecordsQuery(date), conn)
            comments = pd.read_sql(self.makeCommentsQuery(), conn)

        data = {'json': ''}
        if not records.empty:
            jpLabels = self.makeJpLabels(comments)
            records = self.makeRecords(records)
            data = {
                'jockeys': self.makeJockeys(records),
                'records': records.rename(columns=jpLabels).copy(deep=True),
                'racesinfo': pd.DataFrame({'date': records.date[0], 'places': [records.place.unique()]})
            }
            data['results'] = self.makeResults(data['records'])
            data['json'] = self.makeJsonDict(data)

        return data

    @staticmethod
    def makeRecordsQuery(date=None):
        hrs = aliased(HorseResult, name='hrs')
        jrr = aliased(Jrarecord, name='jrr')
        pay = aliased(Payback, name='pay')
        filterQuery = Race.date == date if date else True
        query = select(
            Race.raceid, Race.year, Race.place, Race.racenum, Race.title, Race.coursetype, Race.distance, Race.courseinfo1, Race.courseinfo2, jrr.time.label('record'), Race.weather, Race.coursecondition, Race.date, Race.datetime, Race.posttime, Race.generation, Race.starters, Race.requrl, Race.agecondition, Race.classcondition, Race.racecondition, Race.weight, Race.addedmoney_1st, Race.addedmoney_2nd, Race.addedmoney_3rd, Race.addedmoney_4th, Race.addedmoney_5th, Race.holdtimesnum, Race.holddaysnum,
            hrs.ranking, hrs.postnum, hrs.horseid, hrs.horsenum, hrs.horsename, hrs.horseurl, hrs.sex, hrs.age, hrs.jockeyweight, hrs.jockey, hrs.jockeyurl, hrs.time, hrs.margin, hrs.fav, hrs.odds, hrs.last3f, hrs.passageratelist, hrs.affiliate, hrs.trainer, hrs.trainerurl, hrs.horseweight, hrs.horseweightdiff, hrs.passagerate_1st, hrs.passagerate_2nd, hrs.passagerate_3rd, hrs.passagerate_4th,
            pay.tansho, pay.tanshopay, pay.tanshofav, pay.fukusho, pay.fukushopay, pay.fukushofav, pay.wakuren, pay.wakurenpay, pay.wakurenfav, pay.umaren, pay.umarenpay, pay.umarenfav, pay.wide, pay.widepay, pay.widefav, pay.umatan, pay.umatanpay, pay.umatanfav, pay.fuku3, pay.fuku3pay, pay.fuku3fav, pay.tan3, pay.tan3pay, pay.tan3fav
        )\
        .outerjoin(hrs)\
        .outerjoin(pay)\
        .outerjoin(jrr)\
        .filter(filterQuery)\
        .order_by(Race.place, Race.racenum, hrs.ranking)

        return query

    @staticmethod
    def makeRecords(records):
        records.title = records.title.apply(lambda x: x.rstrip('タイトル'))
        records.posttime = records.posttime.fillna(dt.datetime(1900, 1, 1, hour=0, minute=0)).apply(lambda x: x.strftime('%H:%M'))
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

    @staticmethod
    def makeJockeys(records):
        if records.jockey.dropna().empty: records.jockey = pd.Series(['未確定'] * records.shape[0])
        jockeyct = pd.crosstab([records.place, records.jockey.dropna()], records.ranking, margins=True)
        jockeyct.columns = [int(x) if type(x) is float else x for x in jockeyct.columns]
        for x in [1, 2, 3]:
            if x not in jockeyct.columns: jockeyct[x] = 0

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

    @staticmethod
    def makeResults(records):
        agg_groups = records.query('着順 < 4')[['場所', '形式', 'R', '距離', '天候', '状態', '時刻', '枠番', '馬番', '人気', '騎手']].groupby(['場所', '形式', 'R', '距離', '天候', '状態', '時刻'], as_index=False).agg(list).reset_index(drop=True)
        count_groups = agg_groups.groupby(['場所', '形式'], as_index=False)
        agg_groups = agg_groups.merge(count_groups.size(), on=['場所', '形式'])
        if not agg_groups.empty:
            agg_groups['cumcount_inc'] = None
            agg_groups['cumcount_inc'] = count_groups.cumcount().apply(lambda x: x + 1)
            agg_groups.loc[agg_groups['cumcount_inc'] == 1, 'display_top'] = True
            agg_groups.loc[agg_groups['cumcount_inc'] == agg_groups['size'], 'display_bottom'] = True
            agg_groups = agg_groups.drop(columns=['cumcount_inc'])

        return agg_groups

    @staticmethod
    def countResults():
        with engine.connect() as conn:
            race = [row[0] for row in conn.execute(select(func.count('*')).select_from(Race))][0]
            horse_results = [row[0] for row in conn.execute(select(func.count('*')).select_from(HorseResult))][0]

        counts = {'count': {'Race': race, 'HorseResult': horse_results}}
        return counts

class Racecourse(Base):
    __tablename__ = 'racecourses'
    __table_args__ = (
        {'comment': 'コース'}
    )
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True, comment='コースID')
    place: Mapped[str] = mapped_column(Text, primary_key=True, unique=True, comment='コース名')

class Racedate(Base):
    __tablename__ = 'racedates'
    __table_args__ = (
        {'comment': '開催日'}
    )
    date: Mapped[dt.date] = mapped_column(Date, primary_key=True, comment='日程')
    weekday: Mapped[Optional[int]] = mapped_column(SmallInteger, comment='曜日')
    is_holiday: Mapped[Optional[bool]] = mapped_column(Boolean, comment='祝日')
    gradeRace: Mapped[Optional[dict[str, Any]]] = mapped_column(pg.ARRAY(pg.JSONB), comment='レース')
    option: Mapped[Optional[dict[str, Any]]] = mapped_column(pg.ARRAY(pg.JSONB), comment='option')
    race: Mapped[Optional[dict[str, Any]]] = mapped_column(pg.ARRAY(pg.JSONB), comment='開催')
