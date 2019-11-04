from matplotlib.pylab import *
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import pandas as pd
from matplotlib.animation import FuncAnimation
import csv

mag_data = []
time = []
f = []
avg = []
p = []
t = []
p01 = []
x = []
colors = ['w-', 'green', 'r-', 'c-', 'm-', 'y-', 'gray', 'w-']

file = open("output\SN2007af_magarray.csv", 'r', newline='').readlines()
reader = csv.reader(file, delimiter=',')
filters_from_csv = next(reader)[1::2]

for filters in filters_from_csv:
    data = pd.read_csv("output\SN2007af_magarray.csv", sep=",")
    data = data.dropna(axis=0, how='all')
    data = data.set_index('Time (MJD)')
    time_temp = list(data.index.values)
    time_1 = time_temp[0]
    time_2 = time_temp[len(time_temp) - 1]
    data = data[filters]
    data = data.dropna()
    mag_data.append(list(data))
    time.append(list(data.index.values))
for i in range(len(mag_data)):
    tot = 0
    for j in range(len(mag_data[i])):
        tot += mag_data[i][j]
    avg.append(tot / len(mag_data[i]))
for i in range(len(filters_from_csv)):
    if i != 4:
        time[i] = [time_1] + time[i] + [time_2]
        mag_data[i] = [avg[i]] + mag_data[i] + [avg[i]]
    else:
        time[i] = time[i] + [time_2]
        mag_data[i] = mag_data[i] + [avg[i]]

for i in range(len(mag_data)):
    f.append(interp.interp1d(time[i], mag_data[i], kind='cubic'))

f0 = plt.figure(num=0, figsize=(8, 8))
ax01 = f0.add_subplot(211)
f0.subplots_adjust(hspace=1.5)
f0.patch.set_facecolor('xkcd:black')
ax01.set_title('MagArray plot versus Time (MJD)')
ax01.set_ylim(8, 23)
plt.tight_layout()

ax01.set_ylabel("MagArray of different Wavelengths")
ax01.set_xlabel("Time (MJD)")
for i in range(len(mag_data)):
    p.append(zeros(0))
    t.append(zeros(0))
    p01.append(ax01.plot(time[i], mag_data[i], colors[i], label=filters_from_csv[i]))
    x.append(time[i][0])


def animate(self):
    global x
    global p
    global t
    global time
    global tp
    global inte
    tp = []
    inte = []
    for i in range(len(mag_data)):
        temp = f[i]
        tp.append(temp(x[i]))
        p[i].append(p[i], tp[i])
        t[i].append(t[i], x[i])
        inte.append((time[i][len(time[i]) - 1] - time[i][0]) / 1000)
        x[i] += inte[i]
        p01[i].set_data(t[i], p[i])
        print(p01)
    return p01


simulation = FuncAnimation(f0, animate, blit=False, frames=999, interval=.01, repeat=False)
plt.show()
