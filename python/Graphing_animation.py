# Used: http://www.roboticslab.ca/wp-content/uploads/2012/11/robotics_lab_animation_example.txt

from matplotlib.pylab import *
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import pandas as pd
from matplotlib.animation import FuncAnimation
from pathlib import Path
import csv

plt.style.use('dark_background')
f0 = plt.figure(num=0, figsize=(8, 8))
ax01 = f0.add_subplot(211)
f0.subplots_adjust(hspace=1.5)
f0.patch.set_facecolor('xkcd:black')
ax01.set_title('MagArray plot versus Time (MJD)')
plt.tight_layout()
ax01.set_ylabel("MagArray of different Wavelengths")
ax01.set_xlabel("Time (MJD)")

mag_data = []
time = []
f = []
avg = []
p = []
p1 = []
t = []
p01 = []
x = []
new_time = []
colors = ['w-', 'r-', 'c-', 'm-', 'y-', 'gray', 'w-', 'r-', 'c-', 'm-', 'y-']
d = {}

file_name = Path("../output/SN2007af_magarray.csv")

# Filters
file = open(file_name, 'r', newline='').readlines()
reader = csv.reader(file, delimiter=',')
filters_from_csv = next(reader)[1::2]

# Data frame of the data using pandas
for filters in filters_from_csv:
    data = pd.read_csv(file_name, sep=",")
    data = data.dropna(axis=0, how='all')
    data = data.set_index('Time (MJD)')
    time_temp = list(data.index.values)  # Times
    time_1 = time_temp[0]  # first time in whole set
    time_2 = time_temp[len(time_temp)-1]  # last time in whole set
    data = data[filters]  # Gets the data for only the filters
    data = data.dropna()  # Drops unncessary values like empty
    mag_data.append(list(data))  # list of the data values
    time.append(list(data.index.values))  # list of times for the datavalues
    d[filters] = True

for i in range(len(mag_data)):
    tot = 0
    for j in range(len(mag_data[i])):
        tot += mag_data[i][j]
    if (len(mag_data[i]) == 0):
        continue
    else:
        avg.append(tot/len(mag_data[i]))

j = 0
for i in range(len(filters_from_csv)-1):
    if len(mag_data[i]) == 0:
        continue
    if ((time[i][0] == time_1) & (time[i][len(time[i])-1] != time_2)):
        time[i] = time[i] + [time_2]
        mag_data[i] = mag_data[i]+[round(avg[j], 3)]
        j += 1
    elif ((time[i][len(time[i])-1] == time_2) & (time[i][0] != time_1)):
        time[i] = [time_1] + time[i]
        mag_data[i] = [round(avg[j], 3)]+mag_data[i]
        j += 1
    elif ((time[i][len(time[i])-1] != time_2) & (time[i][0] != time_1)):
        time[i] = [time_1] + time[i] + [time_2]
        mag_data[i] = [round(avg[j], 3)]+mag_data[i]+[round(avg[j], 3)]
        j += 1
    else:
        continue

print(mag_data)
print(time)
# j = 0
# for i in range(len(mag_data)):
#     k = 0
#     count = 0
#     if len(mag_data[i]) == 0:
#         continue
#     else:
#         if mag_data[i][0] == avg[j]:
#             for k in range(len(mag_data[i])):
#                 if mag_data[i][k] == avg[j]:
#                     count += 1
#             if len(mag_data[i]) == count:
#                 f.append(interp.interp1d(time[i], mag_data[i], kind='linear'))
#                 j += 1
#                 new_time.append(time[i])
#         else:
#             f.append(interp.interp1d(time[i], mag_data[i], kind='linear'))
#             j += 1
#             new_time.append(time[i])

# for i in range(len(mag_data)):
#     if len(mag_data[i]) == 0:
#         d[filters_from_csv[i]] = False
#         continue
#     p.append(zeros(0))
#     t.append(zeros(0))
#     p01.append(ax01.plot(time[i], mag_data[i],
#                          colors[i], label=filters_from_csv[i]))
#     x.append(time[i][0])

# p1 = p[0]
# p3 = p[1]
# p4 = p[2]
# p5 = p[3]
# p6 = p[4]

# t1 = t[0]
# t3 = t[1]
# t4 = t[2]
# t5 = t[3]
# t6 = t[4]

# p0_1 = p01[0][0]
# p0_3 = p01[1][0]
# p0_4 = p01[2][0]
# p0_5 = p01[3][0]
# p0_6 = p01[4][0]


# def animate(self):
#     global x
#     global p, p1, p3, p4, p5, p6
#     global t, t1, t3, t4, t5, t6
#     global f
#     global new_time
#     global d
#     tp = []
#     x_temp = []
#     inte = []
#     for i in range(len(f)):
#         temp = f[i]
#         tp.append(temp(x[i]))
#         x_temp.append(x[i])
#         inte.append(((new_time[i][len(new_time[i])-1])-new_time[i][0])/1000)
#         x[i] += inte[i]

#     p1 = append(p1, tp[0])
#     p3 = append(p3, tp[1])
#     p4 = append(p4, tp[2])
#     p5 = append(p5, tp[3])
#     p6 = append(p6, tp[4])

#     t1 = append(t1, x_temp[0])
#     t3 = append(t3, x_temp[1])
#     t4 = append(t4, x_temp[2])
#     t5 = append(t5, x_temp[3])
#     t6 = append(t6, x_temp[4])

#     p0_1.set_data(t1, p1)
#     p0_3.set_data(t3, p3)
#     p0_4.set_data(t4, p4)
#     p0_5.set_data(t5, p5)
#     p0_6.set_data(t6, p6)

#     return p0_1, p0_3, p0_4, p0_5, p0_6


# simulation = FuncAnimation(f0, animate, frames=999, interval=1, repeat=False)
# plt.show()
