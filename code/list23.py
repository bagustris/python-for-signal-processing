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
