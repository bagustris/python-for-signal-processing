# sampling_lab.py: generate sine wave and save as wave.file
# 2021/05/21: initial commit

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile

f = 400             # freq
fs = 8000           # sampling frequency
dur = 5             # duration in seconds
t = np.arange(0, dur, 1.0/fs)
y = np.sin(2* np.pi*f*t)

# play audio (sin) signal
# sd.play(y, fs)

# simpan sin wave sebagai wav file
# wavfile.write('sin_400.wav', fs, y)


## Prosedur praktikum 1:
#0. Ganti f sesuka anda (fs menyesuaikan) dan denganrkan suara yang dihasilkan
#1. Pilih satu nilai f yang anda suka
#2. Variasikan fs dengan 5 nilai yang berbeda-beda, simpan sebagai wav files
#3. Plot setiap perubahan fs pada langkah 2 dengan axis-x yang pendek

## Analisa laporan (maksimal 1 halam termasuk plot)
# 1. Apa yang anda dapat simpulkan dari fs yang berubah-ubah? 
#    (hint: analisa perbedaan plot)
