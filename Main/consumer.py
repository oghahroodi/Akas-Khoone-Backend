import json

import redis
import requests


def connectToRedis():
    try:
        global connRedis
        connRedis = redis.StrictRedis(
            host='localhost', port=6379, password='', charset="utf-8", decode_responses=True)
#        print(connRedis)
#        connRedis.ping()
#        print('Connected!')
    except Exception as ex:
        #        print('Error:', ex)
        exit()


connectToRedis()
while(True):

    task = connRedis.blpop('notif')
    notification = json.loads(task[1])
    print("requests:", notification)
    url = "http://127.0.0.1:8000/notification/"
    requests.post(url, data=notification)
