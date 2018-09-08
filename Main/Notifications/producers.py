import redis

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


def notif(kind, user, *args, **kwargs):
    if kind == 'like':
        pass
    elif kind == 'post':
        p = kwargs.get('post')
        conn.rpush('post', user + ' ' + p)
    elif kind == 'followrequest':
        pass
