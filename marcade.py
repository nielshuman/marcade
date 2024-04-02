import os
import sys
import argparse
from serve2 import DingesServer
import time
import signal
import time
import subprocess
from math import inf

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


EXPIRERY_TIME = -1
from settings import COIN_TIME_VALUE, SKIP_BOOT_ANIMATION

try:
    import gpiozero
except ImportError:
    gpiozero = None
from kiosk import kiosk_driver, is_open
from util import get_game_by_id
from audio import Sound, Music, Voice, close
import controllers
# from sound import play_sound, play_music, stop_music

# save current PID to temp file
with open('.marcade.pid', 'w') as f:
    f.write(str(os.getpid()))

def send_stop_music_signal():
    with open('.marcade.pid', 'r') as f:
        os.kill(int(f.read()), signal.SIGUSR2)

gamesServer.start()

if args.delay and not SKIP_BOOT_ANIMATION:
    time.sleep(17)

kiosk = kiosk_driver(windowed=args.windowed)

menuServer = DingesServer('menu', 8201, socketio=True)

@menuServer.socketio.on('launch_game')
def launch_game(game_id):
    print('Launching game', game_id)
    send_stop_music_signal()
    game = get_game_by_id(game_id)
    if not game:
        print('Game not found')
        return

    game_type = game.get('type', 'web')
    game_path = game.get('path', game['id'])
    print('gametype: ' + game_type)
    if game_type == 'web':
        kiosk.get(gamesServer.url + game_path)
    elif game_type == 'exec':
        kiosk.get(gamesServer.url + 'wait.png')
        game_process = subprocess.Popen(game['command'], cwd=os.path.join('games', game_path))
        with open('.game.pid', 'w') as f:
            f.write(str(game_process.pid))

    # controllers.P1.start(game.get('p1', 'default_1'))
    # controllers.P2.start(game.get('p2', 'default_2'))

    if 'p1' in game:
        controllers.P1.start(game['p1'])
    if 'p2' in game:
        controllers.P2.start(game['p2'])

def coin_inserted():
    print('Coin inserted')
    Sound.coin.play()
    global EXPIRERY_TIME
    currently_playing = (EXPIRERY_TIME > time.time())

    if currently_playing:
        EXPIRERY_TIME+= COIN_TIME_VALUE
    else:
        EXPIRERY_TIME = time.time() + COIN_TIME_VALUE
        go_to_menu()
    
    Voice.reset()
def expire():
    Voice.play(Voice.up)
    Sound.play(Sound.timeover)

    print('Time expired')
    global EXPIRERY_TIME
    EXPIRERY_TIME = -1

    kill_current_game()
    kiosk.get(menuServer.url + 'insert_coin.html')
    controllers.P1.start('menu')
    controllers.P2.stop()
    Music.stop()
    # antimciroX.change_profile('empty')

def kill_current_game():
    """Kill the current exec type game, if there is one running."""
    if os.path.exists('.game.pid'):
        with open('.game.pid', 'r') as f:
            try:
                os.kill(int(f.read()), signal.SIGTERM)
            except ProcessLookupError:
                pass

        os.remove('.game.pid')

def go_to_menu(*args):
    print('Going to menu')

    if EXPIRERY_TIME == -1:
        kiosk.get(menuServer.url + 'insert_coin.html')
        Music.stop()
        return

    kiosk.get(menuServer.url + 'select.html' + '#time_left=' + str(EXPIRERY_TIME - time.time()))
    Music.play(Music.menu, fade_in=False)

    kill_current_game()

    controllers.P1.start('menu')
    controllers.P2.stop()

def go_to_admin(*args):
    print('Going to admin')
    kiosk.get(menuServer.url + 'admin.html')
    global EXPIRERY_TIME
    EXPIRERY_TIME = -1

    Music.stop(fade=False)
    Music.play(Music.menu, fade_in=False)

    kill_current_game()

    controllers.P1.start('menu')
    controllers.P2.stop()

# Sound.start.play()
menuServer.start()
kiosk.get(menuServer.url + 'insert_coin.html')
signal.signal(signal.SIGUSR1, go_to_menu)
signal.signal(signal.SIGUSR2, Music.stop)
signal.signal(signal.SIGRTMIN, go_to_admin)
if gpiozero and not args.no_coin:
    coinListener = gpiozero.Button(21)
    coinListener.when_pressed = coin_inserted
    print('Listening for coin')
else:
    print('Not listening for coin')
    time.sleep(1)
    coin_inserted()

def tarp(n):
    if (n * 60) > COIN_TIME_VALUE:
        return -1
    return (n * 60) + 2

while is_open(kiosk):

    
    # when 5, 2, 1 minutes left, play voice
    time_left = EXPIRERY_TIME - time.time()
    if time_left > 0 and time_left <= COIN_TIME_VALUE:
        if time_left < 7:
            Voice.play(Voice.countdown, chain=False)
            time_left = 0
        if time_left < tarp(0.5):
            Voice.play(Voice.s30)
        elif time_left < tarp(1):
            Voice.play(Voice.m1)
        elif time_left < tarp(2):
            Voice.play(Voice.m2)
        elif time_left < tarp(5):
            Voice.play(Voice.m5)
    
    if EXPIRERY_TIME > 0 and time.time() > EXPIRERY_TIME:
        expire()


    print(time_left)
    
    time.sleep(1)

print('Browser is closed, stopping servers and input devices')
gamesServer.stop()
menuServer.stop()
controllers.stop_all()
close()
kill_current_game()
os.remove('.marcade.pid')