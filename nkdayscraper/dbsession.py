from sqlalchemy.orm import sessionmaker
from models import nkdayraces, db_connect#, create_table

engine = db_connect(True)
# drop_table(engine, nkdayraces)
# create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()
records = session.query(nkdayraces).all()
# session.commit()
for record in records: print(record)
