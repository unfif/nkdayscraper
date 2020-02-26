from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, Date, DateTime, Time, Float#, Boolean, LargeBinary, SmallInteger
from sqlalchemy.dialects import postgresql as pg
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

DATABASE_URL = get_project_settings().get('DATABASE_URL')
SQLITE_URL = get_project_settings().get('SQLITE_URL')
MONGO_URL = get_project_settings().get('MONGO_URL')
basename = DATABASE_URL.split(':')[0].split('+')[0]

class RBase():
    def __repr__(self):
        columns = ', '.join([
            '{0}={1}'.format(key, repr(self.__dict__[key]))
            for key in self.__dict__.keys() if not key.startswith('_')
        ])
        return '<{0}({1})>'.format(self.__class__.__name__, columns)

Base = declarative_base(cls=RBase)

def db_connect(url=DATABASE_URL, echo=False):
    engine = create_engine(url, echo=echo)
    return engine

def mongo_connect(url=MONGO_URL, query=None):
    if url is None: url = 'mongodb://localhost:27017'
    if type(query) is dict:
        if not url.endswith('/'): url += '/'
        url += '?'
        for key, val in query.items():
            url += key + '=' + str(val)

    client = MongoClient(url)
    return client

def create_table(engine):
    Base.metadata.create_all(engine)

class Nkdayraces(Base):
    __tablename__ = 'nkdayraces'

    # _id = None
    datekey = Column(Text, primary_key=True, comment='datekey')
    raceid = Column(Text, primary_key=True, comment='レースID')
    year = Column(Integer, comment='年')
    place = Column(Text, comment='場所')
    racenum = Column(Integer, comment='R')
    title = Column(Text, comment='クラス')
    courcetype = Column(Text, comment='形式')
    distance = Column(Integer, comment='距離')
    direction = Column(Text, comment='情報')
    weather = Column(Text, comment='天候')
    condition = Column(Text, comment='状態')
    date = Column(DateTime(timezone=True), comment='日時')
    day = Column(Date, comment='日程')
    posttime = Column(Time(timezone=True), comment='時刻')
    racegrade = Column(Text, comment='グレード')
    starters = Column(Integer, comment='頭数')
    if basename in ['postgresql', 'mongodb']: addedmoneylist = Column(pg.ARRAY(Integer), comment='賞金')
    else: addedmoneylist = Column(Text, comment='賞金')

    requrl = Column(Text, comment='raceurl')
    placenum = Column(Integer, comment='順位')
    postnum = Column(Integer, comment='枠番')
    horsenum = Column(Integer, primary_key=True, comment='馬番')
    horsename = Column(Text, comment='馬名')
    sex = Column(Text, comment='性')
    age = Column(Integer, comment='齢')
    weight = Column(Float, comment='斤量')
    jockey = Column(Text, comment='騎手')
    time = Column(Time(timezone=False), comment='タイム')
    margin = Column(Text, comment='着差')
    if basename in ['postgresql', 'mongodb']: positionlist = Column(pg.ARRAY(Integer), comment='通過')
    else: positionlist = Column(Text, comment='通過')

    last3f = Column(Float, comment='上り')
    odds = Column(Float, comment='オッズ')
    fav = Column(Integer, comment='人気')
    trainer = Column(Text, comment='調教師')
    horseweight = Column(Float, comment='馬体重')
    horseweightdiff = Column(Integer, comment='増減')
    # owner = Column(Text)
    # addedmoney = Column(Integer)

    # def __repr__(self):
    #     return  "<nkdayraces(raceid='{}',place='{}',racenum='{}',title='{}',courcetype='{}',distance='{}',direction='{}',weather='{}',condition='{},date='{}',day='{}',posttime='{}',racegrade='{}',starters='{}',addedmoneylist='{}',requrl='{}',placenum='{}',postnum='{}',horsenum='{}',horsename='{}',sex='{}',age='{}',weight='{}',jockey='{}',time='{}',margin='{}',positionlist='{}',last3f='{}',odds='{}',fav='{}',trainer='{}',horseweight='{}',horseweightdiff='{}')>".format(self.raceid,self.place,self.racenum,self.title,self.courcetype,self.distance,self.direction,self.weather,self.condition,self.date,self.day,self.posttime,self.racegrade,self.starters,self.addedmoneylist,self.requrl,self.placenum,self.postnum,self.horsenum,self.horsename,self.sex,self.age,self.weight,self.jockey,self.time,self.margin,self.positionlist,self.last3f,self.odds,self.fav,self.trainer,self.horseweight,self.horseweightdiff)
