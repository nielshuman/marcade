import time
from serve2 import DingesServer
from chromium import kiosk_driver, kiosk_subprocess

menu = DingesServer('menu', 8000)
menu.start()

gunwizard = DingesServer('games/gunwizard', 8005)
gunwizard.start()


# pkiosk = kiosk_subprocess(menu.url, gunwizard.url)
kiosk = kiosk_driver(menu.url)
time.sleep(5)
kiosk.get('chrome://gpu/')
time.sleep(10)

# while pkiosk.poll() is None:
#     print("Process is running.")
#     time.sleep(1)


gunwizard.stop()
menu.stop()