from sqlalchemy import create_engine, select, update, delete, between, extract
from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Race, HorseResult, Racedates
import datetime as dt
from dotenv import dotenv_values
from pprint import pprint

config = dotenv_values('.env')
DATABASE_URL = config['DATABASE_URL']
engine = create_engine(DATABASE_URL, echo=True, future=True)
# drop_table(engine, horseresults)
# Base.metadata.create_all(engine)
where = between(
    Racedates.date,
    dt.date(2023, 3, 31),
    dt.date(2023, 4, 9)
)
where = Racedates.date == dt.date(2024, 1, 1)
where = extract('year', Racedates.date) == 2023
query = select(Racedates.date).where(where)
rows = [
    Racedates(date=dt.date(2024, 1, 1)),
    Racedates(date=dt.date(2024, 1, 5)),
]
query = select(Race).join(HorseResult.race)
query = select(Race, HorseResult).outerjoin(HorseResult)
# up_query = update(
Session = sessionmaker(bind=engine, future=True)
with Session() as session:
    session.add_all(rows)
    # record = session.query(Racedates).first()
    records = session.execute(query).first()
    # records = session.scalars(query).all()
    session.execute(delete(Racedates).where(where))
    # session.commit()

    # for record in records:
    #     print(record)

print(records)
