import matplotlib.pyplot as plt
import scipy.interpolate as interp
import pandas as pd
import csv
import math
from pathlib import Path
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import os
import time
import statistics as s
from manipulate_readinuvot import uvot
import scipy 
import matplotlib.image as mpimg

plotAvgs = []
plots = "SN2005cs"
spread=3
# Open data file
row_count = 0
try:
    file = open('../output/' + plots + 'template.csv').readlines()
    row_count = sum(1 for r in file)
    #print('Rows = ' + str(row_count))
except OSError as err:
    print("Could not find template for supernova " + plots + ": {0}".format(err))
    exit

# Read in output data
wave = []
log_fluxTot = [] # Sums of log(flux) vals for each given wave
log_fluxCount = [] # Count of total times a wave's flux val has been added to Tot
log_fluxAvg = [] # Avg of all given flux vals for each given wave
for row in range(1, row_count):
    r = file[row].split(',')
    if(float(r[2]) > 0):
        #print('Adding ' + r[1] + ', ' + str(math.log(float(r[2]), 10)))
        if(not float(r[1]) in wave):
            wave.append(int(r[1]))
            log_fluxTot.append( math.log(float(r[2]), 10) )
            log_fluxCount.append(1)
        else:
            waveInd = wave.index(int(r[1]))
            log_fluxTot[waveInd] += math.log(float(r[2]), 10)
            log_fluxCount[waveInd] += 1

# Compute avg. flux values and find avg total value for 'centering'
plot_sum = 0
for i in range(len(wave)):
    log_fluxAvg.append( log_fluxTot[i] / log_fluxCount[i] )
    plot_sum += log_fluxAvg[i]

# Save the avg log(flux) to center line around
plotAvgs.append(plot_sum / len(wave))
#print("Avg for supernova " + plots[p] + " = " + str(plotAvgs[p]))

# Constant value to add to cur plot for spreading (each should be centered around multiples of 3)
c = spread*(1) - plotAvgs[0]

# Add c to plot
for i in range(len(wave)):
    log_fluxAvg[i] += c

# print(s.mean(log_fluxAvg))
print(uvot(plots, 'y'))
df = uvot(plots, 'y')
print(df['Time (MJD)'])

gs = gridspec.GridSpec(2, 3)

fig = plt.figure()
fig.set_tight_layout(True)

# ---------------------------------------------------------- ax1 plot ----------------------------------------------------------

ax1 = fig.add_subplot(gs[-1, :-1]) 
f_b= scipy.interpolate.interp1d(
        df['Time (MJD)'], df['B'], kind='cubic', fill_value="extrapolate")
f_u= scipy.interpolate.interp1d(
        df['Time (MJD)'], df['U'], kind='cubic', fill_value="extrapolate")
f_uvm2= scipy.interpolate.interp1d(
        df['Time (MJD)'], df['UVM2'], kind='cubic', fill_value="extrapolate")
f_uvw1= scipy.interpolate.interp1d(
        df['Time (MJD)'], df['UVW1'], kind='cubic', fill_value="extrapolate")
f_uvw2= scipy.interpolate.interp1d(
        df['Time (MJD)'], df['UVW2'], kind='cubic', fill_value="extrapolate")
f_v= scipy.interpolate.interp1d(
        df['Time (MJD)'], df['V'], kind='cubic', fill_value="extrapolate")
time_extrap = [i for i in np.arange(df['Time (MJD)'][0]-1, df['Time (MJD)'].iloc[-1]+1, (df['Time (MJD)'].iloc[-1]-df['Time (MJD)'][0])/380)]
b_extrap = f_b(time_extrap)
u_extrap = f_u(time_extrap)
uvm2_extrap = f_uvm2(time_extrap)
uvw1_extrap = f_uvw1(time_extrap)
uvw2_extrap = f_uvw2(time_extrap)
v_extrap = f_v(time_extrap)

b_plot,=ax1.plot([], [])
u_plot,=ax1.plot([], [])
uvm2_plot,=ax1.plot([], [])
uvw1_plot,=ax1.plot([], [])
uvw2_plot,=ax1.plot([], [])
v_plot,=ax1.plot([], [])
# ax1.plot(time_extrap, b_extrap)
# ax1.plot(time_extrap, u_extrap)
# ax1.plot(time_extrap, uvm2_extrap)
# ax1.plot(time_extrap, uvw1_extrap)
# ax1.plot(time_extrap, uvw2_extrap)
# ax1.plot(time_extrap, v_extrap)

min_ = min(min(b_extrap), min(u_extrap), min(uvm2_extrap), min(uvw1_extrap), min(uvw2_extrap), min(v_extrap))
max_ = max(max(b_extrap), max(u_extrap), max(uvm2_extrap), max(uvw1_extrap), max(uvw2_extrap), max(v_extrap))

# ---------------------------------------------------------- ax2 plot ----------------------------------------------------------
ax2 = fig.add_subplot(gs[-1, 2]) 
ax2.plot([0,1])
# mpimg image
ax2.set_xticks([])
ax2.set_yticks([])
files=os.listdir(os.path.join('..','uvot','animation_images'))
files_png = [f for f in files if (f.endswith('.png') and f.startswith("SN2005cs"))]
imgs_dict={}
change_idx = []
for idx,t in enumerate(df['Time (MJD)']):
    change_idx=list(filter(lambda i: i >= t, time_extrap))[0]
    imgs_dict[time_extrap.index(change_idx)]=files_png[idx]

ax2.set_title("Image: "+str(files_png[0]))
plot_img = mpimg.imread(os.path.join('..','uvot','animation_images', files_png[0])) 
show_img=ax2.imshow(plot_img)


# ---------------------------------------------------------- ax3 plot ----------------------------------------------------------
ax3 = fig.add_subplot(gs[0, :])
ax3.set_xlabel('Wavelength (angstroms)')
ax3.set_ylabel('log(flux)+constant')
wave_flux,=ax3.plot([],[])

def init():
    ax1.set_xlim(df['Time (MJD)'][0]-1-((time_extrap[-1]-time_extrap[0])/20), time_extrap[-1]+1+((time_extrap[-1]-time_extrap[0])/20))
    ax1.set_ylim(min_-(max_-min_)/20,max_+(max_-min_)/20)
    ax3.set_xlim(wave[0]-((wave[-1]-wave[0])/20), wave[-1]+((wave[-1]-wave[0])/20))
    ax3.set_ylim(log_fluxAvg[0]-((log_fluxAvg[-1]-log_fluxAvg[0])/20), log_fluxAvg[-1]+((log_fluxAvg[-1]-log_fluxAvg[0])/20))
    ax3.invert_yaxis()
    ax1.invert_yaxis()
    return wave_flux,


def update(i):
    wave_flux.set_data(wave[0:i],log_fluxAvg[0:i])
    # ax2.set_title("Image: "+str(files_png[i]))
    # plot_img = mpimg.imread(os.path.join('animation_images', files_png[i])) 
    # show_img.set_data(plot_img)
    b_plot.set_data(time_extrap[0:i],b_extrap[0:i])
    u_plot.set_data(time_extrap[0:i],u_extrap[0:i])
    uvm2_plot.set_data(time_extrap[0:i],uvm2_extrap[0:i])
    uvw1_plot.set_data(time_extrap[0:i],uvw1_extrap[0:i])
    uvw2_plot.set_data(time_extrap[0:i],uvw2_extrap[0:i])
    v_plot.set_data(time_extrap[0:i],v_extrap[0:i])
    if i in imgs_dict.keys():
        ax2.set_title("Image: "+str(imgs_dict[i]))
        plot_img = mpimg.imread(os.path.join('..','uvot','animation_images', imgs_dict[i])) 
        show_img.set_data(plot_img)


anim = FuncAnimation(fig, update, frames=np.arange(0,379), init_func=init, interval=5, repeat=False)
plt.show()