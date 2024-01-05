import os
# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import time
from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess, is_open
from util import play_sound, AntimicroX
try:
    import gpiozero
except:
    gpiozero = None

import yaml
with open('menu/games.yml') as f:
    games = yaml.load(f, Loader=yaml.FullLoader)

antimciroX = AntimicroX('empty')
antimciroX.start()
gamesServer = DingesServer('games', 8200)
gamesServer.start()

kiosk = kiosk_driver()

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game_id):
    print('Launching game', game_id)
    for g in games:
        if g['id'] == game_id:
            game = g
            break
    antimciroX.change_profile(game['profile'])
    kiosk.get(gamesServer.url + game['path'])

def coin_inserted():
    print('Coin inserted')
    play_sound('audio/coin.mp3')
    kiosk.get(menuServer.url + 'select.html')
    antimciroX.change_profile('enter')

if gpiozero:
    coinListener = gpiozero.Button(21)
    coinListener.when_pressed = coin_inserted
    print('Listening for coin')
else:
    print('Not listening for coin')

play_sound('audio/start.wav')
menuServer.start()
kiosk.get(menuServer.url + 'coin.html')

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed, stopping servers and AntimicroX')
gamesServer.stop()
menuServer.stop()
antimciroX.stop()