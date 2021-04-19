from elasticsearch import Elasticsearch, helpers
from sqlalchemy import create_engine
from sqlalchemy.future.orm import Session
import settings

es = Elasticsearch(settings.ES_URL)
engine = create_engine(settings.DATABASE_URL, echo=False, future=True)

def makeData(tablename, dictList):
    for record in dictList:
        yield {"_index": tablename, "_source": record}

def bulkInsertTable(tablename, session):
    if es.indices.exists(index=tablename): es.indices.delete(index=tablename)
    jsonArray = session.execute(f'SELECT array_to_json(array_agg({tablename})) FROM {tablename}')
    print(jsonArray)
    print(type(jsonArray))
    dictList = list(jsonArray)[0].array_to_json
    helpers.bulk(es, makeData(tablename, dictList))

indices = ['jrarecords', 'races', 'horseresults', 'paybacks']

with Session(engine, future=True) as session:
    for index in indices:
        bulkInsertTable(index, session)
