from datetime import datetime
from bson.objectid import ObjectId
from flask import current_app
import os
from flask_pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.adv_sop

def event_logging(event_var, user_id, account_id, object_id, old_doc, new_doc, error):
    log_entry = {
        "date_inserted": datetime.now(),
        "event": event_var,
        "user_id": user_id,
        "account_id": account_id,
        "object_id": ObjectId(object_id),
        "old_doc": old_doc,
        "new_doc": new_doc,
        "error": error
    } 
    log_result = db.logs.insert_one(log_entry)