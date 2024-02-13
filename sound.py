print('Initing sound... ',  end="")
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *
pygame.mixer.init()
print('Done')

# def play_sound(filename, block=False):
#     sd.play(*sf.read(filename, dtype='int16'))
#     if block: sd.wait()

def play_sound(filename, block=False):
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(filename))
    if block:
        while pygame.mixer.Channel(1).get_busy():
            pass


def play_music(filename):
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(filename), -1)

def stop_music():
    pygame.mixer.stop() # TODO: only stop music
    pygame.mixer.pause()
    print('Stopping music')
