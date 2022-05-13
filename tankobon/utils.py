import requests
import os
import pymongo

def matrix_notif(tpe, record, data, user):
    message = tpe + '\n-----\n' + str(record) + '\n-----\n' + str(data) + '\n-----\n' + user.username
    body = {
        "text": message,
        "format": "plain",
        "displayName": "Tankobon Notif"
    }
    requests.post(os.environ['TANKOBON_NOTIF'], json=body)

def mongo_log(tpe, record_name, data, user):
    client = pymongo.MongoClient(os.environ['TANKOBON_LOGS'])
    db = client.TankobonLogs
    record = {
        'type': tpe,
        'record_name': record_name,
        'data': data,
        'user': user
    }
    db.logs.insert_one(record)