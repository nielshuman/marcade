import time
from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess, is_open

gamesServer = DingesServer('games', 8200)
gamesServer.start()

kiosk = kiosk_driver()

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game):
    print('Launching game', game)
    kiosk.get(gamesServer.url + game)

menuServer.start()

kiosk.get(menuServer.url + 'index.html')
# time.sleep(1)
# kiosk.get('')

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed')
gamesServer.stop()
menuServer.stop()