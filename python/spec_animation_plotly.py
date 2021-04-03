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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def initialize_plots(plot, output_file_name, isStatic):

    # ------------------------ FIRST PLOT = FLux vs Wavelength ------------------------ 
    # Get data and group by the different times
    df1= pd.read_csv(os.path.join('..','output', 'TEMPLATE', output_file_name+'_template.csv'), header=0)
    time_df = df1.groupby(['MJD'])
    groups=[time_df.get_group(x).sort_values(by=('MJD')).reset_index() for x in time_df.groups]
    num_groups= len(groups)
    time_groups=[round(groups[idx]["MJD"][0], 3) for idx in range(num_groups)]

    groups_list_wavelength = [list(i['Wavelength']) for i in groups]
    groups_list_Flux = [list(i['Flux']) for i in groups]

    # fig = make_subplots(rows=2, cols=1, subplot_titles=("Flux vs Wavelength", "Magnitude vs Time"))
    spec=go.Figure()
    for i in range(num_groups):
        spec.add_trace(go.Scatter(x=groups_list_wavelength[i], y=groups_list_Flux[i],
                marker=dict(
                    size=4),
                    mode='markers',
                    name=time_groups[i]))
    # fig.update_layout(
    # title_text="Flux vs Wavelength", template='plotly_dark')
    spec.update_xaxes(title_text="Wavelength (angstroms)")
    spec.update_yaxes(title_text="Log(flux)+constant")
    spec.update_layout(template='plotly_dark')
    spec.update_yaxes(tickformat=".2g")
    spec.show()

    # ------------------------ FIRST PLOT END ------------------------ 

    # ------------------------ SECOND PLOT = Magnitude vs Time (MJD) Plot ------------------------ 
    # Get data from uvot function that returns the manipulated combined data from the original .dat file 
    # The combined data is simply each row is the appropriate time the data was measured and the associated band magnitude measurements
    df=pd.read_csv('../output/MAGS/'+output_file_name+'_mangledmagsarray.csv')

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

    # # Plot the interpolated plots that are smooth because of high enumeration of values inbetween the times given
        # ax2.plot(time_extrap,func, label=filter_bands[idx])

    times = [df['Time (MJD)'][0:(i+1)] for i in range(num_groups)]
    filter_ = []
    light=go.Figure()

    for idx,func in enumerate(interp_funcs):
        light.add_trace(go.Scatter(x=df['Time (MJD)'], y=df[filter_bands[idx]],
                marker=dict(
                    size=10),
                    mode='lines+markers',showlegend=True, name=filter_bands[idx]))    

    light.update_xaxes(title_text="Time (MJD)")
    light.update_yaxes(title_text="Magnitude")
    light.update_layout(template='plotly_dark')
    light.update_yaxes(autorange="reversed", autotypenumbers="strict")
    # fig.update_layout(title_text="Summary Plot", template='plotly_dark')
    # light.show()

    # ------------------------ SECOND PLOT END ------------------------ 

    return 

def summary_plot(plot, output_file_name, save, show, isStatic, interval_param=1):
    initialize_plots(plot, output_file_name, isStatic)


if __name__ == "__main__":
    summary_plot("SN2007af","SN2007af_SNIa_series", True, True, True, 500)