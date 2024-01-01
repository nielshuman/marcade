import time

from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess, is_open
from util import play_sound, listen_for_coin

gamesServer = DingesServer('games', 8200)
gamesServer.start()

kiosk = kiosk_driver()

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game):
    print('Launching game', game)
    kiosk.get(gamesServer.url + game)

menuServer.start()
# time.sleep(3)
kiosk.get(menuServer.url + 'coin.html')

def coin_inserted():
    print('Coin inserted')
    play_sound('audio/coin.mp3')
    kiosk.get(menuServer.url + 'select.html')

# listen_for_coin(17, coin_inserted)

# time.sleep(5)
# coin_inserted()

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed')
gamesServer.stop()
menuServer.stop()