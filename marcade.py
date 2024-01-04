import os
import time

# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess, is_open
from util import play_sound
try:
    import gpiozero
except:
    gpiozero = None


gamesServer = DingesServer('games', 8200)
gamesServer.start()

kiosk = kiosk_driver()

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game):
    print('Launching game', game)
    kiosk.get(gamesServer.url + game)

menuServer.start()
kiosk.get(menuServer.url + 'coin.html')
play_sound('audio/start.wav')

def coin_inserted():
    print('Coin inserted')
    play_sound('audio/coin.mp3')
    kiosk.get(menuServer.url + 'select.html')

if gpiozero:
    coinListener = gpiozero.Button(21)
    coinListener.when_pressed = coin_inserted
    print('Listening for coin')
else:
    print('Not listening for coin')

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed')
gamesServer.stop()
menuServer.stop()