import time
from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess

print('Launching chrome...')
kiosk = kiosk_driver()
print('Launching menu...')

gunwizard = DingesServer('games/gunwizard', 8001, socketio=False)
gunwizard.start()
print('Tarp!')
menu = DingesServer('menu', 7583, socketio=True)

@menu.socketio.on('launch_game')
def launch_game(game):
    game = DingesServer(f'games/{game}', 8004)
    game.start()
    kiosk.get(game.url)

menu.start()
kiosk.get(menu.url + 'arcade-menu.html')
# Your existing code here


# pkiosk = kiosk_subprocess(menu.url, gunwizard.url)
# kiosk.get('chrome://gpu/')

# while pkiosk.poll() is None:
#     print("Process is running.")
#     time.sleep(1)