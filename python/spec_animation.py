# imports
import matplotlib.pyplot as plt
import pandas as pd
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
gs = gridspec.GridSpec(nrows=2, ncols=7)
fig = plt.figure(figsize=(10,5))
fig.set_tight_layout(True)


# Set the three different plots to the specific locations in the gridspec
# First Plot - First Row, All Columns
ax1 = fig.add_subplot(gs[0, :4])
# Second Plot - Last row, ALl available columns
ax2 = fig.add_subplot(gs[-1, :4]) 
# Third Plot - Last Row, 3rd column 
ax3 = fig.add_subplot(gs[0:, 4:]) 

ax1.invert_yaxis()
ax2.invert_yaxis()
plots = "SN2005cs"

# ------------------------ FIRST PLOT = FLux vs Wavelength ------------------------ 
df1= pd.read_csv(os.path.join('..','output', 'SN2005cstemplate.csv'), header=0)
time_df = df1.groupby(['MJD'])
groups=[time_df.get_group(x).sort_values(by=('MJD')) for x in time_df.groups]

times_plots=[]
for i in range(len(groups)):
        time_var='time'+str(i)
        time_var,=ax1.plot([],[], 'o',  markersize=1)
        times_plots.append(time_var)

# Initialize the first plot to the first time mjd flux vs wavelength
ax1.plot(groups[0]['Wavelength'],groups[0]['Flux'], 'o',   markersize=1)

# Plot Settings
ax1.set_xlabel('Wavelength (angstroms)')
ax1.set_ylabel('log(flux)+constant')
ax1.set_title('Flux vs Wavelength')
# ------------------------ FIRST PLOT END ------------------------ 

# ------------------------ SECOND PLOT = Magnitude vs Time (MJD) Plot ------------------------ 
# Get data from uvot function that returns the manipulated combined data from the original .dat file 
# The combined data is simply each row is the appropriate time the data was measured and the associated band magnitude measurements
plots = "SN2005cs"
df = uvot(plots, 'y') 

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

# Used to update the points ontop of the magnitude vs time plot
B_plot,=ax2.plot([], [], 'ko', markersize=5)
U_plot,=ax2.plot([], [], 'ko', markersize=5)
UVM2_plot,=ax2.plot([], [], 'ko', markersize=5)
UVW1_plot,=ax2.plot([], [], 'ko', markersize=5)
UVW2_plot,=ax2.plot([], [], 'ko', markersize=5)
V_plot,=ax2.plot([], [], 'ko', markersize=5)

# Plot Settings
ax2.set_xlabel('Time (MJD)')
ax2.set_ylabel('Magnitude')
ax2.set_title('Magnitude vs Time')
# Get the labels for the plot legend 
handles,labels=ax2.get_legend_handles_labels()
# Add the legend to plot 2 outside of the plot area
ax2.legend(handles, labels,bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
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
def animation(fig, ax1, ax2, ax3, times_plots):

    def update(i):
        if i==7:
            time.sleep(3)
        else:
                # ----- Update the ax1 plot with the flux vs wavelength for each time mjd -----
                # Clear the plot flux vs wavelength
                if i ==0:
                        for idx in range(len(times_plots)):
                                times_plots[idx].set_data([], [])  
                for idx in range(i+1):
                        times_plots[idx].set_data(groups[idx]['Wavelength'], groups[idx]['Flux'])
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

    return FuncAnimation(fig, update, frames=np.arange(0,8), interval=1000, repeat=True)

def main():
    anim=animation(fig,ax1, ax2, ax3, times_plots)
    plt.show()



if __name__ == "__main__":
    main()