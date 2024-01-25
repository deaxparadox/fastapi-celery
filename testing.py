import threading
from time import sleep

def lets_sleep(d):
    sleep(d)
    
ts = [
    threading.Thread(target=lets_sleep, args=(4, )) for _ in range(4)
]
for t in ts: t.start()
for t in ts: t.join()