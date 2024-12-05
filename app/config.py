import os
from flask_pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/mydb')
    mongo = MongoClient(MONGO_URI)
    db = mongo['advpos']
    RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY', 'default-recaptcha-secret-key')
    RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY', 'default-recaptcha-site-key')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
