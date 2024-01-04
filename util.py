import soundfile as sf
import sounddevice as sd

def play_sound(filename, block=False):
    sd.play(*sf.read(filename, dtype='int16'))
    if block: sd.wait()