import requests
import os

def matrix_notif(tpe, record, data, user):
    message = tpe + '\n-----\n' + str(record) + '\n-----\n' + str(data) + '\n-----\n' + user.username
    body = {
        "text": message,
        "format": "plain",
        "displayName": "Tankobon Notif"
    }
    requests.post(os.environ['TANKOBON_NOTIF'], json=body)