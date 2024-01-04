from gpiozero import Button
button = Button(21)
from util import *

def pressed():
    print("Muntje!")

button.when_pressed = pressed

while True:
    pass

# Exec=lxterminal -t Marcade --working-directory=/home/niels/marcade -e 'python3 marcade.py'