#%%
import os
os.chdir('/Users/pathz/Documents/scrapy/nkdayscraper'); print(os.getcwd())
from sqlalchemy import create_engine, select, update, delete, between, extract
from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Racedate, Racecourse, Jrarecord, Race, HorseResult, Payback
import datetime as dt
from dotenv import dotenv_values
from pprint import pprint

env = dotenv_values('.env')
DATABASE_URL = env['DATABASE_URL']
engine = create_engine(DATABASE_URL, echo=True, future=True)
# where = between(
#     Racedate.date,
#     dt.date(2023, 3, 31),
#     dt.date(2023, 4, 9)
# )
# where = Racedate.date == dt.date(2024, 1, 1)
where = extract('year', Racedate.date) == 2023
# query = select(Racedate.date).where(where)
query = select(Race, Racecourse, Jrarecord, HorseResult, Payback).outerjoin_from(Race, Jrarecord)\
.outerjoin(Racecourse)\
.outerjoin(Payback)\
.outerjoin(HorseResult)
Session = sessionmaker(bind=engine, future=True)
with Session() as session:
    # record = session.query(Racedate).first()
    record = session.execute(query).first()
    # records = session.scalars(query).all()

print(len(record), record)
# %%
