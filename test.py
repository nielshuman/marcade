import sounddevice as sd
import soundfile as sf
import time

data, fs = sf.read('coin.mp3', dtype='int16')
sd.play(data, fs)
time.sleep(5)