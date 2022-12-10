import pymongo

from libgravatar import Gravatar

from tankobon.settings import TANKOBON_LOGS


def get_user_image(email) -> str:
    gravatar = Gravatar(email)
    image = gravatar.get_image(default="retro")
    return image


def mongo_log(tpe, record_name, data, user):
    client = pymongo.MongoClient(TANKOBON_LOGS)
    _db = client.TankobonLogs
    record = {"type": tpe, "record_name": record_name, "data": data, "user": user}
    _db.logs.insert_one(record)
