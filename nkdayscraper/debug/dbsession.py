from sqlalchemy.orm import sessionmaker
from models import horseresults, db_connect#, create_tables

engine = db_connect(echo=True)
# drop_table(engine, horseresults)
# create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
records = session.query(horseresults).all()
# session.commit()
for record in records: print(record)
