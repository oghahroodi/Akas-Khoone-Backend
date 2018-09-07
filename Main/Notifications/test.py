from producers import notif,connect
import time
connect()
i = 0
while(True):
    i += 1
    notif('post', 1)
    time.sleep(1)