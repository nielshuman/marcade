import os
import sys
import argparse
from serve2 import DingesServer
import time

# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serve', action='store_true', help='Serve only mode')
parser.add_argument('-w', '--windowed', action='store_true', help='Windowed mode')
parser.add_argument('-c', '--no-coin', action='store_true', help='Do not listen for coin, insert coin on start')
parser.add_argument('-d', '--delay', action='store_true', help='start with a delay ')

args = parser.parse_args()

gamesServer = DingesServer('games', 8200)

if args.serve:
    print('Serve only mode')
    gamesServer.serve()
    sys.exit(0)


import signal
import time
try:
    import gpiozero
except ImportError:
    gpiozero = None
from kiosk import kiosk_driver, is_open
from util import get_game_by_id
from audio import Sound, Music, close
import controllers
# from sound import play_sound, play_music, stop_music

# save current PID to temp file
with open('.marcade.pid', 'w') as f:
    f.write(str(os.getpid()))

def send_stop_music_signal():
    with open('.marcade.pid', 'r') as f:
        os.kill(int(f.read()), signal.SIGUSR2)

gamesServer.start()

if args.delay:
    time.sleep(13)

kiosk = kiosk_driver(windowed=args.windowed)

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game_id):
    print('Launching game', game_id)
    send_stop_music_signal()
    game = get_game_by_id(game_id)
    kiosk.get(gamesServer.url + game.get('path', game['id']))
    controllers.P1.start(game.get('p1', 'default_1'))
    controllers.P2.start(game.get('p2', 'default_2'))

def coin_inserted():
    print('Coin inserted')
    Sound.coin.play()
    go_to_menu()

def expire():
    print('Time expired')
    kiosk.get(menuServer.url + 'insert_coin.html')
    # antimciroX.change_profile('empty')

def go_to_menu(*args):
    print('Going to menu')
    kiosk.get(menuServer.url + 'select.html')
    Music.play(Music.menu, fade_in=False)
    controllers.P1.start('menu')
    controllers.P2.stop()

Sound.start.play()
menuServer.start()
kiosk.get(menuServer.url + 'insert_coin.html')
signal.signal(signal.SIGUSR1, go_to_menu)
signal.signal(signal.SIGUSR2, Music.stop)

if gpiozero and not args.no_coin:
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
controllers.stop_all()
close()
os.remove('.marcade.pid')