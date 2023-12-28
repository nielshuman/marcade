import time
from serve2 import DingesServer
from kiosk import kiosk_driver, kiosk_subprocess, is_open
import sounddevice as sd
import soundfile as sf

def play_sound(filename, block=False):
    sd.play(*sf.read(filename, dtype='int16'))
    if block: sd.wait()

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
time.sleep(5)
play_sound('audio/coin.mp3')
kiosk.get(menuServer.url + 'select.html')

while is_open(kiosk):
    time.sleep(1)

print('Browser is closed')
gamesServer.stop()
menuServer.stop()