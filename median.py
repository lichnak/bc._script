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
    k = (win - 1) // 2
    m = y[i + 1:((i + 1) + k)]
    n = y[(i-k):i]
    if i < k:
        # ----- correct -------
        zero1 = np.zeros(k-i, dtype=int)
        a = np.concatenate((zero1, y[:i+1], m), axis=None)
        q[i] = np.median(a)
        # ---------------------
    elif (i+((win-1)//2)) > (len(x)-1):
        # ----- correct -------
        p = k-((len(x)-1)-i)
        zero2 = np.zeros(p, dtype=int)
        b = np.concatenate((n, y[i:], zero2), axis=None)
        q[i] = np.median(b)
        # ---------------------
    else:
        # ----- correct -------
        c = y[i-((win-1)//2):(i+((win+1)//2))]
        q[i] = np.median(c)
        # ---------------------


plt.plot(x, q, linewidth=1, label='mujmedian', color='green')

# vestavena funkce medfilt()
z = signal.medfilt(y, win)

plt.plot(x, z, linewidth=0.8, color='orangered', label='medfilt')
plt.legend()

plt.subplot(212)
plt.autoscale(enable=True, axis='x', tight=bool)
plt.plot(x, z-q)
plt.title('chyba', loc='center')

plt.show()
