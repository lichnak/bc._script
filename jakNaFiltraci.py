import numpy as np

data_x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
data_filtered = np.zeros(data_x.shape)
alpha = 2 # koeficient u filtrovanych dat
beta = 1 # koeficient u nefiltrovanych dat
# vyfiltrovana data (k) = beta * nefiltrovana data(k) + alpha * vyfiltrovana data(k-1)

for idx, x in np.ndenumerate(data_x):
    if idx[0] == 0:
        data_filtered[0] = x
    else:
        data_filtered[idx[0]] = beta * x + alpha * data_filtered[idx[0] - 1]
        print("beta * ",x,"+ alpha * ", data_filtered[idx[0] - 1])
print(data_x)
print(data_filtered)