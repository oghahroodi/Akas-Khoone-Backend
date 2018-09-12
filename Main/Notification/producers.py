import redis
from .utilities import makeJsonNotif
from Social.models import *
import json


def connect():
    try:
        global conn
        conn = redis.StrictRedis(
            host='localhost', port=6379, password='', charset="utf-8", decode_responses=True)
        print(conn)
        conn.ping()
        print('Connected!')
    except Exception as ex:
        print('Error:', ex)
        exit('Failed to connect, terminating.')


def notif(kind, doer, entity, date):
    if kind == 'like':
        jsonDic = makeJsonNotif(kind="like", doer=str(
            doer), entity=str(entity), date=str(date))
        jsonStr = json.dumps(jsonDic)
        conn.rpush('notif', jsonStr)
    elif kind == 'comment':
        jsonDic = makeJsonNotif(kind="comment", doer=str(
            doer), entity=str(entity), date=str(date))
        jsonStr = json.dumps(jsonDic)
        conn.rpush('notif', jsonStr)
