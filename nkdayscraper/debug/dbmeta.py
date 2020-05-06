from sqlalchemy import create_engine, MetaData, select, and_, or_, not_
from scrapy.utils.project import get_project_settings
import pandas as pd

engine = create_engine(get_project_settings().get('DATABASE_URL'), echo=False)
# print(engine.table_names())
# meta = MetaData(engine)
meta = MetaData()
meta.reflect(bind=engine)
# print(meta.tables.keys())
table = meta.tables['horseresults']
cols = table.c
# print(cols.keys())
con = engine.connect()
sql = table.select().where(cols.raceid.like('2019030203__')).where(cols.placenum.in_([1, 2, 3])).order_by(cols.racenum).order_by(cols.placenum)
# sql = "SELECT * FROM horseresults AS nk "
# sql += "WHERE nk.raceid LIKE '2019030202__' AND nk.placenum IN (1, 2, 3) "
# sql += "ORDER BY nk.racenum, nk.placenum"
racesdf = pd.read_sql_query(sql, con)
racesdf.columns

for index, row in racesdf.iterrows():
    if index == 0:
        sr = row
        for column in row:
            print(type(column))

sr
type(sr)
sr.items()
for index, val in sr.items():
    print(index, val)

for index, val in sr.to_dict().items:
    print(index, val)

con.close()
