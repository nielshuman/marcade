import time
from serve2 import DingesServer
from chromium import kiosk_driver, kiosk_subprocess

print('Launching chrome...')
kiosk = kiosk_driver()
print('Launching menu...')


menu = DingesServer('menu', 8000, socketio=True)
@menu.socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    kiosk.get('chrome://gpu/')

menu.start()
kiosk.get(menu.url)

gunwizard = DingesServer('games/gunwizard', 8005)
gunwizard.start()

# pkiosk = kiosk_subprocess(menu.url, gunwizard.url)
# kiosk.get('chrome://gpu/')

# while pkiosk.poll() is None:
#     print("Process is running.")
#     time.sleep(1)


# gunwizard.stop()
# menu.stop()