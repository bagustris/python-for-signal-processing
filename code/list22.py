from matplotlib.pylab import *

f = 1.0 # Hz, signal frequency
fs = 5.0 # Hz, sampling rate (ie. >= 2*f)
t = arange(-1,1+1/fs,1/fs)
x = sin(2*pi*f*t)

fig,ax = subplots()
ax.plot(t,x,'o-')
ax.axis(xmin = 1/(4*f)-1/fs*3,
		xmax = 1/(4*f)+1/fs*3,
		ymin = 0,
		ymax = 1.1 )
ax.set_xlabel('Time',fontsize=18)
ax.set_ylabel('Amplitude',fontsize=18)
show()
