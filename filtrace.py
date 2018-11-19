import csv
from scipy import signal
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import os
os.chdir('F:\\')

fig1 = plt.figure(1)

ax = fig1.add_subplot(1, 1, 1)

data = np.genfromtxt('testovaci.dat', delimiter='\t')
row = data.shape[0]
col = data.shape[1]
data = data[:, 7:]

r = data[:, 103]
s = np.arange(0, row, 1)

# Discrete Fourier transform
#N = len(r)
#fs = 200
#Ts = 1.0/fs
#k = np.arange(N)
#frq = fs*k/N
#frq = frq[range(N/2)]
#DATA = np.fft.fft(r)/N
#DATA = DATA[range(N/2)]

# data filtration
n = 100
b = [1.0/ n] * n
a = 1
f = signal.lfilter(b, a, r) #1D one side filter
sg = signal.savgol_filter(r, 301, 2) #Savitzky-Golay
mf = signal.medfilt(r, 501) #Median filter

# plots
ax.plot(s, r, linewidth=0.3, c='r')
ax.plot(s, f, 'k')
ax.plot(s, sg, 'g')
ax.plot(s, mf, 'b')
ax.legend(['Original data', 'Filtfilt', 'Savitzky-Golay', 'Median filter'])
ax.set_title('Data filtration in Python')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Intensity ()')

#ax2 = fig1.add_subplot(2, 2, 3)
#ax2.plot(s, r, 'r')

#ax3 = fig1.add_subplot(2, 2, 4)
#ax3.plot(frq, abs(DATA), 'r')
#ax3.set_xlabel('Frequency (Hz)')
#ax3.set_ylabel('|Y(freq)|')


plt.show()
