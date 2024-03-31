import openal
import time
import pulsectl

pulse = pulsectl.Pulse('Marcade')

FADE_OUT_WHEN_STOPPING = True
FADE_IN_WHEN_STARTING = True
FADE_TIME = 5
FADE_STEPS = 20

class Sound:
    coin = openal.oalOpen('audio/sound/coin.wav')
    start = openal.oalOpen('audio/sound/start.wav')
    timeover = openal.oalOpen('audio/sound/timeover.wav')

    def play(sound, block=False):
        sound.play()
        if block:
            while sound.get_state() == openal.AL_PLAYING:
                pass

class Voice:
    m1 = openal.oalOpen('audio/voice/1m.wav')
    m2 = openal.oalOpen('audio/voice/2m.wav')
    m5 = openal.oalOpen('audio/voice/5m.wav')
    s30 = openal.oalOpen('audio/voice/30s.wav')
    up = openal.oalOpen('audio/voice/time_is_up.wav')
    countdown = openal.oalOpen('audio/voice/countdown.wav')
    
    played = []

    def play(voice, chain=False):
        if voice in Voice.played:
            return False
        Voice.played.append(voice)
        
        set_process_volume('chromium', 0.3)
        if Music.current:
            Music.current.set_gain(0.2)

        time.sleep(0.5)

        voice.play()
        while voice.get_state() == openal.AL_PLAYING:
            pass
        
        if chain:
            return True

        time.sleep(0.5)
        set_process_volume('chromium', 1)
        if Music.current:
            Music.current.set_gain(1)

        return True
    
    def reset():
        Voice.played = []

class Music:
    menu = openal.oalOpen('audio/music/menu.wav')

    current = None
    def stop(*args, fade=True):
        if not Music.current:
            return print('No music to stop')
        print('Stopping music')
        # Fade out music
        if FADE_OUT_WHEN_STOPPING and fade:
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

def set_process_volume(binary_or_name, volume):
    for sink in pulse.sink_input_list():
        if binary_or_name.lower() in sink.proplist.get('application.process.binary', '').lower() or binary_or_name.lower() in sink.proplist.get('application.name', '').lower():
            pulse.volume_set_all_chans(sink, volume)
            return True
    return False