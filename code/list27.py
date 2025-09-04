from __future__  import division
from numpy import *
from matplotlib.pyplot import *

fig, ax = subplots()
k = 0
fs = 2
ax.plot(t, sinc(k, fs*t), 
        t, sinc(k+1 -fs *t, '--', k/fs, 1, '0', (k)/fs, 0, 'o',
        t, sinc(k-1, fs*t), '--', k/fs, 1, 'o', (-k)/fs, 0, 'o'
        )
ax.hlines(0, -1, 1) # horizontal lines
ax.vlines(0, -.2,1)
ax.annotate('sample value goes here',
            xy=(0,1),           # arrowhead position     
            xytext=(-1+.1,1.1), # text position
            arrowprops = {'facecolor': 'red', 
                            'shrink': 0.05},
            )
ax.annotate('no interference here', 
            xy=(0,0),
            xytext=(-1+.1,0.5),
            arrowprops={'facecolor': 'green','shrink':0.05}
            )
