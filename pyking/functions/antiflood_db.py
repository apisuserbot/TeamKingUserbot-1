import json
from .. import udB


def get_flood():
    n = [json.loads(json.dumps(udB.get("ANTIFLOOD")))]
    return n[0]


def set_flood(chat_id, limit):
    omk = get_flood()
    omk.update({str(chat_id): str(limit)})
    udB.set("ANTIFLOOD", str(omk))
    return True


def get_flood_limit(chat_id):
    omk = get_flood()
    if str(chat_id) in omk.keys():
        return omk[str(chat_id)]
    else:
        return False
