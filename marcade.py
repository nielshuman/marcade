import os
# Change the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# import time
from serve2 import DingesServer
# from kiosk import kiosk_driver, is_open
# from util import play_sound, AntimicroX, get_game_by_id
try:
    import gpiozero
except:
    gpiozero = None

# antimciroX = AntimicroX('empty')
# antimciroX.start()
gamesServer = DingesServer('games', 8200)
gamesServer.serve()

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
    coin_inserted()

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed, stopping servers and AntimicroX')
gamesServer.stop()
menuServer.stop()
antimciroX.stop()