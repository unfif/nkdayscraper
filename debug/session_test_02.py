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
where = extract('year', Racedate.date) == 2023
query = select(Race)
Session = sessionmaker(bind=engine, future=True)
with Session() as session:
    # record = session.query(Racedate).first()
    record = session.execute(query).first()
    # records = session.scalars(query).all()

print(len(record), record)
# %%
