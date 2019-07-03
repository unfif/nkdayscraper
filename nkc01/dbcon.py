from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:marehito@localhost:5432/postgres")

con = engine.connect()
res = con.execute("SELECT * FROM NKTHEDAYRACES")
for row in res: print(row)

con.close()
