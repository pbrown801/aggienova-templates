#  take an input spectrum
import pandas as pd
import numpy as np
from utilities import *
from mangle_simple import *
from validation_plotting import *
import argparse
from observedmags_to_counts import *
from filterlist_to_filterfiles import *
'''
Main wrapper for aggienova-templates
sn_name is a string with the desired supernova name
filterlist is an array of the filters being used
Program handles I/O between different functions of the project.
Output is csv with matrix of wavelength,epoch,flux
--output/[sn_name]_template.csv
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process supernova through spectrum template.')

    parser.add_argument('supernova', metavar='supernova', type=str, nargs='+', help='A supernova to process.')
    parser.add_argument('template', metavar='template', type=str, nargs='+', help='A template file to process supernova with.')
    parser.add_argument('csv', metavar='csv', type=str, nargs='?', default='y', choices=['y','n','Y','N'], help='Save data as csv, y/n.')

    args = parser.parse_args()

    sn_name = args.supernova[0] #assign sn name at beginning and look for that file as an input
    template_spectrum = args.template[0] #assign a template spectrum to use
    store_as_csv = args.csv[0]==True
    filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I']
    filter_file_list = filterlist_to_filterfiles(filterlist)
    observedmags_to_counts(sn_name,filterlist)
    inFile = '../input/'+sn_name+'_countsarray'+'.csv'


    file = open(inFile).readlines()
    reader = csv.reader(file,delimiter = ',')
    filter_curves_list_no_format = next(reader)[1:]
    filter_curves_list = list(map('../filters/{0}'.format, filter_file_list))

    row_count = sum(1 for row in file)
    filter_count = len(filter_curves_list)
    mjd_list = np.empty((row_count-1))
    flux_matrix = np.empty((1,row_count-1))
    flux_matrix.fill(np.nan)
    wavelengths = np.empty(1)
    counts_list = np.empty((row_count-1,filter_count))
    ind = 0
    for row in reader:
        if len(row) == 0:
            continue
        epoch = np.float64(row[0])-0
        counts_in = np.array(list(map(np.float64,row[1:]))) #theres gotta be an easier way to do this #just double checking that it's a float -t8
        mjd_list[ind]=epoch
        # print(mjd_list[ind])
        counts_list[ind,:] = counts_in

        mangled_spec_wave, mangled_spec_flux = mangle_simple(template_spectrum, filter_curves_list, counts_in) #mangle the spectrum to match the given count rates
        if ind == 0:
            wavelengths =mangled_spec_wave
            flux_matrix = np.resize(flux_matrix,(len(mangled_spec_flux),row_count-1))
        flux_matrix[:,ind] = mangled_spec_flux
        # mangling outputs spectrum that matches input counts by multiplying func by og spec

        ind+=1

    df= pd.DataFrame(index = wavelengths,data = flux_matrix,columns= mjd_list)

    output_file = '../output/'+sn_name+'_template.csv'
    if store_as_csv:
        df.to_csv(output_file,index=True,float_format='%g')

    counts_list = np.array(counts_list,dtype='float')
    filter_curves_list_no_format = [x.split('_')[0] for x in filter_curves_list_no_format]

    # filtered_df = df[(df.Wavelength > 1000) & (df.Wavelength < 10000) & (df.Epoch < 54330)]
    # output_3d = '../output/'+sn_name+'_3d.csv'
    # filtered_df.to_csv(output_3d,index=False) #comment this if you already have your df or dont want to save a filtered version FUTURE: flag to do this

    validation_plotting(filter_curves_list_no_format,counts_list,mjd_list) #Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis

    from plot_3d import plot_3D
    # filtered_df = pd.read_csv(output_file,index_col=0,header=0) #uncomment this if you have a saved df you just want to read and plot in 3d
    # mjd_list = np.array(filtered_df.columns.values,dtype='float')
    # wavelengths = np.array(filtered_df.index.values,dtype='float')
    # flux_matrix = np.array(filtered_df.values,dtype='float')
    plot_3D(mjd_list,wavelengths,flux_matrix,sn_name)
