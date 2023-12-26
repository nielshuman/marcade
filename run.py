import time
from serve2 import DingesServer
from chromium import open_kiosk

menu = DingesServer('menu', 8000)
menu.start()

gunwizard = DingesServer('games/gunwizard', 8005)
gunwizard.start()


pkiosk = open_kiosk(menu.url, gunwizard.url)

while pkiosk.poll() is None:
    print("Process is running.")
    time.sleep(1)

gunwizard.stop()
menu.stop()

open_kiosk('https://fallingfalling.com')