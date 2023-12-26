CHROMIUM = ()
import subprocess, os


def open_kiosk(*tabs: str):
    """
    Open Chromium in kiosk mode with specified tabs.
    """

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
