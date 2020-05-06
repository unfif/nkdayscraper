from pymongo import MongoClient
from bson.json_util import loads
import json
# import datetime as dt

mongos = [
    MongoClient('mongodb://localhost:27017/'),
    MongoClient('mongodb+srv://undo5:marehito@mongui-t1cam.gcp.mongodb.net/')
]

def f2j(f): return loads(json.dumps(json.load(f)))

for mongo in mongos:
    db = mongo.netkeiba
    clct = db.horseresults

    clct.drop()#delete_many({})
    with open('results02.json', encoding='UTF8') as f:
        clct.insert_many(f2j(f))

    # mongo.close


# db = mg.testdb
# clct = db.testclct
#
# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": dt.datetime.utcnow()}
# result01 = clct.insert_one(post)
#
# posts = [{"author": "Mike",
#           "text": "Another post!",
#           "tags": ["bulk", "insert"],
#           "date": dt.datetime(2009, 11, 12, 11, 14)},
#          {"author": "Eliot",
#           "title": "MongoDB is fun",
#           "text": "and pretty easy too!",
#           "date": dt.datetime(2009, 11, 10, 10, 45)}]
# result02 = clct.insert_many(posts)
#
# clct.find_one()
# for doc in clct.find(): print(doc)
