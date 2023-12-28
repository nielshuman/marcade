from multiprocessing import Process
import time

a = 'foo'

def test():
    while True:
        print(a)
        time.sleep(1)

p = Process(target=test)
p.start()

time.sleep(3)
a = 'bar'