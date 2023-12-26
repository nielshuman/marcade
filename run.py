import subprocess
import time
# from serve import Kutserver
from serve2 import DingesServer
import os
CHROMIUM = ()

def open_kiosk(*tabs):
    global CHROMIUM
    if not CHROMIUM:
        if os.system("dpkg -s chromium-browser | grep Status") == 0:
            CHROMIUM = ('chromium-browser',)
        elif os.system("dpkg -s chromium | grep Status") == 0:
            CHROMIUM = ('chromium',)
        else:
            raise Exception('Chromium not installed')
    CHROMIUM_FLAGS = (
    '--kiosk',
    '--noerrdialogs',
    '--disable-infobars',
    '--no-first-run',
    '--ozone-platform=wayland',
    '--enable-features=OverlayScrollbar',
    '--start-maximized'
    ) 
    return subprocess.Popen(CHROMIUM + tabs + CHROMIUM_FLAGS,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

gunwizard = DingesServer('games/gunwizard', 8005)
gunwizard.start()

pkiosk = open_kiosk('randomcolour.com', gunwizard.url)

while pkiosk.poll() is None:
    print("Process is running.")
    time.sleep(2)
    
# pkiosk = open_kiosk(['http://randomcolour.com/', 'pws.justniels.nl', '127.0.0.1:8005/'])

gunwizard.stop()