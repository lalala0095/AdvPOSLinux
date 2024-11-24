import os
from flask_pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')  # Use 'default-secret-key' as fallback
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/mydb')  # Fallback to local Mongo URI
    mongo = MongoClient(MONGO_URI)
    db = mongo['adv_sop']

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
