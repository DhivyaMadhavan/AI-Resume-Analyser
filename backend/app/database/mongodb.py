from pymongo import MongoClient
from app.config import settings
import time


start = time.perf_counter()

client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

print(
    "Mongo client creation:",
    time.perf_counter() - start
)


start = time.perf_counter()

db = client[settings.DATABASE_NAME]

resume_collection = db["resume_analysis"]
matching_collection = db["jd_matching"]

print(
    "Mongo collection setup:",
    time.perf_counter() - start
)
