import requests
import pymongo
from tankobon.settings import TANKOBON_LOGS

def mongo_log(tpe, record_name, data, user):
    client = pymongo.MongoClient(TANKOBON_LOGS)
    db = client.TankobonLogs
    record = {
        'type': tpe,
        'record_name': record_name,
        'data': data,
        'user': user
    }
    db.logs.insert_one(record)