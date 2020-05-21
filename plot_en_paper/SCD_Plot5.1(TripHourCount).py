import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

n_C = [13160, 196984, 998591, 2510799, 1235263, 352025, 226157, 237333, 233549, 207479, 236484, 355617, 938226, 1562587, 1054989, 553942, 441071, 312601, 50850]
n_NC = [2530, 30923, 127254, 268412, 183505, 101401, 83336, 90886, 97049, 92143, 98475, 118377, 174925, 210928, 142346, 95084, 86467, 55486, 9085]
n_NH = [1160, 11370, 53219, 114995, 71874, 33266, 24487, 26559, 27571, 26002, 26933, 30997, 48743, 63953, 41134, 26624, 24112, 16788, 2588]

# n_C = np.array(n_C)
# n_NC = np.array(n_NC)
# n_NH = np.array(n_NH)

# fig, axes = plt.subplots(figsize = (15,10))
# length = 3
# plt.bar([i for i in range(0,24)],np.array(n_C),np.array([3]*length),label = 'commuter')
# ax = plt.gca()
# ax.set_xticks(np.array([x*4 for x in range(length)]))
# ax.set_xticklabels([i for i in range(5,24)])
#
# plt.legend()
# plt.show()

fig = plt.figure(figsize=(8,4))
plt.bar([i for i in range(5,24)], n_C, label = 'commuter', color = seaborn.xkcd_rgb['nice blue'])
plt.bar([i for i in range(5,24)], n_NC, bottom = n_C, label = 'non-commuter', color = seaborn.xkcd_rgb['orange red'])
plt.bar([i for i in range(5,24)], n_NH, bottom = np.sum([n_C,n_NC], axis=0), label = 'non-home', color = seaborn.xkcd_rgb['seaweed green'])
# plt.xlim(5,24)
plt.xticks(range(5,24,1))
plt.xlabel(r'Departure time, t[h]', fontsize=12)
plt.ylabel(r'No. of depatures, N', fontsize=12)
plt.legend()
plt.tight_layout()

plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\TripHourCount.png',dpi=150)
plt.show()

