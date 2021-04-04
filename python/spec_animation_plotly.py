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
# Plotly imports
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

def plotly_plots(plot, output_file_name):

    # ------------------------ FIRST PLOT = FLux vs Wavelength ------------------------ 
    # Get data and group by the different times
    df1= pd.read_csv(os.path.join('..','output', 'TEMPLATE', output_file_name+'_template.csv'), header=0)
    time_df = df1.groupby(['MJD'])
    groups=[time_df.get_group(x).sort_values(by=('MJD')).reset_index() for x in time_df.groups]
    num_groups= len(groups)
    time_groups=[round(groups[idx]["MJD"][0], 3) for idx in range(num_groups)]

    groups_list_wavelength = [list(i['Wavelength']) for i in groups]
    groups_list_Flux = [list(i['Flux']) for i in groups]

    # --------------------------- PLOTLY SPECTRUM --------------------------------
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
    # spec.show()

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

    # --------------------------- PLOTLY Light --------------------------------
    light=go.Figure()
    for idx in range(len(interp_funcs)):
        light.add_trace(go.Scatter(x=df['Time (MJD)'], y=df[filter_bands[idx]],
                marker=dict(
                    size=10),
                    mode='lines+markers',showlegend=True, name=filter_bands[idx]))    

    light.update_xaxes(title_text="Time (MJD)")
    light.update_yaxes(title_text="Magnitude")
    light.update_layout(template='plotly_dark')
    light.update_yaxes(autorange="reversed", autotypenumbers="strict")
    # light.show()
    # ------------------------ SECOND PLOT END ------------------------ 

    # --------------------------- PLOTLY convert to html --------------------------------
    output_html_spec_name = output_file_name+'_spec_summaryPlot.html'
    output_html_light_name = output_file_name+'_light_summaryPlot.html'

    pio.write_html(spec, file=r'../output/PLOTS/HTML/'+output_html_spec_name)
    pio.write_html(light, file=r'../output/PLOTS/HTML/'+output_html_light_name)
  
def summary_plot(plot, output_file_name):
    plotly_plots(plot, output_file_name)


if __name__ == "__main__":
    # sn_output_names = [ 'SN2006bp_SNII_series', 'SN2008aw_SNII_series', 'SN2012aw_SNII_series', 'SN2017eaw_SNII_series', 'SN2017cbv_SNIa_series', 'SN2007on_SNIa_series', 'SN2005ke_SNIa_series']
    # sn_names = ['SN2006bp', 'SN2008aw', 'SN2012aw', 'SN2017eaw', 'SN2017cbv', 'SN2007on', 'SN2005ke']
    # for idx, sn in enumerate(sn_names):
    #     summary_plot(sn, sn_output_names[idx])
    summary_plot("SN2007af","SN2007af_SNIa_series")
    # summary_plot("SN2005cs","SN2005cs_uvot_SNII_series")
    # summary_plot("SN2011by","SN2011by_SNIa_series")