import openal

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
        if Music.current:
            Music.current.stop()
            Music.current = None
    def play(song):
        Music.stop()
        song.set_looping(True)
        song.play()
        Music.current = song

close = openal.oalQuit