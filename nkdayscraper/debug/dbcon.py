from sqlalchemy import create_engine
from scrapy.utils.project import get_project_settings

engine = create_engine(get_project_settings().get('DATABASE_URL'), future=False)

with engine.connect() as conn:
    res = conn.execute("SELECT * FROM horseresults")
    for row in res: print(row)
