import time
from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess

print('Launching chrome...')
kiosk = kiosk_driver()
print('Launching menu...')

menu = DingesServer('menu', 8000, socketio=True)

@menu.socketio.on('launch_game')
def poep(game):
    game = DingesServer(f'games/{game}', 6003)
    game.start()
    kiosk.get(game.url)

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