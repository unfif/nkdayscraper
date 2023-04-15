from sqlalchemy import create_engine, select, update, delete, between, extract
from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Race, HorseResult, Racedate
import datetime as dt
from dotenv import dotenv_values
from pprint import pprint

config = dotenv_values('.env')
DATABASE_URL = config['DATABASE_URL']
engine = create_engine(DATABASE_URL, echo=True, future=True)
# drop_table(engine, horseresults)
# Base.metadata.create_all(engine)
where = between(
    Racedate.date,
    dt.date(2023, 3, 31),
    dt.date(2023, 4, 9)
)
where = Racedate.date == dt.date(2024, 1, 1)
where = extract('year', Racedate.date) == 2023
query = select(Racedate.date).where(where)
rows = [
    Racedate(date=dt.date(2024, 1, 1)),
    Racedate(date=dt.date(2024, 1, 5)),
]
query = select(Race).join(HorseResult.race)
query = select(Race, HorseResult).outerjoin(HorseResult).order_by(
	Race.date,
	Race.place,
	Race.racenum,
	HorseResult.ranking,
)
# up_query = update(
Session = sessionmaker(bind=engine, future=True)
with Session() as session:
    session.add_all(rows)
    # record = session.query(Racedate).first()
    records = session.execute(query).first()
    # records = session.scalars(query).first()
    session.execute(delete(Racedate).where(where))
    # session.commit()

    # for record in records:
    #     print(record)

print(records)
