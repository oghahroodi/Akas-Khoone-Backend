from django.shortcuts import render
import redis
from django.http import HttpResponse

def test(request):
    try:
        conn = redis.StrictRedis(
            host='localhost',
            port=6379,
            password='')
        print (conn)
        conn.ping()
        print ('Connected!')
    except Exception as ex:
        print ('Error:', ex)
        exit('Failed to connect, terminating.')
    return HttpResponse("krk")



