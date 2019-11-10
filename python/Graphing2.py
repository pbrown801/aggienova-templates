from matplotlib.pylab import *
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import pandas as pd
from matplotlib.animation import FuncAnimation
import csv

mag_data=[]
time = []
f=[]
avg=[]
p=[]
t=[]
p01=[]
x=[]

file = open("..\output\SN2007af_magarray.csv", 'r', newline='').readlines()
reader = csv.reader(file, delimiter=',')
filters_from_csv = next(reader)[1::2]

for filters in filters_from_csv:
    data = pd.read_csv("..\output\SN2007af_magarray.csv", sep=",")
    data = data.dropna(axis=0, how='all')
    data = data.set_index('Time (MJD)')
    time_temp=list(data.index.values)
    time_1=time_temp[0]
    time_2=time_temp[len(time_temp)-1]
    data=data[filters]
    data=data.dropna()
    mag_data.append(list(data))
    time.append(list(data.index.values))
for i in range(len(mag_data)):
    tot = 0
    for j in range(len(mag_data[i])):
        tot+=mag_data[i][j]
    if (len(mag_data[i])==0):
        continue
    avg.append(tot/len(mag_data[i]))
    # print(avg)
for i in range(len(filters_from_csv)-1):
    if (i==4):
            time[i] = time[i] + [time_2]
            mag_data[i]=mag_data[i]+[avg[i]]
    elif (i==8):
        time[i] = [time_1] + time[i]
        mag_data[i]=[avg[i]]+mag_data[i]
    else:
        time[i] = [time_1] + time[i] + [time_2]
        mag_data[i]=[avg[i]]+mag_data[i]+[avg[i]]

plt.style.use('dark_background')

time_UVW2 = time[0]
UVW2 = mag_data[0]
time_UVM2 = time[1]
UVM2 = mag_data[1]
time_UVW1 = time[2]
UVW1 = mag_data[2]
time_U = time[3]
U = mag_data[3]
time_B = time[4]
B = mag_data[4]
time_V = time[5]
V = mag_data[5]
time_R = time[6]
R = mag_data[6]
time_I = time[7]
I = mag_data[7]
time_J = time[8]
J = mag_data[8]
time_H = time[9]
H = mag_data[9]

f1 = interp.interp1d(time_UVW2, UVW2, kind='cubic')
f2 = interp.interp1d(time_UVM2, UVM2, kind='cubic')
f3 = interp.interp1d(time_UVW1, UVW1, kind='cubic')
f4 = interp.interp1d(time_U, U, kind='cubic')
f5 = interp.interp1d(time_B, B, kind='cubic')
f6 = interp.interp1d(time_V, V, kind='cubic')
f7 = interp.interp1d(time_R, R, kind='cubic')
f8 = interp.interp1d(time_I, I, kind='cubic')
f9 = interp.interp1d(time_J, J, kind='cubic')
f10 = interp.interp1d(time_H, H, kind='cubic')
f0 = plt.figure(num=0, figsize=(8, 8))
ax01 = f0.add_subplot(211)
f0.subplots_adjust(hspace=1.5)
f0.patch.set_facecolor('xkcd:black')
ax01.set_title('MagArray plot versus Time (MJD)')
ax01.set_ylim(8, 23)
plt.tight_layout()

ax01.set_ylabel("MagArray of different Wavelengths")
ax01.set_xlabel("Time (MJD)")
p1 = zeros(0)
p2 = zeros(0)
p3 = zeros(0)
p4 = zeros(0)
p5 = zeros(0)
p6 = zeros(0)
p7 = zeros(0)
p8 = zeros(0)
p9 = zeros(0)
p1_0 = zeros(0)

t1 = zeros(0)
t2 = zeros(0)
t3 = zeros(0)
t4 = zeros(0)
t5 = zeros(0)
t6 = zeros(0)
t7 = zeros(0)
t8 = zeros(0)
t9 = zeros(0)
t10 = zeros(0)

p01, = ax01.plot(time_UVW2, UVW2, 'w-', label='UVW2')
p02, = ax01.plot(time_UVM2, UVM2, 'green', label='UVM2')
p03, = ax01.plot(time_UVW1, UVW1, 'r-', label='UVW1')
p04, = ax01.plot(time_U, U, 'c-', label='U')
p05, = ax01.plot(time_B, B, 'm-', label='B')
p06, = ax01.plot(time_V, V, 'y-', label='V')
p07, = ax01.plot(time_R, R, 'gray', label='R')
p08, = ax01.plot(time_I, I, 'w-', label='I')
p09, = ax01.plot(time_J, J, 'gray', label='J')
p10, = ax01.plot(time_H, H, 'w-', label='H')

ax01.legend([p01, p02, p03, p04, p05, p06, p07, p08, p09, p10], [p01.get_label(), p02.get_label(), p03.get_label(), p04.get_label(), p05.get_label(), p06.get_label(), p07.get_label(), p08.get_label(), p09.get_label(),p10.get_label()])

x1 = time_UVW2[0]
x2 = time_UVM2[0]
x3 = time_UVW1[0]
x4 = time_U[0]
x5 = time_B[0]
x6 = time_V[0]
x7 = time_R[0]
x8 = time_I[0]
x9 = time_J[0]
x10 = time_H[0]

def animate(self):
    global x1, x2, x3, x4, x5, x6, x7, x8, x9, x10
    global p1, p2, p3, p4, p5, p6, p7, p8, p9, p1_0
    global t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
    global time_UVW2, time_UVM2, time_UVW1, time_U, time_B, time_V, time_R, time_I, time_J, time_H

    tp1 = f1(x1)
    tp2 = f2(x2)
    tp3 = f3(x3)
    tp4 = f4(x4)
    tp5 = f5(x5)
    tp6 = f6(x6)
    tp7 = f7(x7)
    tp8 = f8(x8)
    tp9 = f9(x9)
    tp10 = f10(x10)

    p1 = append(p1, tp1)
    p2 = append(p2, tp2)
    p3 = append(p3, tp3)
    p4 = append(p4, tp4)
    p5 = append(p5, tp5)
    p6 = append(p6, tp6)
    p7 = append(p7, tp7)
    p8 = append(p8, tp8)
    p9 = append(p9, tp9)
    p1_0 = append(p1_0, tp10)

    t1 = append(t1, x1)
    t2 = append(t2, x2)
    t3 = append(t3, x3)
    t4 = append(t4, x4)
    t5 = append(t5, x5)
    t6 = append(t6, x6)
    t7 = append(t7, x7)
    t8 = append(t8, x8)
    t9 = append(t9, x9)
    t10 = append(t10, x10)

    inte1 = (time_UVW2[len(time_UVW2)-1] - time_UVW2[0]) / 1000
    inte2 = (time_UVM2[len(time_UVM2)-1] - time_UVM2[0]) / 1000
    inte3 = (time_UVW1[len(time_UVW1)-1] - time_UVW1[0]) / 1000
    inte4 = (time_U[len(U)-1] - time_U[0]) / 1000
    inte5 = (time_B[len(B)-1] - time_B[0]) / 1000
    inte6 = (time_V[len(V)-1] - time_V[0]) / 1000
    inte7 = (time_R[len(R)-1] - time_R[0]) / 1000
    inte8 = (time_I[len(I)-1] - time_I[0]) / 1000
    inte9 = (time_J[len(J)-1] - time_J[0]) / 1000
    inte10 = (time_H[len(H)-1] - time_H[0]) / 1000

    x1 += inte1
    x2 += inte2
    x3 += inte3
    x4 += inte4
    x5 += inte5
    x6 += inte6
    x7 += inte7
    x8 += inte8
    x9 += inte9
    x10 += inte10

    p01.set_data(t1, p1)
    p02.set_data(t2, p2)
    p03.set_data(t3, p3)
    p04.set_data(t4, p4)
    p05.set_data(t5, p5)
    p06.set_data(t6, p6)
    p07.set_data(t7, p7)
    p08.set_data(t8, p8)
    p09.set_data(t9, p9)
    p10.set_data(t10, p1_0)
    return p01, p02, p03, p04, p05, p06, p07, p08, p09, p10


simulation = FuncAnimation(f0, animate, blit=False, frames=999, interval=.01, repeat=False)
plt.show()
