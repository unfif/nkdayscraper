from sqlalchemy import create_engine
from scrapy.utils.project import get_project_settings

engine = create_engine(get_project_settings().get('DATABASE_URL'))

con = engine.connect()
res = con.execute("SELECT * FROM nkdayraces")
for row in res: print(row)

con.close()
