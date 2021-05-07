from sqlalchemy.orm import sessionmaker
from ..models import horseresults, db_connect#, Base

engine = db_connect(echo=True)
# drop_table(engine, horseresults)
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, future=False)
session = Session()
records = session.query(horseresults).all()
# session.commit()
for record in records: print(record)
