from pymongo import MongoClient
from app.config import settings

# Create a single MongoDB client for the entire application
client = MongoClient(settings.MONGO_URI)

# Select the database
db = client[settings.DATABASE_NAME]