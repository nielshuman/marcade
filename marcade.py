import os
import sys
import signal
import argparse

# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# save current PID to temp file
with open('.marcade.pid', 'w') as f:
    f.write(str(os.getpid()))

import time
from serve2 import DingesServer
from kiosk import kiosk_driver, is_open
from util import get_game_by_id
from antimicroX import AntimicroX
# from sound import play_sound, play_music, stop_music
try:
    import gpiozero
except ImportError:
    gpiozero = None

from audio import Sound, Music, close

def send_stop_music_signal():
    print('Sending stop music signal')
    with open('.marcade.pid', 'r') as f:
        os.kill(int(f.read()), signal.SIGUSR2)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serve', action='store_true', help='Serve only mode')
parser.add_argument('-w', '--windowed', action='store_true', help='Windowed mode')
args = parser.parse_args()

gamesServer = DingesServer('games', 8200)

if args.serve:
    print('Serve only mode')
    gamesServer.serve()
    sys.exit(0)

gamesServer.start()

antimciroX = AntimicroX(default_profile='empty', profiles_directory='profiles')
antimciroX.start()

kiosk = kiosk_driver(windowed=args.windowed)

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
    send_stop_music_signal()


def coin_inserted():
    print('Coin inserted')
    Sound.coin.play()
    go_to_menu()

def expire():
    print('Time expired')
    kiosk.get(menuServer.url + 'insert_coin.html')
    antimciroX.change_profile('empty')

def go_to_menu(*args):
    print('Returning to menu')
    kiosk.get(menuServer.url + 'select.html')
    Music.play(Music.menu)
    antimciroX.change_profile('empty')

Sound.start.play()
menuServer.start()
kiosk.get(menuServer.url + 'insert_coin.html')
signal.signal(signal.SIGUSR1, go_to_menu)
signal.signal(signal.SIGUSR2, Music.stop)

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
os.remove('.marcade.pid')
close()