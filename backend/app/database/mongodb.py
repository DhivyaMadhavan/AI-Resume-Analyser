from pymongo import MongoClient
from app.config import settings

client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client[settings.DATABASE_NAME]

resume_collection = db["resume_analysis"]
matching_collection = db["jd_matching"]
jobs_collection = db["jobs"]
