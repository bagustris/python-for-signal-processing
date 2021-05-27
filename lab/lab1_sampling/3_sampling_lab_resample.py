# sampling_resample.py: analyze different sampling frequency
import librosa
import sounddevice as sd

[y, sr] = librosa.load('speech.wav', sr=None)
sd.play(y, sr)

y_8k = librosa.resample(y, sr, 8000)
sd.play(y, 8000)

## prosedur praktikum 3:
#0. dengarkan y dengan fs aslinya
#1. Resample y dengan 4 fs yang berbeda, 2 upsample dan 2 downsample
#   dengarkan dan plot hasilnya
#2. Simpan hasil resample dalam wav file (4 wav files)

### Analisa laporan (maksimal 2 halaman termasuk plot)
## 1. Apa yang berubah setelah proses resample? Misal sinyal x di resample 
##     menjadi x'. Apa bedanya x dan x' ? hint:dengarkan dan plot

## Analisa praktikum 1, 2, dan 3, digabung dalam 3 halaman pdf
## file pdf dan wav digabung dalam format NRP.zip
