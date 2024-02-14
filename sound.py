# This file is dead!


# print('Initing sound... ',  end="")
# from os import environ
# environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# import pygame
# from pygame.locals import *
# pygame.mixer.init()
# print('Done')


import openal

global music_source
music_source = None

# def play_sound(filename, block=False):
#     sd.play(*sf.read(filename, dtype='int16'))
#     if block: sd.wait()

def play_sound(filename, block=False):
    # pygame.mixer.Channel(1).play(pygame.mixer.Sound(filename))
    # if block:
    #     while pygame.mixer.Channel(1).get_busy():
    #         pass
    print('Playing sound', filename)
    source = openal.oalOpen(filename)
    source.play()
    if block:
        while source.get_state() == openal.AL_PLAYING:
            pass

def play_music(filename):
    # pygame.mixer.Channel(0).play(pygame.mixer.Sound(filename), -1)
    print('Playing music', filename)
    global music_source
    if music_source:
        music_source.stop()
    music_source = openal.oalOpen(filename)
    music_source.set_looping(True)
    music_source.play()

def stop_music():
    # pygame.mixer.Channel(0).stop()
    print('Stopping music')
    global music_source
    if music_source:
        music_source.stop()
        music_source = None
    else:
        print('No music playing')
