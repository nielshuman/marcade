import subprocess
import time
from multiprocessing import Process
# from serve import Kutserver
from serve2 import DingesServer

def open_kiosk(tabs):
    CHROMIUM_FLAGS = [
    '--kiosk',
    '--noerrdialogs',
    '--disable-infobars',
    '--no-first-run',
    '--ozone-platform=wayland',
    '--enable-features=OverlayScrollbar',
    '--start-maximized'
    ]
    
    return subprocess.Popen(['chromium'] + tabs + CHROMIUM_FLAGS, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

gserver = DingesServer('games/gunwizard')

pgserver = Process(target=gserver.serve, args=(8005,))
pgserver.start()

pkiosk = open_kiosk(['http://randomcolour.com/', '127.0.0.1:8005/'])

while pkiosk.poll() is None:
    print("Process is running.")
    time.sleep(2)
    
pgserver.terminate()