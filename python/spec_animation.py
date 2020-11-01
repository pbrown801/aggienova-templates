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

print(s.mean(log_fluxAvg))

gs = gridspec.GridSpec(2, 2)

fig = plt.figure()
fig.set_tight_layout(True)

ax1 = fig.add_subplot(gs[0, 0]) 
ax1.plot([0,1])

ax2 = fig.add_subplot(gs[0, 1]) 
ax2.plot([0,1])
# mpimg image
# ax2.set_xticks([])
# ax2.set_yticks([])
# ax2.set_title("Image: "+str(files_png[0]))
# plot_img = mpimg.imread(os.path.join('animation_images', files_png[0])) 
# show_img=ax2.imshow(plot_img)

ax3 = fig.add_subplot(gs[1, :])
wave_flux,=ax3.plot([],[])

def init():
    ax3.set_xlim(wave[0], wave[-1])
    ax3.set_ylim(log_fluxAvg[0], log_fluxAvg[-1])
    ax3.invert_yaxis()
    return wave_flux,


def update(i):
    wave_flux.set_data(wave[0:i],log_fluxAvg[0:i])
    # ax2.set_title("Image: "+str(files_png[i]))
    # plot_img = mpimg.imread(os.path.join('animation_images', files_png[i])) 
    # show_img.set_data(plot_img)


anim = FuncAnimation(fig, update, frames=np.arange(0,379), init_func=init, interval=100, repeat=False)
plt.show()