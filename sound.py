print('Initing sound...')
import pygame
from pygame.locals import *
pygame.mixer.init()
print('Sound inited.')
# def play_sound(filename, block=False):
#     sd.play(*sf.read(filename, dtype='int16'))
#     if block: sd.wait()

def play_sound(filename, block=False):
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(filename))
    if block:
        pygame.mixer.Channel(1).join()


def play_music(filename):
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(filename), -1)

def stop_music():
    pygame.mixer.Channel(0).stop()