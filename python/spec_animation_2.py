# imports
import matplotlib.pyplot as plt
# import pandas as pd
# import csv
# import math
from pathlib import Path
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import os
import time
# import statistics as s
from manipulate_readinuvot import uvot
import scipy 
from scipy.interpolate import interp1d
import matplotlib.image as mpimg

# Global plot variables 
# Define the gridspec which is 2 rows by 3 columns and the figure for the matplotlib plot
gs = gridspec.GridSpec(2, 3)
fig = plt.figure(figsize=(10,5))
fig.set_tight_layout(True)


# Set the three different plots to the specific locations in the gridspec
# First Plot - First Row, All Columns
ax1 = fig.add_subplot(gs[0, :])
# Second Plot - Last row, ALl available columns
ax2 = fig.add_subplot(gs[-1, :-1]) 
# Third Plot - Last Row, 3rd column 
ax3 = fig.add_subplot(gs[-1, 2]) 

ax1.invert_yaxis()
ax2.invert_yaxis()




# ------------------------ SECOND PLOT = Magnitude vs Time (MJD) Plot ------------------------ 
# Get data from uvot function that returns the manipulated combined data from the original .dat file 
# The combined data is simply each row is the appropriate time the data was measured and the associated band magnitude measurements
plots = "SN2005cs"
df = uvot(plots, 'y') 

# print(df)
# print(df['UVM2'])

f_b= interp1d(
        df['Time (MJD)'], df['B'], kind='cubic')
f_u= interp1d(
        df['Time (MJD)'], df['U'], kind='cubic')
f_uvm2= interp1d(
        df['Time (MJD)'], df['UVM2'], kind='cubic')
f_uvw1= interp1d(
        df['Time (MJD)'], df['UVW1'], kind='cubic')
f_uvw2= interp1d(
        df['Time (MJD)'], df['UVW2'], kind='cubic')
f_v= interp1d(
        df['Time (MJD)'], df['V'], kind='cubic')

time_extrap = np.linspace(df['Time (MJD)'][0], df['Time (MJD)'].iloc[-1], num=1000, endpoint=True)       
b_extrap = f_b(time_extrap)
u_extrap = f_u(time_extrap)
# uvm2_extrap = f_uvm2(time_extrap) # Has NaN values so cannot interpolate
uvw1_extrap = f_uvw1(time_extrap)
# uvw2_extrap = f_uvw2(time_extrap) # Has Nan Values so cannot interpolate
v_extrap = f_v(time_extrap)

ax2.plot(time_extrap, b_extrap, label="B")
ax2.plot(time_extrap, u_extrap, label="U")
# ax2.plot(time_extrap, uvm2_extrap, label="UVM2")
ax2.plot(time_extrap, uvw1_extrap, label="UVW1")
# ax2.plot(time_extrap, uvw2_extrap, label="UVW2")
ax2.plot(time_extrap, v_extrap, label="V")
ax2.set_xlabel('Time (MJD)')
ax2.set_ylabel('Magnitude')
# Used to update the points ontop of the magnitude vs time plot
B_plot,=ax2.plot([], [], 'ko', markersize=5)
U_plot,=ax2.plot([], [], 'ko', markersize=5)
UVM2_plot,=ax2.plot([], [], 'ko', markersize=5)
UVW1_plot,=ax2.plot([], [], 'ko', markersize=5)
UVW2_plot,=ax2.plot([], [], 'ko', markersize=5)
V_plot,=ax2.plot([], [], 'ko', markersize=5)


# ------------------------ SECOND PLOT END ------------------------ 

# ------------------------ THIRD PLOT = Image ------------------------ 
ax3.set_xticks([])
ax3.set_yticks([])
files=os.listdir(os.path.join('..','uvot','animation_images'))
files_png = [f for f in files if (f.endswith('.png') and f.startswith("SN2005cs"))]

# Initialize the plot to the first image in the beginning
ax3.set_title(str(files_png[0][:-4]))
plot_img = mpimg.imread(os.path.join('..','uvot','animation_images', files_png[0])) 
show_img=ax3.imshow(plot_img)
# ------------------------ THIRD PLOT END ------------------------ 
def animation(fig, ax1, ax2, ax3):

    def update(i):
        if i==7:
            time.sleep(3)
        else:
            # ----- Update the ax2 plot with the points based on the time(MJD) -----

            B_plot.set_data(df['Time (MJD)'][0:(i+1)], df['B'][0:(i+1)])
            U_plot.set_data(df['Time (MJD)'][0:(i+1)], df['U'][0:(i+1)])
            # UVM2_plot.set_data(df['Time (MJD)'][0:(i+1)], df['UVM2'][0:(i+1)])
            UVW1_plot.set_data(df['Time (MJD)'][0:(i+1)], df['UVW1'][0:(i+1)])
            # UVW2_plot.set_data(df['Time (MJD)'][0:(i+1)], df['UVW2'][0:(i+1)])
            V_plot.set_data(df['Time (MJD)'][0:(i+1)], df['V'][0:(i+1)]) 

            # ------ Update the ax3 plot with the image corresponding to each MJD -----
            ax3.set_title(str(files_png[i]))
            plot_img = mpimg.imread(os.path.join('..','uvot','animation_images', files_png[i])) 
            show_img.set_data(plot_img)

    return FuncAnimation(fig, update, frames=np.arange(0,8), interval=500, repeat=True)

def main():
    anim=animation(fig,ax1, ax2, ax3)
    # Get the labels for the plot legend 
    handles,labels=ax2.get_legend_handles_labels()
    # Add the legend to plot 2 outside of the plot area
    ax2.legend(handles, labels,bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    plt.show()



if __name__ == "__main__":
    main()