# this is what Peter can run and get a count rate plot and a 3d plot
# python3 run_pipeline.py SN2007af SN2017erp_hst_20170629.dat y

#  take an input spectrum
import pandas as pd
import numpy as np
from utilities import *
from mangle_simple import *
from validation_plotting import *
import argparse
from observedmags_to_counts import *
from filterlist_to_filterfiles import *
from mangled_to_counts import *
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

    parser.add_argument('supernova', metavar='supernova', type=str, nargs=1, help='A supernova to process.')
    parser.add_argument('template', metavar='template', type=str, nargs=1, help='A template file to process supernova with.')
    parser.add_argument('csv', metavar='csv', type=str, nargs='?', default='y', choices=['y','n','Y','N'], help='Save data as csv, y/n.')

    args = parser.parse_args()

    sn_name = args.supernova[0] #assign sn name at beginning and look for that file as an input
    template_spectrum = args.template[0] #assign a template spectrum to use
    # dat_to_csv(args.template[0])
    store_as_csv = args.csv[0].upper()=='Y'

    reference_epoch_mjd=0.0

    #####              these are the filters we will check for from the OSC csv file
    # 
    desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I', 'J', 'H', 'K']
    # 
    observedmags_to_counts(sn_name,desired_filter_list)

    inFile = '../input/'+sn_name+'_countsarray'+'.csv' #gets input count rates from existing file

    file = open(inFile).readlines()
    reader = csv.reader(file,delimiter = ',')

    #  these are the filters actually present in the csv file
    #  blank columns are removed by observedmags_to_counts

    filters_from_csv = next(reader)[1:]

    filter_file_list = filterlist_to_filterfiles(filters_from_csv)

    row_count = sum(1 for row in file)
    filter_count = len(filter_file_list)

    mjd_list = np.empty((row_count-1)) #empty list to hold time values
    flux_matrix = np.empty((1,row_count-1)) #empty matrix to hold flux values
    flux_matrix.fill(np.nan)

    wavelengths = np.empty(1)
    counts_list = np.empty((row_count-1,filter_count))
    mangled_counts = np.empty((row_count-1,filter_count))

    ind = 0
    for row in reader:
        print(row_count-1-ind)
        if len(row) == 0:
            continue
        epoch = np.float64(row[0])-reference_epoch_mjd
        counts_in = np.array(list(map(np.float64,row[1:]))) #theres gotta be an easier way to do this #just double checking that it's a float -t8

        mjd_list[ind]=epoch
        counts_list[ind,:] = counts_in #appending counts per filter at epoch

        #mangle the spectrum to match the given count rates
        mangled_spec_wave, mangled_spec_flux = mangle_simple(template_spectrum, filter_file_list, counts_in) 

        if ind == 0:
            wavelengths =mangled_spec_wave #why are we only doing this once? The values of wavelength change every increment

            #flux_matrix = np.resize(flux_matrix,(len(mangled_spec_flux),row_count-1)) #OLD TEST SPEED
            flux_matrix = np.empty((len(mangled_spec_flux),row_count-1)) #NEW TEST SPEED
            flux_matrix.fill(np.nan)

        flux_matrix[:,ind] = mangled_spec_flux

        #Getting counts of mangled template
        temp_temp_spec =np.column_stack((wavelengths,mangled_spec_flux))
        temp_counts = get_counts_multi_filter(temp_temp_spec,filter_file_list)
        mangled_counts[ind,:] = temp_counts

        ind+=1

    mangled_to_counts(sn_name,filters_from_csv,mangled_counts,mjd_list)
    df= pd.DataFrame(index = wavelengths,data = flux_matrix,columns= mjd_list)

    output_file = '../output/'+sn_name+'_template.csv' #format is different than input template (see vega.dat.csv)
    if store_as_csv:
        df.to_csv(output_file,index=True,float_format='%g')

    counts_list = np.array(counts_list,dtype='float')
    # filter_curves_list_no_format = [x.split('_')[0] for x in filter_curves_list_no_format]

    # filtered_df = df[(df.Wavelength > 1000) & (df.Wavelength < 10000) & (df.Epoch < 54330)]
    # output_3d = '../output/'+sn_name+'_3d.csv'
    # filtered_df.to_csv(output_3d,index=False) #comment this if you already have your df or dont want to save a filtered version FUTURE: flag to do this

    validation_plotting(filters_from_csv,counts_list,mjd_list) 
#    validation_plotting(filter_curves_list_no_format,counts_list,mjd_list) #Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis

    from plot_3d import plot_3D
    # filtered_df = pd.read_csv(output_file,index_col=0,header=0) #uncomment this if you have a saved df you just want to read and plot in 3d
    # mjd_list = np.array(filtered_df.columns.values,dtype='float')
    # wavelengths = np.array(filtered_df.index.values,dtype='float')
    # flux_matrix = np.array(filtered_df.values,dtype='float')
    plot_3D(mjd_list,wavelengths,flux_matrix,sn_name)
