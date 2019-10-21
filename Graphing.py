from matplotlib.pylab import *
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import pandas as pd
from matplotlib.animation import FuncAnimation
import numpy as np
plt.style.use('dark_background')

pd.options.display.float_format = "{:.2f}".format
pd.options.display.max_rows = 10

magarray_data = pd.read_csv("SN2007af_magarray.csv", sep=",")
magarray_data.head()
print(magarray_data)

# time_UVW2 = [54161.8408, 54165.0591, 54177.5535, 54200.1088, 54213.7318, 54309.2917]
# UVW2 = [((18.788 + 18.815 + 17.499 + 17.358) / 4), 18.788, 18.815, 17.499, 17.358,((18.788 + 18.815 + 17.499 + 17.358) / 4)]
# time_UVM2 = [54161.8408, 54165.0591, 54177.5535, 54200.1088, 54213.7318, 54309.2917]
# UVM2 = [(0.189 + 0.195 + 0.121 + 0.115) / 4, 0.189, 0.195, 0.121, 0.115, (0.189 + 0.195 + 0.121 + 0.115) / 4]
# time_UVW1 = [54161.8408, 54170.6312, 54179.5612, 54204.4517, 54217.2887, 54309.2917]
# UVW1 = [(19.673 + 19.636 + 18.966 + 19.253) / 4, 19.673, 19.636, 18.966, 19.253,(19.673 + 19.636 + 18.966 + 19.253) / 4]
# time_U = [54161.8408,54204.4517,54309.2917]
# U = [0.314,0.314,0.314]
# time_B = [54161.8408, 54171.5313, 54206.5268, 54309.2917]
# B = [((17.243+15.638)/2), 17.243, 15.638, ((17.243+15.638)/2)]
# time_V = [54161.8408, 54171.5313, 54206.5268, 54309.2917]
# V = [((0.088+0.07)/2), 0.088, 0.07, ((0.088+0.07)/2)]
# time_R = [54161.8408, 54172.3682, 54208.7714, 54237.9345, 54272.4349, 54309.2917]
# R = [((15.38 + 13.885 + 14.67 + 14.432) / 4), 15.38, 13.885, 14.67, 14.432, ((15.38 + 13.885 + 14.67 + 14.432) / 4)]
# time_I = [54161.8408, 54172.3682, 54208.7714, 54237.9345, 54272.4349, 54309.2917]
# I = [((0.057 + 0.043 + 0.008 + 0.009) / 4), 0.057, 0.043, 0.008, 0.009, ((0.057 + 0.043 + 0.008 + 0.009) / 4)]

# f1 = interp.interp1d(time_UVW2, UVW2, kind='cubic')
# f2 = interp.interp1d(time_UVM2, UVM2, kind='cubic')
# f3 = interp.interp1d(time_UVW1, UVW1, kind='cubic')
# f4 = interp.interp1d(time_U, U, kind='nearest')
# f5 = interp.interp1d(time_B, B, kind='cubic')
# f6 = interp.interp1d(time_V, V, kind='cubic')
# f7 = interp.interp1d(time_R, R, kind='cubic')
# f8 = interp.interp1d(time_I, I, kind='cubic')
#
# f0 = plt.figure(num=0, figsize=(8, 8))
# ax01 = f0.add_subplot(211)
# ax02 = f0.add_subplot(212)
# # ax03 = f0.add_subplot(222)
# # ax01 = subplot2grid((2, 2), (0, 0))
# # ax02 = subplot2grid((2, 2), (0, 1))
# # ax03 = subplot2grid((2, 2), (1, 0))
# # ax04 = subplot2grid((2, 2), (1, 1))
# f0.subplots_adjust(hspace=1.5)
# f0.patch.set_facecolor('xkcd:black')
# ax01.set_title('MagArray plot versus Time (mjd)')
#
# ax01.set_ylim(0, 25)
# ax02.set_ylim(0, 0.35)
#
# # ax01.grid(True)
# # ax02.grid(True)
# plt.tight_layout()
#
# ax02.set_xlabel("Time (mjd)")
# ax01.set_ylabel("MagArray of different Wavelengths")
# ax02.set_ylabel("MagArray of different Wavelengths")
# p1 = zeros(0)
# p2 = zeros(0)
# p3 = zeros(0)
# p4 = zeros(0)
# p5 = zeros(0)
# p6 = zeros(0)
# p7 = zeros(0)
# p8 = zeros(0)
#
# t1 = zeros(0)
# t2 = zeros(0)
# t3 = zeros(0)
# t4 = zeros(0)
# t5 = zeros(0)
# t6 = zeros(0)
# t7 = zeros(0)
# t8 = zeros(0)
#
# p01, = ax01.plot(time_UVW2, UVW2, 'b-', label='UVW2')
# p02, = ax02.plot(time_UVM2, UVM2, 'green', label='UVM2')
# p03, = ax01.plot(time_UVW1, UVW1, 'r-', label='UVW1')
# p04, = ax02.plot(time_U, U, 'c-', label='U')
# p05, = ax01.plot(time_B, B, 'm-', label='B')
# p06, = ax02.plot(time_V, V, 'y-', label='V')
# p07, = ax01.plot(time_R, R, 'gray', label='R')
# p08, = ax02.plot(time_I, I, 'w-', label='I')
#
# ax01.legend([p01, p03, p05, p07], [p01.get_label(), p03.get_label(), p05.get_label(), p07.get_label()])
# ax02.legend([p02, p04, p06, p08], [p02.get_label(), p04.get_label(), p06.get_label(), p08.get_label()])
# x1 = time_UVW2[0]
# x2 = time_UVM2[0]
# x3 = time_UVW1[0]
# x4 = time_U[0]
# x5 = time_B[0]
# x6 = time_V[0]
# x7 = time_R[0]
# x8 = time_I[0]
#
#
# def animate(self):
#     global x1, x2, x3, x4, x5, x6, x7, x8
#     global p1, p2, p3, p4, p5, p6, p7, p8
#     global t1, t2, t3, t4, t5, t6, t7, t8
#     global time_UVW2, time_UVM2, time_UVW1, time_U, time_B, time_V, time_R, time_I
#     tp1 = f1(x1)
#     tp2 = f2(x2)
#     tp3 = f3(x3)
#     tp4 = f4(x4)
#     tp5 = f5(x5)
#     tp6 = f6(x6)
#     tp7 = f7(x7)
#     tp8 = f8(x8)
#
#     p1 = append(p1, tp1)
#     p2 = append(p2, tp2)
#     p3 = append(p3, tp3)
#     p4 = append(p4, tp4)
#     p5 = append(p5, tp5)
#     p6 = append(p6, tp6)
#     p7 = append(p7, tp7)
#     p8 = append(p8, tp8)
#
#     t1 = append(t1, x1)
#     t2 = append(t2, x2)
#     t3 = append(t3, x3)
#     t4 = append(t4, x4)
#     t5 = append(t5, x5)
#     t6 = append(t6, x6)
#     t7 = append(t7, x7)
#     t8 = append(t8, x8)
#
#     inte1 = (time_UVW2[5] - time_UVW2[0]) / 1000
#     inte2 = (time_UVM2[5] - time_UVM2[0]) / 1000
#     inte3 = (time_UVW1[5] - time_UVW1[0]) / 1000
#     inte4 = (time_U[2] - time_U[0]) / 1000
#     inte5 = (time_B[3] - time_B[0]) / 1000
#     inte6 = (time_V[3] - time_V[0]) / 1000
#     inte7 = (time_R[5] - time_R[0]) / 1000
#     inte8 = (time_I[5] - time_I[0]) / 1000
#
#     x1 += inte1
#     x2 += inte2
#     x3 += inte3
#     x4 += inte4
#     x5 += inte5
#     x6 += inte6
#     x7 += inte7
#     x8 += inte8
#
#     p01.set_data(t1, p1)
#     p02.set_data(t2, p2)
#     p03.set_data(t3, p3)
#     p04.set_data(t4, p4)
#     p05.set_data(t5, p5)
#     p06.set_data(t6, p6)
#     p07.set_data(t7, p7)
#     p08.set_data(t8, p8)
#
#     return p01, p02, p03, p04, p05, p06, p07, p08
#
#
# simulation = FuncAnimation(f0, animate, blit=False, frames=999, interval=.01, repeat=False)
# plt.show()
