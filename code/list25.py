from __future__ import division 
from matplotlib.pyplot import *
from numpy import *

f = 1.0
fs = 5.0
t = arange(-1,1+1/fs,1/fs)
x = sin(2*pi*f*t)

fig, ax = subplots()
t = linspace(-1,1, 100)
ts = arange(-1, 1+1/fs, 1/fs)
num_coeffs = len (ts)
sm = 0
for k in range(-num_coeffs, num_coeffs):
    sm += sin(2*pi*(k/fs))*sin(k - fs*t)
ax.plot(t, sm, '--', t, sin(2*pi*t), ts, sin(2*pi*ts), 'o')
ax.set_title('Sampling rate=%3.2f Hz' % fs, fontsize=18)
show()
