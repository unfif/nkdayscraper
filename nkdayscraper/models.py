from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, Date, DateTime, Time, Float#, Boolean, LargeBinary, SmallInteger
from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_connect(is_echo = False):
    """Performs database connection using database settings from settings.py. Returns sqlalchemy engine instance"""
    engine = create_engine(get_project_settings().get('DATABASE_URL'))
    return engine

def create_table(engine):
    Base.metadata.create_all(engine)

class Nkdayraces(Base):
    __tablename__ = 'nkdayraces'

    raceid = Column(Text, primary_key=True, comment='レースID')
    place = Column(Text, comment='場所')
    racenum = Column(Integer, comment='R')
    title = Column(Text, comment='クラス')
    courcetype = Column(Text, comment='形式')
    distance = Column(Integer, comment='距離')
    direction = Column(Text, comment='情報')
    weather = Column(Text, comment='天候')
    condition = Column(Text, comment='状態')
    date = Column(DateTime, comment='日時')
    day = Column(Date, comment='日程')
    posttime = Column(Time, comment='時刻')
    racegrade = Column(Text, comment='グレード')
    starters = Column(Integer, comment='頭数')
    raceaddedmoney = Column(Text, comment='賞金')
    requrl = Column(Text, comment='raceurl')

    placenum = Column(Integer, primary_key=True, comment='順位')
    postnum = Column(Integer, comment='枠番')
    horsenum = Column(Integer, comment='馬番')
    horsename = Column(Text, comment='馬名')
    sex = Column(Text, comment='性')
    age = Column(Integer, comment='齢')
    weight = Column(Float, comment='斤量')
    jockey = Column(Text, comment='騎手')
    time = Column(Time, comment='タイム')
    margin = Column(Text, comment='着差')
    position = Column(Text, comment='通過')
    last3f = Column(Float, comment='上り')
    odds = Column(Float, comment='オッズ')
    fav = Column(Integer, comment='人気')
    trainer = Column(Text, comment='調教師')
    horseweight = Column(Float, comment='馬体重')
    horseweightdiff = Column(Integer, comment='増減')
    # owner = Column(Text)
    # addedmoney = Column(Integer)

    def __repr__(self):
        return "f<nkdayraces(raceid='{}',place='{}',racenum='{}',title='{}',courcetype='{}',distance='{}',direction='{}',weather='{}',condition='{},datetime='{}',racegrade='{}',starters='{}',raceaddedmoney='{}',requrl='{}',placenum='{}',postnum='{}',horsenum='{}',horsename='{}',sex='{}',age='{}',weight='{}',jockey='{}',time='{}',margin='{}',position='{}',last3f='{}',odds='{}',fav='{}',trainer='{}',horseweight='{}',horseweightdiff='{}')>".format(self.raceid,self.place,self.racenum,self.title,self.courcetype,self.distance,self.direction,self.weather,self.condition,self.datetime,self.racegrade,self.starters,self.raceaddedmoney,self.requrl,self.placenum,self.postnum,self.horsenum,self.horsename,self.sex,self.age,self.weight,self.jockey,self.time,self.margin,self.position,self.last3f,self.odds,self.fav,self.trainer,self.horseweight,self.horseweightdiff
        )
