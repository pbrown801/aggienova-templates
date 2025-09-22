# this is what Peter can run and get a count rate plot and a 3d plot
# Command to run all:
# python3 run_pipeline.py SN2007af SN2017erp_m1_UVopt.dat y
# Command to run Uvot:
# python3 run_pipeline.py SN2005cs SN2006bp_uvmodel.dat y y
# Command to add template series for mangling:
# python3 run_pipeline.py SN2007af SNIa_series.txt y 
# python3 run_pipeline.py SN2005cs SNII_series.txt y y 

# imports 
import time
import pandas as pd
import numpy as np
from utilities import *
from validation_plotting import *
from Graphing import *
from manipulate_readinuvot import *
#from select_template import sel_template
from spec_animation import summary_plot
import Luminosity_Converter
import argparse
from mpl_toolkits.mplot3d import Axes3D
import scipy
import matplotlib.pyplot as plt
import csv
import os
from pathlib import Path
import math as math
import requests
from contextlib import closing
import string

# this drops the np.float64( from printing in front of float values
np.set_printoptions(legacy="1.25")


'''
might need to use this to run on windows and mac
from https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

data_folder = Path("source_data/text_files/")

file_to_open = data_folder / "raw_data.txt"

f = open(file_to_open)


'''
# Global Variables
desired_filter_list = ['UVW2', 'UVM2', 'UVW1',  'U', 'B', 'V', 'R', 'I']
# J, H, K causes error in example
desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I', 'J', 'H', 'K']
desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V']



def arrange_data(openedcountsfile, template_spectrum, filterlist, reference_epoch_mjd):
    '''
    Use the template spectrum or series to create a mangled spectrum of the flux using the effective areas of each filter bands, 
    the flux of the template spectrum, and the ratio between the sn_name count rates and template spectrum's count rates.
    ''' 
    

    #print("row start")
    if 'series' in template_spectrum:
        spectraname=sel_template(0, "../spectra/"+template_spectrum)
    else:
        spectraname = "../spectra/" + template_spectrum
    
    
    filter_file_list, zeropointlist, pivotlist = filterlist_to_filterfiles(filterlist, spectraname)



    # Akash -- read in the template spectrum.
    # If it starts after wavelength_min or ends before wavelength_max
    # then change these values so that the template spectrum covers the whole range
    # we are making the spectrum for
    # Create wavelength list to extend just before and after the pivot wavelengths
    # of the observed filters
    wavelength_min = 10.0*(math.floor(min(pivotlist)/10.0))-200.0
    wavelength_max = 10.0*(math.ceil(max(pivotlist)/10.0)) + 200.0
    wavelength_nbins = int((wavelength_max-wavelength_min)/10.0+1)

    # print("# of wavelength bins", wavelength_nbins)
    wavelength_list = np.empty(wavelength_nbins)
    for counter in range(wavelength_nbins):
        wavelength_list[counter] = wavelength_min+10.0*counter

    row_count = len(openedcountsfile)
    filter_count = len(filter_file_list)

    reader = csv.reader(openedcountsfile, delimiter=',')
    filters_from_csv = next(reader)[1::2]

    #  openedcountsfile includes a header row
    mjd_list = np.empty((row_count-1))
    epoch_list = np.empty((row_count-1)) 
    flux_matrix = np.empty((row_count-1, wavelength_nbins))
    flux_matrix.fill(np.nan)
    input_counts_list = np.empty((row_count-1, filter_count))
    mangled_counts_list = np.empty((row_count-1, filter_count))

    data = []
    ind = 0

    # Mangled Spectrum
    spec = []

    spectraWavelengths = np.array([])
    flux = np.array([])
    mangled_spec_wave = np.array([])
    mangled_spec_flux = np.array([])
    st = time.time()
    for row in reader:
         
        if len(row) == 0:
            continue
        mjd_list[ind] = np.float64(row[0])
        epoch = np.float64(row[0])-reference_epoch_mjd
        
        epoch_list[ind] = epoch
        

        # The count rates from the counts_array file of the supernova which is the converted magnitudes from the original observations of each epoch of each band
        
        counts_in = np.array(list(map(np.float64, row[1::2])))
        # counterrs_in = np.array(list(map(np.float64,row[2::2]))) #theres gotta be an easier way to do this #just double checking that it's a float -t8

        #mjd_list[ind] = epoch
        # appending counts per filter at epoch
        input_counts_list[ind, :] = counts_in

        #print("row start")
        if 'series' in template_spectrum:
            spectraname=sel_template(epoch, "../spectra/"+template_spectrum)
            print(spectraname)
            spectraWavelengths, flux = clean_spectrum(spectraname)
        else:
         if ind == 0:
            spectraname = "../spectra/" + template_spectrum
            print(spectraname)
            spectraWavelengths, flux = clean_spectrum(spectraname)


        ########### where most of the work happens
        # Function Call 3
        # mangle the spectrum to match the given count rates
        mangled_spec_wave, mangled_spec_flux = mangle_simple(
            spectraWavelengths, flux, filter_file_list, zeropointlist, pivotlist, counts_in)
        spec += [mangled_spec_flux]

        #print("row end")

        #print("interp start")
        f = scipy.interpolate.interp1d(
            mangled_spec_wave, mangled_spec_flux, kind='linear')
        #print("interp end")

        flux_interp = f(wavelength_list)
        flux_matrix[ind, :] = flux_interp
        fill_epoch = [epoch]*wavelength_nbins
        temp_data = [fill_epoch[:], wavelength_list[:], flux_interp[:]]
        data.extend(np.array(temp_data).transpose())

        # Getting counts of mangled template
        temp_template_spec = np.column_stack((wavelength_list[:], flux_interp[:]))
        # print(temp_template_spec)
        # temp_counts = get_counts_multi_filter(temp_template_spec,filter_file_list)
        # the above is what used to be called in case we want to revert
        # The unified total_counts function returns two additional values along with the counts array so using two dummy variables

        # Function Call 4
        # Get the count rates for each filter band for the new spectrum created.
        temp_counts = specarray_to_counts(temp_template_spec, filter_file_list)

        #temp_1,temp_2,temp_counts = total_counts(temp_template_spec,filter_file_list)
        mangled_counts_list[ind, :] = temp_counts
        ind += 1
        
    return  mjd_list, input_counts_list, epoch_list, mangled_counts_list, wavelength_list, flux_matrix, data


##################################################################

##################################################################

##################################################################
def main():
    '''
    Main wrapper for aggienova-templates
    sn_name is a string with the desired supernova name
    filterlist is an array of the filters being used
    Program handles I/O between different functions of the project.
    Output is csv with matrix of wavelength,epoch,flux
    --output/TEMPLATE/[sn_name]_template.csv
    '''
    # Use command line to grab arguments from the user
    parser=argparse.ArgumentParser(description='Process supernova thrrough spectrum template.')
    parser.add_argument('supernova', metavar='supernova',
                        type=str, nargs=1, help='A supernova to process.')
    parser.add_argument('template', metavar='template', type=str,
                        nargs=1, help='A template file to process supernova with.')
    parser.add_argument('csv', metavar='csv', type=str, nargs='?', default='y', choices=[
                        'y', 'n', 'Y', 'N'], help='Save data as csv, y/n.')
    parser.add_argument('uvot', metavar='uvot', type=str, nargs='?', default='n', choices=[
                        'y', 'n', 'Y', 'N'], help='Process only uvot supernova file.')
    args = parser.parse_args()
    # Assign the arguments to variables
    sn_name = args.supernova[0]
    template_spectrum = args.template[0]
    store_as_csv = args.csv[0].upper() == 'Y'
    process_uvot = args.uvot[0].upper() == 'Y'

	#     add as inputs the MW reddening, the host reddening, the distance, the redshift and maybe all of the uncertainties
	#     rather than pulling them from the csv



    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('../input/NewSwiftSNweblist.csv', cur_path)
    with open(new_path, 'r') as f:
        SNList = f.read()
    # print(SNList)

    if 'series' in template_spectrum:
        f=open('../spectra/'+template_spectrum).readline()
        template_spectrum_default=f.strip().split(" ")[1][11:]
    else:
        template_spectrum_default=template_spectrum




    ##############  SELECT THE SOURCE OF THE INPUT DATA: OPEN SUPERNOVA CATALOG OR UVOT
    # If the files are not uvot we call the sn_data_online and check_filter_data
    if(not process_uvot):
        bool_error, bool_online_data=sn_data_online(sn_name)
        if not bool_error:
            check_filter_data(sn_name)
        # Function call 1
        # Convert the magnitudes from the sn data to count rates
        oscmags_to_counts(sn_name, desired_filter_list, template_spectrum_default)

        with open('../output/Test_A.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([1, "Filterlist", desired_filter_list])
        
        orig_file = open('../input/'+sn_name+'_osc.csv', 'r', newline='').readlines()
        orig_file_reader = csv.reader(orig_file, delimiter=',')
        next(orig_file_reader)
        first_obv=next(orig_file_reader)[1]
    else:
        uvotfilepath=('../input/'+sn_name+'_uvotB15.1.dat')
        uvotmags_to_counts(sn_name,template_spectrum)
        #first_obv=uvot(sn_name,"y")
        #sn_name = sn_name+'_uvot'
		#   this could pull from the SOUSA repo
        #orig_file = open('../input/'+sn_name+'_uvotB15.1.dat', 'r', newline='').readlines()
        # print(orig_file)

    output_file_name = sn_name+"_"+template_spectrum

    openedcountsfile = open('../input/COUNTS/'+sn_name+'_countsarray.csv', 'r', newline='').readlines()
    #print("counts from file", openedcountsfile)
    reader = csv.reader(openedcountsfile, delimiter=',')
    #print("reader ",reader)
    #  these are the filters actually present in the csv file
    #  blank columns are removed by observedmags_to_counts

    # This reads in the filter name headers and skips the error columns
    filters_from_csv = next(reader)[1::2]
    first_obs=(next(reader)[0])
    #first_obs=53556.8

    # adjust the reference epoch with the first observed epoch
    reference_epoch_mjd = float(first_obs) - 1 
    #print("reference epoch mjd ", reference_epoch_mjd)

    # Function call 2
    filter_file_list, zeropointlist, pivotlist = filterlist_to_filterfiles(filters_from_csv, template_spectrum_default)

    # Dropping file into output
    # '../output/' + sn_name +
    with open('../output/Test_A.csv', 'a', newline='') as out:
        writer = csv.writer(out)
        writer.writerow([7, "Filter File List", filter_file_list])
        writer.writerow([8, "Zeropoint List", zeropointlist])
        writer.writerow([9, "Pivot List", pivotlist])
   
    mjd_list, input_counts_list, epoch_list, mangled_counts_list, wavelength_list, flux_matrix, data  = arrange_data(openedcountsfile, template_spectrum, filters_from_csv, reference_epoch_mjd)
    #mangled_counts, mjd_list, data, counts_list, mangled_spec_wave, wavelength_list, epoch_list, flux_matrix = mangle_data(openedcountsfile, pivotlist, template_spectrum, filter_file_list, reference_epoch_mjd, zeropointlist)
    
    df = pd.DataFrame(columns=['MJD', 'Wavelength', 'Flux'], data=data)
    
    # format is different than input template (see vega.dat.csv)
    output_file = '../output/TEMPLATE/'+output_file_name+'_template.csv'
    if store_as_csv:
        df.to_csv(output_file, index=False, float_format='%g')
    
    lum_df= Luminosity_Converter.Lum_conv(sn_name, output_file)
    lum_output_file= '../output/TEMPLATE/'+output_file_name+'_lum_template.csv'
    if store_as_csv:
        lum_df.to_csv(lum_output_file, index=False, float_format='%g')

    # Function Call 5
    # Creates an output file of the mangled counts for each filter band for each epoch
    mangled_to_counts(
        output_file_name, filters_from_csv, mangled_counts_list, mjd_list)

    # Convert the mangled count rates to magnitudes
    countrates2mags(output_file_name, template_spectrum_default)

    input_counts_list = np.array(input_counts_list, dtype='float')

    with open('../output/Test_A.csv', 'a', newline='') as out:
        writer = csv.writer(out)
        writer.writerow([10, "Input Wave", wavelength_list])
        #writer.writerow([11, "Mangled Spectrum Flux", spec])
        writer.writerow([11, "Counts List", input_counts_list])

#    filtered_df = df[(df.Wavelength > 1000) & (df.Wavelength < 10000) & (df.MJD < 54330)] #filters data to remove outliers
#    filtered_df.to_csv('../output/'+sn_name+'_filtered.csv',index=False)

# The bool statment was to ensure that we only delete the temporary online data file we downloaded.
#    if(not process_uvot):
#        if bool_online_data == True:
#            print("Removing" + sn_name + "_osc.csv from input folder")
#            os.remove('../input/'+sn_name+'_osc.csv')
# Commented out so we keep the files we make, 
# but they are on the gitignorelist so that they don't get committed back

    '''
    Testing output
    '''
    print("run finished")

    #  3d plot
    plots3d(sn_name, output_file_name, wavelength_list, epoch_list, flux_matrix, template_spectrum)
    
    # uses mangledmagsarray

    # summary animation plot with light curves and spectra in spec_animation.py
    '''
    Fix plots changing size as animating
    '''
    
    if "uvot" in output_file_name:
        summary_plot(sn_name, output_file_name, True, True, False, 750, False)
    else:
        summary_plot(sn_name, output_file_name, True, True, True, 750, False)
    


if __name__ == "__main__":
    main()
