from __future__ import division 
from matplotlib.pyplot import *
from numpy import *

f = 1.0
fs = 5.0
t = arange(-1,1+1/fs,1/fs)
x = sin(2*pi*f*t)

interval = []
apprx = []

tp = hstack([linspace(t[i], t[i+1], 20, False) for i in range(len(t)-1)])

for i in range(len(t)-1):
	interval.append(logical_and(t[i] <= tp,tp < t[i+1]))
	apprx.append((x[i+1]-x[i])/(t[i+1]-t[i])*(tp[interval[-1]]-t[i]) + x[i])
x_hat = piecewise(tp, interval, apprx) # piecewise linear approximation

fig, ax1 = subplots()
ax1.fill_between(tp,x_hat,sin(2*pi*f*tp),facecolor='red')
ax1.set_xlabel('Time',fontsize=18)
ax1.set_ylabel('Amplitude',fontsize=18)
ax2 = ax1.twinx() # create clone of ax1
sqe = (x_hat-sin(2*pi*f*tp))**2 #compute squared-error
ax2.plot(tp, sqe,'r')
ax2.axis(xmin=-1,ymax= sqe.max() )
ax2.set_ylabel('Squared error', color='r',fontsize=18)
ax1.set_title('Errors with Piecewise Linear Interpolant',fontsize=18)

