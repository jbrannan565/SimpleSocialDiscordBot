import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
MONGO_ADDR = os.getenv('MONGO_ADDR')
MONGO_PORT = os.getenv('MONGO_PORT')

if MONGO_ADDR and MONGO_PORT:
    client = MongoClient(MONGO_ADDR, MONGO_PORT)
else:
    client = MongoClient()


db = client.simp_bot_db