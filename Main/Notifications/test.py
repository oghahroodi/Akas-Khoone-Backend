from producers import notif, connect
import time
connect()

import json
from redis import StrictRedis

red = StrictRedis()

i = 0
while(True):

    red.rpush('command-queue', json.dumps({
        'type': 1,
        'payload': {
            'pk': 13
        }
    }))


    notif('post', '1', post='13')
    # time.sleep(0.01)


while True:
    command = json.loads(red.blpop('command-queue'))
    ctype = command['type']

    if ctype == 1:
        post_id = Post.objects.get(pk=payload['pk'])
        #...