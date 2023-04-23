# %%
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Race, HorseResult# , Racedate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from dotenv import dotenv_values
from pprint import pprint

config = dotenv_values('.env')
DATABASE_URL = config['DATABASE_URL']
engine = create_engine(DATABASE_URL, echo=False, future=True)

class RaceSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Race
    include_fk = True
    include_relationships = True
    load_instance = True

class HorseResultSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = HorseResult
    include_fk = True
    include_relationships = True
    load_instance = True
    race = fields.Nested(RaceSchema)

race_schema = RaceSchema()
# pprint(race_schema)
horseresult_schema = HorseResultSchema()
# HorseResult.__table__.c.keys()
# race_cols = [getattr(Race, col) for col in Race.__table__.c.keys()]
# print(race_cols)
# result_cols = [getattr(HorseResult, col) for col in HorseResult.__table__.c.keys()]
# print(result_cols)
query = select(
  Race, HorseResult
  # *race_cols, *result_cols
).outerjoin(
  HorseResult
).where(
  HorseResult.ranking != None,
  Race.date == '2023-04-16'
).order_by(
  Race.date,
  Race.place,
  Race.racenum,
  HorseResult.ranking,
)
Session = sessionmaker(bind=engine, future=True)
with Session() as session:
  # race = session.execute(query).first()
  # race = session.scalars(query).first()
  # pprint(race)
  results = session.execute(query).all()
  # results = session.scalars(query).all()
  # classes = [
  #   row[1].race = row[0]
  # for row in results]
  # print(classes[1])
  records = [
    HorseResult(
      **{
        **(horseresult_schema.dump(row[1])),
        **{'race': race_schema.dump(row[0])}
      }
    )
  for row in results]
  print(records[1])
  # dump_data = horseresult_schema.dump(records[1])
  # pprint(dump_data)
  # %%
  dump_data = race_schema.dump(results[0][0])
  pprint(dump_data)
  load_data = race_schema.load(dump_data, session=session)
  pprint(load_data)

  dump_data = horseresult_schema.dump(results[0][1])
  pprint(dump_data)
  load_data = horseresult_schema.load(dump_data, session=session)
  pprint(load_data)
