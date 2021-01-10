# imports
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import os
import time
from manipulate_readinuvot import uvot
import scipy 
from scipy.interpolate import interp1d
import matplotlib.image as mpimg

def initialize_plots(plot):
    # Define the gridspec which is 2 rows by 3 columns and the figure for the matplotlib plot
    gs = gridspec.GridSpec(nrows=2, ncols=7)
    fig = plt.figure(figsize=(15,8))
    fig.set_tight_layout(True)

    # Set the three different plots to the specific locations in the gridspec
    # First Plot - First Row, All Columns
    ax1 = fig.add_subplot(gs[0, :4])
    # Second Plot - Last row, ALl available columns
    ax2 = fig.add_subplot(gs[-1, :4]) 
    # Third Plot - Last Row, 3rd column 
    ax3 = fig.add_subplot(gs[0:, 4:]) 

    ax2.invert_yaxis()

    # ------------------------ FIRST PLOT = FLux vs Wavelength ------------------------ 
    # Get data and group by the different times
    df1= pd.read_csv(os.path.join('..','output', plot+'_template.csv'), header=0)
    time_df = df1.groupby(['MJD'])
    groups=[time_df.get_group(x).sort_values(by=('MJD')).reset_index() for x in time_df.groups]
    num_groups= len(groups)
    time_groups=[groups[idx]["MJD"][0] for idx in range(num_groups)]

    # Invisibly set the plot with all the data then overwrite it with the animation
    for i in range(num_groups):
        if i==0:
            ax1.plot(groups[i]['Wavelength'],groups[i]['Flux'], 'wo', markersize=1, label=" "*(len(str(time_groups[i]))+6))
        else:
            ax1.plot(groups[i]['Wavelength'],groups[i]['Flux'], 'wo', markersize=1)

    # Plot empty plots for each time that will be used by funcAnimation and set_data function to plot the data at certain frames
    times_plots=[]
    for i in range(num_groups):
            time_var='time'+str(i)
            time_var,=ax1.plot([],[], 'o',  markersize=1)
            times_plots.append(time_var)


    # Plot Settings
    ax1.set_xlabel('Wavelength (angstroms)')
    ax1.set_ylabel('log(flux)+constant')
    ax1.set_title('Flux vs Wavelength')

    # Get the labels for the plot legend 
    handles,labels=ax1.get_legend_handles_labels()
    # Add the legend to plot 2 outside of the plot area
    ax1.legend(handles, labels,bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)

    # ------------------------ FIRST PLOT END ------------------------ 

    # ------------------------ SECOND PLOT = Magnitude vs Time (MJD) Plot ------------------------ 
    # Get data from uvot function that returns the manipulated combined data from the original .dat file 
    # The combined data is simply each row is the appropriate time the data was measured and the associated band magnitude measurements
    df=pd.read_csv('../output/'+plot+'_mangledmagsarray.csv')

    # Interpolate linearly for the missing NaN values in the each band that has Nan values. We do not do it for band error measurements
    filter_bands = list(filter(lambda i: ('Time' not in i and 'err' not in i),list(df.columns)))
    for band in filter_bands:
        nan_idx =list(df[band].index[df[band].apply(np.isnan)])
        if len(nan_idx)!=0:
            val_idx = [df[band][i] for i in range(len(df[band])) if i not in nan_idx]
            replace_nan_idx_times = [df['Time (MJD)'][i] for i in range(len(df[band])) if i in nan_idx]
            df_temp = df[df[band].isin(val_idx)] 
            nan_interp_func = interp1d(df_temp['Time (MJD)'], df_temp[band], kind='linear', fill_value='extrapolate')
            for idx,i in enumerate(nan_idx):
                df[band][i] = nan_interp_func(replace_nan_idx_times[idx])

    # Create the time interpolation function for each band
    interp_func_templates = [interp1d(df['Time (MJD)'], df[band], kind='cubic') for band in filter_bands]
    # Get a 1000 time points between the start and end times
    time_extrap = np.linspace(df['Time (MJD)'][0], df['Time (MJD)'].iloc[-1], num=1000, endpoint=True) 
    # Interpolate magnitude for each band  for each of the 1000 time points
    interp_funcs = [i(time_extrap) for i in interp_func_templates]     

    # Plot the interpolated plots that are smooth because of high enumeration of values inbetween the times given
    for idx,func in enumerate(interp_funcs):
        ax2.plot(time_extrap,func, label=filter_bands[idx])

    # Used to update the points given to us in original data on top of the magnitude vs time plot
    bands_plots=[]
    for bands in filter_bands:
        bands_var = bands + '_plot'
        bands_var,=ax2.plot([],[], 'ko',  markersize=3)
        bands_plots.append(bands_var)

    # Plot Settings
    ax2.set_xlabel('Time (MJD)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Magnitude vs Time')
    # Get the labels for the plot legend 
    handles,labels=ax2.get_legend_handles_labels()
    # Add the legend to plot 2 outside of the plot area
    ax2.legend(handles, labels,bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    # ------------------------ SECOND PLOT END ------------------------ 

    # # ------------------------ THIRD PLOT = Image Globals  ------------------------ 
    ax3.set_xticks([])
    ax3.set_yticks([])

    files=os.listdir(os.path.join('..','uvot','animation_images'))

    # # ------------------------ THIRD PLOT END ------------------------ 

    return fig,ax1, ax2, ax3, times_plots, groups, time_groups, bands_plots,df, filter_bands, num_groups, files
# ------------------------ Animation Function --------------------
def animation(plot,fig,ax1, ax2, ax3, times_plots, groups, time_groups, bands_plots,df, filter_bands, num_groups, files, interval_time, static):

    def init():
        # Third plot initialization
        global files_png, web_img, show_img

        ax3.set_xticks([])
        ax3.set_yticks([])

        try:
            if static:
                if "uvot"in plot:
                    web_img=os.path.join('..', 'images', 'website_images', plot+'.png')
                else:
                    web_img=os.path.join('..', 'images', 'website_images', plot+'_uvot.png')
                # Initialize the plot to the first image in the beginning
                ax3.set_title(str(plot))
                plot_img = mpimg.imread(web_img) 
                show_img=ax3.imshow(plot_img)
            else:
                if "uvot"in plot:
                    files_png = [f for f in files if (f.endswith('.png') and f.startswith(plot[:-5]))]

                else:
                    files_png = [f for f in files if (f.endswith('.png') and f.startswith(plot))]
                # Initialize the plot to the first image in the beginning
                ax3.set_title(str(files_png[0][:-4]))
                plot_img = mpimg.imread(os.path.join('..','uvot','animation_images', files_png[0])) 
                show_img=ax3.imshow(plot_img)
        except FileNotFoundError:
            print("No image file for the supernova")

    def update(i):
        if i==num_groups:
            time.sleep(1.75)
        else:
                # --------- Update the ax1 plot with the flux vs wavelength for each time mjd ---------
                # Clear the plot flux vs wavelength
                if i ==0:
                        for idx in range(len(times_plots)):
                            times_plots[idx].set_data([], [])  
                            times_plots[idx].set_label("")  
                # Plot the FLux and wavelength values up to the ith time. This is so that it appears as if we are adding on top of the previous plot.
                for idx in range(i+1):
                    times_plots[idx].set_data(groups[idx]['Wavelength'], groups[idx]['Flux'])
                    times_plots[idx].set_label(time_groups[idx])

                                # Get the labels for the plot legend 
                handles,labels=ax1.get_legend_handles_labels()
                # Add the legend to plot 2 outside of the plot area
                ax1.legend(handles[1:], labels[1:],bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
               
               # --------- Update the ax2 plot with the points based on the time(MJD) ---------
                # Plot the original points up to the ith time based on the frame so that it appears as if we are adding one more plot of points each time.
                for idx,plot in enumerate(bands_plots):
                    plot.set_data(df['Time (MJD)'][0:(i+1)], df[filter_bands[idx]][0:(i+1)])

                # --------- Update the ax3 plot with the image corresponding to each MJD ---------
                if not(static):
                    ax3.set_title(str(files_png[i]))
                    plot_img = mpimg.imread(os.path.join('..','uvot','animation_images', files_png[i])) 
                    show_img.set_data(plot_img)                    

    return FuncAnimation(fig, update, init_func=init, frames=np.arange(0,num_groups+1), interval=interval_time, repeat=True)

def main(plot,save, show, isStatic, interval_param=1):
    fig,ax1, ax2, ax3, times_plots, groups, time_groups, bands_plots,df, filter_bands, num_groups, files=initialize_plots(plot)
    anim=animation(plot,fig,ax1, ax2, ax3, times_plots, groups, time_groups, bands_plots,df, filter_bands, num_groups, files, interval_param, isStatic)
    if save:
        anim.save(r'../output/'+plot+'_animation.gif', writer="imagemagick")
        fig.savefig(r'../output/'+plot+'_summaryPlot.png')
    if show:
        plt.show()


if __name__ == "__main__":
    main("SN2005cs_uvot", True, True, False, 500)