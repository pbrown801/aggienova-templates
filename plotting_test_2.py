from matplotlib.pylab import *
import matplotlib.pyplot as plt
import scipy.interpolate as interp
from matplotlib.animation import FuncAnimation

time=[54165.0591,54177.5535,54200.1088,54213.7318]
UVM2=[18.788,18.815,17.499,17.358]
f2=interp.interp1d(time,UVM2, kind='cubic')

f0=plt.figure(num=0, figsize=(8, 8))
f0.suptitle("Plot Traversal Animation", fontsize=10)
ax01 = subplot2grid((1, 1), (0, 0))
# ax02 = subplot2grid((2, 2), (0, 1))
# ax03 = subplot2grid((2, 2), (1, 0))
# ax04 = subplot2grid((2, 2), (1, 1))
f0.subplots_adjust(hspace=1.5)

ax01.set_title('MagArray plot versus Time (mjd)')

ax01.set_ylim(17,20)

# ax01.set_xlim(time[0],time[0]+5)

ax01.grid(True)

ax01.set_xlabel("Time (mjd)")
ax01.set_ylabel("UVM2")


p1=zeros(0)
t=zeros(0)
p01, = ax01.plot(time,UVM2,'b-',label='p1')

x=time[0]
xmax=time[0]+5.0

def animate(self):
    global x
    global p1
    global t
    global time
    global inte
    tp1 = f2(x)
    p1=append(p1,tp1)
    t=append(t,x)
    inte = (time[3]-time[0])/1000
    x+=inte

    p01.set_data(t,p1)

    # if x >= xmax - 1.00:
    #     p01.axes.set_xlim(time[0] + x - xmax + 0.04 , x + 0.04)
    return p01

simulation = FuncAnimation(f0, animate, blit=False, frames=1000, interval=.05, repeat=False)
plt.show()