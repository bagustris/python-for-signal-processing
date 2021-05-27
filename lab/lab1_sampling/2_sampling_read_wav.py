# sampling_read_wav: read and plot wav file

import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import matplotlib.pyplot as plt

[fs, x] = wavfile.read('sin_500.wav')
print("sampling rate: ", fs)

sd.play(x, fs)
plt.plot(x)

## prosedur praktikum 2:
#0. Ganti file sine_500.wav dengan file anda pada percobaan #1 (write_sin)
#1. Ganti file sin_500.wav dengan speech.wav
#2. dengarkan y (speech.wav), dengan fs yang berbeda-beda, 
#   perhatikan perbedaannya (denganrkan dan plot)

## analisa (maksimal 1 halaman)
#1. Apa yang terjadi ketika memutar wav file dengan fs yang bukan aslinya 
##  (langkah 1)

