import openal
import time

FADE_OUT_WHEN_STOPPING = True
FADE_IN_WHEN_STARTING = True
FADE_TIME = 5
FADE_STEPS = 20

class Sound:
    coin = openal.oalOpen('audio/sound/coin.wav')
    start = openal.oalOpen('audio/sound/start.wav')

    def play(sound, block=False):
        sound.play()
        if block:
            while sound.get_state() == openal.AL_PLAYING:
                pass

class Music:
    menu = openal.oalOpen('audio/music/menu.wav')

    current = None
    def stop(*args):
        if not Music.current:
            return print('No music to stop')
        print('Stopping music')
        # Fade out music
        if FADE_OUT_WHEN_STOPPING:
            for i in range(FADE_STEPS):
                Music.current.set_gain(1 - (i / FADE_STEPS))
                time.sleep(FADE_TIME / FADE_STEPS)
            Music.current.set_gain(0)
            time.sleep(1)
        Music.current.stop()
        Music.current = None

    def play(song, fade_in=FADE_IN_WHEN_STARTING):
        Music.stop()
        song.set_looping(True)
        if fade_in:
            song.set_gain(0)
            song.play()
            for i in range(FADE_STEPS):
                song.set_gain(i / FADE_STEPS)
                time.sleep(FADE_TIME / FADE_STEPS)
        else:
            song.set_gain(1)
            song.play()
        Music.current = song

close = openal.oalQuit