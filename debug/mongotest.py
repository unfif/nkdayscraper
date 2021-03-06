from pymongo import MongoClient
import datetime as dt

mongo = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
mongo = MongoClient('mongodb://localhost:27017/?serverSelectionTimeoutMS=30000')
mongo.server_selection_timeout
# mongo.wTimeoutMS
db = mongo.python
collection = db.test01
collection.drop()#delete_many({})

mongo = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=30000)
db = mongo.python
collection = db.test01

doc = {'raceid': '201906040511', 'place': '中山', 'racenum': 11, 'title': 'セントライト記念', 'coursetype': '芝', 'distance': 2200, 'courseinfo1': '右 外', 'weather': '曇', 'condition': '重', 'date': dt.datetime(2019, 9, 16, 15, 45), 'date': dt.date(2019, 9, 16), 'posttime': dt.time(15, 45), 'racegrade': '(国際)(指定)馬齢', 'starters': 18, 'addedmoneylist': [5400000, 2200000, 1400000, 810000, 540000], 'placenum': 18, 'postnum': 2, 'horsenum': 3, 'horsename': 'マテリ アルワールド', 'sex': '牡', 'age': 3, 'weight': 56.0, 'jockey': '木幡育', 'time': dt.time(0, 2, 13, 800000), 'margin': 'クビ', 'fav': 18, 'odds': 314.3, 'last3f': 36.7, 'positionlist': [14, 13, 15, 16], 'trainer': '中川', 'horseweight': 508, 'horseweightdiff': 2, 'requrl': 'https://race.netkeiba.com/?pid=race&id=p201906040511&mode=top'}

doc['date'] = dt.datetime.combine(doc['date'], dt.time())
doc['posttime'] = str(doc['posttime'])
doc['time'] = str(doc['time'])
collection.insert_one(doc)
collection.find_one({})

    # mongo.close


# db = mg.testdb
# collection = db.testclct
#
# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": dt.datetime.utcnow()}
# result01 = collection.insert_one(post)
#
# posts = [{"author": "Mike",
#           "text": "Another post!",
#           "tags": ["bulk", "insert"],
#           "date": dt.datetime(2009, 11, 12, 11, 14)},
#          {"author": "Eliot",
#           "title": "MongoDB is fun",
#           "text": "and pretty easy too!",
#           "date": dt.datetime(2009, 11, 10, 10, 45)}]
# result02 = collection.insert_many(posts)
#
# collection.find_one()
# for doc in collection.find(): print(doc)
