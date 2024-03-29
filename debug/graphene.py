from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from nkdayscraper.models import Race, HorseResult# , Racedate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from dotenv import dotenv_values
from pprint import pprint

config = dotenv_values('.env')
DATABASE_URL = config['DATABASE_URL']
engine = create_engine(DATABASE_URL, echo=False, future=True)

class RaceSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Race
		include_fk = True
		# include_relationships = True
		load_instance = True

class HorseResultSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = HorseResult
		include_fk = True
		# include_relationships = True
		load_instance = True

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

class HorseResultGql(SQLAlchemyObjectType):
	class Meta:
		model = HorseResult
		# use `only_fields` to only expose specific fields ie "name"
		# only_fields = ("name",)
		# use `exclude_fields` to exclude specific fields ie "last_name"
		# exclude_fields = ("last_name",)

class Query(graphene.ObjectType):
	horseresults = graphene.List(HorseResultGql)

	def resolve_horseresults(self, info):
		query = HorseResult.get_query(info)  # SQLAlchemy query
		return query.all()

schema = graphene.Schema(query=Query)

query = '''
	query {
		horseresults {
			raceid,
			horsename
		}
	}
'''

race_schema = RaceSchema()
# pprint(race_schema)
horseresult_schema = HorseResultSchema()

query = select(Race, HorseResult).outerjoin(
	HorseResult
).where(
	HorseResult.ranking != None
).order_by(
	Race.date,
	Race.place,
	Race.racenum,
	HorseResult.ranking,
)
Session = sessionmaker(bind=engine, future=True)
with Session() as session:
	race = session.execute(query).first()
	# race = session.scalars(query).first()

	# pprint(race)

	# dump_data = race_schema.dump(race[0])
	# pprint(dump_data)
	# load_data = race_schema.load(dump_data, session=session)
	# pprint(load_data)

	# dump_data = horseresult_schema.dump(race[1])
	# pprint(dump_data)
	# load_data = horseresult_schema.load(dump_data, session=session)
	# pprint(load_data)

	result = schema.execute(query, context_value={'session': session})
	print(result)
