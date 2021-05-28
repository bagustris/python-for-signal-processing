#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt. subplots ()
k = 0
fs = 2 # makes this plot easier to read
ax.plot(t, np.sinc(k - fs * t),
		t, np.sinc(k+1 - fs * t),'--',k/fs,1,'o',(k)/fs,0,'o',
		t, np.sinc(k-1 - fs * t),'--',k/fs,1,'o',(-k)/fs,0,'o'
)
ax.hlines(0,-1,1) # horizontal lines
ax.vlines(0,-.2,1) # vertical lines
ax.annotate('sample value goes here',
			xy=(0,1), # arrowhead position
			xytext=(-1+.1,1.1),# text position
			arrowprops={'facecolor':'red',
			'shrink':0.05},
)
ax.annotate('no interference here',
			xy=(0,0),
			xytext=(-1+.1,0.5),
			arrowprops={'facecolor':'green','shrink':0.05},
)
plt.show()