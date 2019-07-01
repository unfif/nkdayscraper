from sqlalchemy.orm import sessionmaker
from models import nkthedayraces, db_connect#, create_table
#import pandas as pd

engine = db_connect(True)
# drop_table(engine, nkthedayraces)
# create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()
nkthedayraces = session.query(nkthedayraces).all()
# session.commit()
for nkthedayrace in nkthedayraces:
    print(nkthedayrace)
