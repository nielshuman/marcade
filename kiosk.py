CHROMIUM = ()
import subprocess, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def kiosk_subprocess(*tabs: str):
    """
    Open Chromium in kiosk mode with specified tabs, using subprocess.
    Returns a subprocess.Popen object.
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

def kiosk_driver(url: str = None):
    """
    Open Chromium in kiosk mode using Selenium WebDriver.
    Optionally, open a URL.
    """

    chrome_options = Options()
    chrome_options.add_argument('--kiosk')
    chrome_options.add_argument('--noerrdialogs')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--ozone-platform=wayland')
    chrome_options.add_argument('--enable-features=OverlayScrollbar')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    if url: driver.get(url)
    
    return driver

def is_open(driver: webdriver.Chrome):
    """
    Checks if a browser is open by attempting to access the driver's title.
    """
    try:
        driver.title
        return True
    except:
        return False