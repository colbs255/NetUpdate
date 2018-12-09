from NetUpdate import NetUpdate
import time

def time_stamp():
    timestamp = time.time()
    return str(timestamp)

updater = NetUpdate(port=8080)
updater.callback = time_stamp

updater.start()
time.sleep(20)
print('ending')
updater.end()

time.sleep(10)

print('starting again')
updater._port_number = 8081
updater.start()
time.sleep(10)
updater.end()
print('should have closed')
while True:
    continue