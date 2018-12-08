from NetUpdate import NetUpdate
import time

def time_stamp():
    timestamp = time.time()
    return str(timestamp)

updater = NetUpdate(port=8081)
updater.callback = time_stamp
updater.start()
time.sleep(20)
updater.end()
while True:
    continue