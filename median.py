import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

x = np.arange(1, 10, 0.05)
y = np.random.rand(len(x))
q = np.zeros(len(x))

plt.subplot(211)

plt.autoscale(enable=True, axis='x', tight=bool)
plt.plot(x, y, linewidth=0.5, c='grey', label='Původní data')
ax = plt.gca()
ax.xaxis.set_label_coords(0.98, -0.05)
plt.xlabel('t')
plt.ylabel('f(t)')
win = int(input('Enter window size:'))

# muj median
for i in range(len(x)):
    print(i)
    if i == 0:
        q[i] = 0
    elif i == len(x)-1:
        q[i] = 0
    else:
        b = (i+win)-1
        a = y[i:b]
        q[i] = np.median(a)

plt.plot(x, q, linewidth=1, label='mujmedian', color='forestgreen')

# vestavena funkce medfilt()
z = signal.medfilt(y, win)
plt.plot(x, z, linewidth=0.8, color='orangered', label='medfilt')
plt.legend()

plt.subplot(212)
plt.autoscale(enable=True, axis='x', tight=bool)
plt.plot(x, z-q)
plt.title('chyba', loc='center')

plt.show()
