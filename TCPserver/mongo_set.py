import pymongo
import datetime
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
print(mongo_client.server_info())  # 判断是否连接成功
mongo_db = mongo_client['TouchOperation']
mongo_collection = mongo_db['Touch2Server']


info = {
    'name': 'Zarten',
    'text': 'Inserting a Document',
    'tags': ['a', 'b', 'c'],
    'date': datetime.datetime.now()
}
mongo_collection.insert_one(info)
last_one= [i for i in mongo_collection.find({'name':'Zarten'}).sort('_id',-1).limit(1)]
# print(mongo_collection.insert_one(info))
coll_names = mongo_db.list_collection_names(session=None)
print(last_one[0]['date'])
print(coll_names)
