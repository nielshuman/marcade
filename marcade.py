import os
import sys

# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import time
from serve2 import DingesServer
from kiosk import kiosk_driver, is_open
from util import play_sound, AntimicroX, get_game_by_id
try:
    import gpiozero
except:
    gpiozero = None

gamesServer = DingesServer('games', 8200)

if len(sys.argv) > 1:
    if sys.argv[1] == '-s':
        print('Serve only mode')
        gamesServer.serve()
        sys.exit(0)

gamesServer.start()

antimciroX = AntimicroX('empty')
antimciroX.start()

kiosk = kiosk_driver()

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game_id):
    print('Launching game', game_id)
    game = get_game_by_id(game_id)
    kiosk.get(gamesServer.url + game['path'])
    try:
        antimciroX.change_profile(game['profile'])
    except KeyError:
        antimciroX.change_to_default()

def coin_inserted():
    print('Coin inserted')
    play_sound('audio/coin.mp3')
    kiosk.get(menuServer.url + 'select.html')
    antimciroX.change_profile('enter')

def expire():
    print('Time expired')
    kiosk.get(menuServer.url + 'coin.html')
    antimciroX.change_profile('empty')


play_sound('audio/start.wav')
menuServer.start()
kiosk.get(menuServer.url + 'coin.html')

if gpiozero:
    coinListener = gpiozero.Button(21)
    coinListener.when_pressed = coin_inserted
    print('Listening for coin')
else:
    print('Not listening for coin')
    time.sleep(5)
    coin_inserted()

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed, stopping servers and AntimicroX')
gamesServer.stop()
menuServer.stop()
antimciroX.stop()