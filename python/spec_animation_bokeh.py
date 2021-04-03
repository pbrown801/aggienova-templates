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
from bokeh.plotting import figure, output_file, show, ColumnDataSource, output_file, save
from bokeh.io import curdoc
from bokeh.palettes import Turbo256
from bokeh.layouts import gridplot
import random
import bokeh.plotting
import bokeh.layouts
import bokeh.embed
from bokeh.embed import json_item, file_html, components
from bokeh.resources import CDN
import json

def random_color(num):
    random_color_arr = [random.sample(list(split_color_arr),1)[0]  for split_color_arr in np.array_split(Turbo256[20:], num)]
    random.shuffle(random_color_arr)
    return random_color_arr

def bokeh_plots(plot, output_file_name):
    curdoc().theme = 'dark_minimal'
    # ------------------------ FIRST PLOT = FLux vs Wavelength ------------------------ 
    # Get data and group by the different times
    df1= pd.read_csv(os.path.join('..','output', 'TEMPLATE', output_file_name+'_template.csv'), header=0)
    time_df = df1.groupby(['MJD'])
    groups=[time_df.get_group(x).sort_values(by=('MJD')).reset_index() for x in time_df.groups]
    num_groups= len(groups)
    time_groups=[round(groups[idx]["MJD"][0], 3) for idx in range(num_groups)]

    spec = figure(
        title = 'Flux vs Wavelength',
        x_axis_label = 'Wavelength (angstroms)', 
        y_axis_label = 'log(flux)+constant',
        plot_width=1100, plot_height=500
    )
    groups_list_wavelength = [list(i['Wavelength']) for i in groups]
    groups_list_Flux = [list(i['Flux']) for i in groups]
    for t, w, f, color,  in zip(time_groups, groups_list_wavelength, groups_list_Flux, random_color(num_groups)):
        spec.circle(w, f, color=color, alpha=0.8, muted_color=color, muted_alpha=0.075, legend_label=str(t))
    
    spec.legend.click_policy="hide"
    spec.add_layout(spec.legend[0], 'right')
    
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
    # for idx,func in enumerate(interp_funcs):
    #     ax2.plot(time_extrap,func, label=filter_bands[idx])

    light = figure(
        title = 'Magnitude vs Time',
        x_axis_label = 'Time (MJD)', 
        y_axis_label = 'Magnitude',
    )
    
    x= [list(df['Time (MJD)']) for fb in filter_bands] 
    y = [ list(df[fb]) for fb in filter_bands]

    

    # for idx,func in enumerate(interp_funcs):
    for filter_legend, time, bands, color,  in zip(filter_bands, x, y, random_color(len(filter_bands))):
        light.line(time, bands, color=color, legend_label=filter_legend)
        light.circle(time, bands, color=color, alpha=0.8, muted_color=color, muted_alpha=0.075, legend_label=filter_legend)
    
    light.legend.click_policy="hide"
    light.add_layout(light.legend[0], 'right')
    light.y_range.flipped = True
    spec.sizing_mode = 'stretch_both'
    light.sizing_mode = 'stretch_both'    
    grid = gridplot([[spec], [light]], sizing_mode='stretch_both', toolbar_options=dict(logo=None), toolbar_location=None)
    # output_file(r'../output/PLOTS/HTML/'+output_file_name+'_summaryPlot.html')
    # save(grid)
    # print(file_html(grid, CDN,r'../output/PLOTS/HTML/'+output_file_name+'_summaryPlot.html'))
    # plots={'spec':spec, 'light': light}
    # scripts,div = components(plots)
    # print(scripts)
    # print(div)
    # item_text = json.dumps(json_item(grid, output_file_name+'_summaryPlot'))
    # print(item_text)
    return spec, light
    # show(grid)    # ------------------------ SECOND PLOT END ------------------------ 

def summary_plot(plot, output_file_name):
    bokeh_plots(plot, output_file_name)


if __name__ == "__main__":
    # summary_plot("SN2007af","SN2007af_SNIa_series")
    summary_plot("SN2005cs","SN2005cs_uvot_SNII_series")