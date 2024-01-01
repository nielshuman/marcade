import soundfile as sf
import sounddevice as sd

import time
import soundfile as sf
import sounddevice as sd

try:
    import gpiod
    from gpiozero import Button
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
    button = Button(counter_pin)
    button.when_pressed = callback
    print(f'Listening for coin on pin {counter_pin}')