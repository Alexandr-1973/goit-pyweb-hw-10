from pymongo import MongoClient



def get_mongodb():
    client = MongoClient("mongodb://localhost")
    db = client.hw10
    return db
