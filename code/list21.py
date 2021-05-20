from __future__ import division
from matplotlib.pylab import *

fig,ax = subplots()
f = 1.0 # Hz, signal frequency
fs = 5.0 # Hz, sampling rate (ie. >= 2*f)
t = arange(-1,1+1/fs,1/fs) 	# sample interval, symmetric
							# for convenience later
x = sin(2*pi*f*t)
ax.plot(t,x,'o-')
ax.set_xlabel('Time',fontsize=18)
ax.set_ylabel('Amplitude',fontsize=18)
show()
