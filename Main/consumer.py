import sqlite3
import redis
from sqlite3 import Error
import time
from django.conf import settings
import os
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Main.settings"
)
django.setup()
from Notification.models import *
from Post.models import *
from Account.models import *
from Social.models import *


def connectToRedis():
    try:
        global connRedis
        connRedis = redis.StrictRedis(
            host='localhost', port=6379, password='', charset="utf-8", decode_responses=True)
        print(connRedis)
        connRedis.ping()
        print('Connected!')
    except Exception as ex:
        print('Error:', ex)
        exit('Failed to connect, terminating.')


connectToRedis()
while(True):

    user = connRedis.lpop('post')
    user = int(user)
    print(user)
    if user != None:
        for i in Relation.objects.all().filter(userFollowed=user):
            p = PostNotif(user=i.userFollowing)
            p.save()
    time.sleep(10)
