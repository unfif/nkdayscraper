from sqlalchemy import create_engine, MetaData

engine = create_engine("postgresql+psycopg2://postgres:marehito@localhost:5432/postgres")

print(engine.table_names())
meta = MetaData(engine)
meta.reflect(bind=engine)

print(meta.tables.keys())
# con = engine.connect()
# res = con.execute("SELECT * FROM NKTHEDAYRACES")
# for row in res: print(row)

# con.close()
