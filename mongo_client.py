from pymongo import MongoClient

# Direct MongoDB URI
client = MongoClient("mongodb://mongodb.database.svc.cluster.local:27017/")
db = client["crud"]
collection = db["submitted_messages"]

def save_to_mongo(message):
    collection.insert_one(message)
