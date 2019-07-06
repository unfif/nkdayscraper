from sqlalchemy import create_engine, MetaData, select, and_, or_, not_
import pandas as pd

engine = create_engine("postgresql+psycopg2://postgres:marehito@localhost:5432/postgres", echo=False)
# print(engine.table_names())
# meta = MetaData(engine)
meta = MetaData()
meta.reflect(bind=engine)
# print(meta.tables.keys())
table = meta.tables['nkthedayraces']
cols = table.c
# print(cols.keys())
con = engine.connect()
sql = table.select().where(cols.raceid.like('2019030202__')).where(cols.placenum.in_([1, 2, 3])).order_by(cols.racenum).order_by(cols.placenum)
# sql = "SELECT * FROM nkthedayraces AS nk "
# sql += "WHERE nk.raceid LIKE '2019030202__' AND nk.placenum IN (1, 2, 3) "
# sql += "ORDER BY nk.racenum, nk.placenum"
pd.read_sql_query(sql, con)

con.close()
