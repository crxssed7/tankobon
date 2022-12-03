import requests
import pymongo
from tankobon.settings import TANKOBON_LOGS
from libgravatar import Gravatar


def get_user_image(email) -> str:
    g = Gravatar(email)
    image = g.get_image(default="retro")
    return image


def mongo_log(tpe, record_name, data, user):
    client = pymongo.MongoClient(TANKOBON_LOGS)
    db = client.TankobonLogs
    record = {"type": tpe, "record_name": record_name, "data": data, "user": user}
    db.logs.insert_one(record)
