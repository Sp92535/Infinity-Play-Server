import os
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFSBucket

load_dotenv()

try:
    client = MongoClient(os.getenv('MONGO_HOST'))
    db = client[os.getenv('MONGO_DB')]
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")
    db = None