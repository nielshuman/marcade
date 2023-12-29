import soundfile as sf
import sounddevice as sd

import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

def play_sound(filename, block=False):
    sd.play(*sf.read(filename, dtype='int16'))
    if block: sd.wait()

def listen_for_coin(pin, callback):
    if not GPIO:
        print('Not running on Raspberry Pi, not listening for coin')
        return
    counter_pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(counter_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(counter_pin, GPIO.RISING)
    GPIO.add_event_callback(counter_pin, callback)
    print(f'Listening for coin on pin {counter_pin}')