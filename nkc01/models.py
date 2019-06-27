from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, Date, DateTime, Time, Float#, Boolean, LargeBinary, SmallInteger
from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_connect(is_echo = False):
    """Performs database connection using database settings from settings.py. Returns sqlalchemy engine instance"""
    return create_engine(get_project_settings().get('URI'), echo=is_echo)

def create_table(engine):
    Base.metadata.create_all(engine)

class nkthedayraces(Base):
    __tablename__ = 'nkthedayraces'

    raceid = Column(Text, primary_key=True)
    place = Column(Text)
    racenum = Column(Integer)
    title = Column(Text)
    courcetype = Column(Text)
    distance = Column(Integer)
    direction = Column(Text)
    weather = Column(Text)
    condition = Column(Text)
    posttime = Column(Time)
    date = Column(Date)
    racegrade = Column(Text)
    starters = Column(Integer)
    raceaddedmoney = Column(Text)

    placenum = Column(Integer, primary_key=True)
    postnum = Column(Integer)
    horsenum = Column(Integer)
    horsename = Column(Text)
    sex = Column(Text)
    age = Column(Integer)
    weight = Column(Float)
    jockey = Column(Text)
    time = Column(Time)
    margin = Column(Text)
    position = Column(Text)
    last3f = Column(Float)
    odds = Column(Float)
    fav = Column(Integer)
    trainer = Column(Text)
    horseweight = Column(Float)
    horseweightdiff = Column(Integer)
    # owner = Column(Text)
    # addedmoney = Column(Integer)

    # def __repr__(self):
    #    return "f<User(name='{}', fullname='{}', nickname='{}')>".format(
    #        self.name, self.fullname, self.nickname
    #    )
