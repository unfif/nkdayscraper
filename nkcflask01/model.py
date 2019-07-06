from flask_sqlalchemy import SQLAlchemy
import pandas as pd

db = SQLAlchemy()
engine = db.create_engine("postgresql+psycopg2://postgres:marehito@localhost:5432/postgres", echo=False)
meta = db.MetaData()
meta.reflect(bind=engine)
table = meta.tables['nkthedayraces']
cols = table.c

def init_db(app):
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:marehito@localhost:5432/postgres"#?charset=utf8"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)

class ToDoItem(db.Model):
  __tablename__ = "todoitems"
  item_id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False, default=False)
  done = db.Column(db.Boolean, nullable=False)

class NkTheDayRaces():
    def getRaces():
        con = engine.connect()
        sql = table.select().where(cols.raceid.like('2019030202__')).where(cols.placenum.in_([1, 2, 3])).order_by(cols.racenum).order_by(cols.placenum)
        racesdf = pd.read_sql_query(sql, con)
        con.close()
        return racesdf

class ToDoList:
  def add(self, title):
    item = ToDoItem(title=title, done=False)
    db.session.add(item)
    db.session.commit()

  def delete(self, item_id):
    item = ToDoItem.query.filter_by(item_id=item_id).first()
    db.session.delete(item)
    db.session.commit()

  def get_all(self):
    items = ToDoItem.query.all()
    return items

  def delete_doneitem(self):
    ToDoItem.query.filter_by(done=True).delete()
    db.session.commit()

  def update_done(self, items):
    for item in self.get_all():
      if item.item_id in items:
        item.done = True
      else:
        item.done = False
    db.session.commit()
