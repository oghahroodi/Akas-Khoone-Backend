import json
import re

import redis
import string
import random
import requests


def contactState(index):
    if index == 0:
        return "friend"
    if index == 1:
        return "registered"
    if index == 2:
        return "notregistered"
    if index == 3:
        return "requested"

def makeRelation(following,followed):
    return {'userFollowing': following, 'userFollowed':followed}

def makeMail(code):
    return "کد ورودی برای فراموشی رمز عبور:\n" + code


def email(username):
    red = redis.StrictRedis(
        host='localhost', port=6379, password='', charset="utf-8", decode_responses=True)
    random_token = ''.join([random.choice(string.ascii_uppercase + string.ascii_uppercase) for _ in range(50)])
    red.hmset(random_token, {"email": username})
    link = ("http://127.0.0.1:8000/verification/%s/" % random_token)
    data = {
        "to": username,
        "body": "سلام \n برای کامل شدن ثبت نام روی لینک زیر کلیک کنید \n" + link,
        "subject": "تایید ایمیل"
    }

    requests.post(url="http://192.168.10.66:80/api/send/mail", data=json.dumps(data),
                  headers={"agent-key": "OOmIZh9U6m", "content-type": "application/json"})


