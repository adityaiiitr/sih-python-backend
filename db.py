from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv() 

def createConnection(collection="TEST"):
    mongo_url = os.getenv('MONGO_URI')
    database_name = os.getenv('DATABASE_NAME')                 

    client = MongoClient(mongo_url)

    db = client[database_name]

    collection = db[collection]

    return collection

