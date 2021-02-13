# this is what Peter can run and get a count rate plot and a 3d plot
# Command to run without Uvot:
# python3 run_pipeline.py SN2007af SN2017erp_m1_UVopt.dat y
# Command to run Uvot:
# python3 run_pipeline.py SN2005cs SN2006bp_uvmodel.dat y y

# imports 
import time
import pandas as pd
import numpy as np
from mangle_simple import *
from utilities import *
from validation_plotting import *
from Graphing import *
from manipulate_readinuvot import *
import argparse
from observedmags_to_counts import *
from filterlist_to_filterfiles import *
from mangled_to_counts import *
from mpl_toolkits.mplot3d import Axes3D
import scipy
import matplotlib.pyplot as plt
import csv


# Global Variables
desired_filter_list = ['UVW2', 'UVM2', 'UVW1',  'U', 'B', 'V', 'R', 'I']
# J, H, K causes error in example
#desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I', 'J', 'H', 'K']

'''
If the data for the sn_name does not exist we retrieve it frrom the supernova catalog at api.sne.space.
Returns two boolean values:
bool_online_data - If we have sucessfully retrieve the online data we make bool_online_data True otherwise false.
bool_error -  If we have an error in gathering the specified superrnova we make bool_error True otherwise false
'''
def sn_data_online(sn_name):
    bool_error = False
    bool_online_data = False
    for root, dirs, files in os.walk('../input'):
        if sn_name + "_osc.csv" not in files:
            print(sn_name+" not found - Retrieving data from supernova catalog")
            # Url of the csv file from the supernova catalog
            df = pd.read_csv("https://api.sne.space/" + sn_name +
                            "/photometry/time+magnitude+e_magnitude+upperlimit+band+instrument+telescope+source?format=csv&time&magnitude")
            df.to_csv('../input/'+sn_name+'_osc.csv', index=False)
            x = df.shape
            if (x[0] > 10):
                bool_online_data = True
                df.to_csv('../input/'+sn_name+'_osc.csv', index=False)
            else:
                print("Error too few rows. " + sn_name +
                    " data from catalog below:")
                print(df)
                bool_error = True
    return bool_error, bool_online_data

'''
Nathan's code: Check if filter data exists for current supernova before running observed mags
'''
def check_filter_data(sn_name):
    csv_name = str(sn_name) + "_osc.csv"
    csv_path = '../input/'+csv_name
    csv_file = open(csv_path, "r")
    csv_read = csv.reader(csv_file, delimiter=',')
    # Filters that are not in csv file
    filter_copy = desired_filter_list.copy()
    for row in csv_read:
        filter_i = row[5]
        for filter in filter_copy:
            if filter == filter_i:
                filter_copy.remove(filter_i)
    csv_file.close()
    # If copy is empty, then all filters are in csv file
    for filter in filter_copy:
        desired_filter_list.remove(filter)

'''
Use the template spectrum to create a mangled spectrum of the flux using the effective areas of each filter bands, 
the flux of the template spectrum, and the ratio between the sn_name count rates and template spectrum's count rates.
'''
def mangle_data(file, pivotlist, template_spectrum, filter_file_list, reader, reference_epoch_mjd, zeropointlist):
    # Akash -- read in the template spectrum.
    # If it starts after wavelength_min or ends before wavelength_max
    # then change these values so that the template spectrum covers the whole range
    # we are making the spectrum for
    # Create wavelength list to extend just before and after the pivot wavelengths
    # of the observed filters
    wavelength_min = 10.0*(math.floor(min(pivotlist)/10.0))-200.0
    wavelength_max = 10.0*(math.ceil(max(pivotlist)/10.0)) + 200.0
    wavelength_nbins = int((wavelength_max-wavelength_min)/10.0+1)

    print("# of wavelength bins", wavelength_nbins)
    wavelength_list = np.empty(wavelength_nbins)
    for counter in range(wavelength_nbins):
        wavelength_list[counter] = wavelength_min+10.0*counter

    row_count = len(file)
    filter_count = len(filter_file_list)

    mjd_list = np.empty((row_count-1))
    epoch_list = np.empty((row_count-1)) 
    flux_matrix = np.empty((row_count-1, wavelength_nbins))
    flux_matrix.fill(np.nan)
    counts_list = np.empty((row_count-1, filter_count))
    mangled_counts = np.empty((row_count-1, filter_count))

    data = []
    ind = 0

    # Mangled Spectrum
    spec = []

    spectraname = "../spectra/" + template_spectrum
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

        mjd_list[ind] = epoch
        # appending counts per filter at epoch
        counts_list[ind, :] = counts_in

        print("row start")
        if ind == 0:
            spectraWavelengths, flux = clean_spectrum(spectraname)

        # Function Call 3
        # mangle the spectrum to match the given count rates
        mangled_spec_wave, mangled_spec_flux = mangle_simple(
            spectraWavelengths, flux, filter_file_list, zeropointlist, pivotlist, counts_in, st)
        spec += [mangled_spec_flux]

        print("row end")

        print("interp start")
        f = scipy.interpolate.interp1d(
            mangled_spec_wave, mangled_spec_flux, kind='linear')
        print("interp end")

        flux_interp = f(wavelength_list)
        flux_matrix[ind, :] = flux_interp
        fill_epoch = [epoch]*wavelength_nbins
        temp_data = [fill_epoch[:], wavelength_list[:], flux_interp[:]]
        data.extend(np.array(temp_data).transpose())

        # Getting counts of mangled template
        temp_template_spec = np.column_stack(
            (wavelength_list[:], flux_interp[:]))
        # print(temp_template_spec)
        # temp_counts = get_counts_multi_filter(temp_template_spec,filter_file_list)
        # the above is what used to be called in case we want to revert
        # The unified total_counts function returns two additional values along with the counts array so using two dummy variables

        # Function Call 4
        # Get the count rates for each filter band for the new spectrum created.
        temp_counts = specarray_to_counts(
            temp_template_spec, filter_file_list)

        #temp_1,temp_2,temp_counts = total_counts(temp_template_spec,filter_file_list)
        mangled_counts[ind, :] = temp_counts
        ind += 1
    return mangled_counts, mjd_list, data, counts_list, mangled_spec_wave, wavelength_list, epoch_list, flux_matrix

'''
Function to house all the plotting that is to be done at the end of the pipeline.
'''
def plots(sn_name, wavelength_list, epoch_list, flux_matrix):
    # Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis
    spectrum_plot([sn_name])
    # validation_plotting(filters_from_csv,counts_list,mjd_list, mangled_counts, sn_name)

#    from plot_3d import plot_3D    # filtered_df = pd.read_csv(output_file,header=0) #uncomment this if you have a saved df you just want to read and plot in 3d

    # mjd_list = np.array(filtered_df['MJD'],dtype='float')
    # wavelengths = np.array(filtered_df['Wavelength'],dtype='float')
    # flux_matrix = np.array(filtered_df['Flux'],dtype='float')
    #
    # 3dplot not working. only uncomment if fixed.
    # plot_3D(df,sn_name)

    fig = plt.figure()
    ax = Axes3D(fig)
    X, Y = np.meshgrid(wavelength_list, epoch_list)
    Z = flux_matrix

    surf = ax.plot_surface(
        X, Y, flux_matrix, rstride=1, cstride=1, cmap='hot')
    ax.set_zlim(0, np.amax(Z))

    plot.show()  # without this the 3d surface plot doesn't show but extra plot shows too

'''
Main wrapper for aggienova-templates
sn_name is a string with the desired supernova name
filterlist is an array of the filters being used
Program handles I/O between different functions of the project.
Output is csv with matrix of wavelength,epoch,flux
--output/[sn_name]_template.csv
'''
def main():
    # Use command line to grab arguments from the user
    parser=argparse.ArgumentParser(description='Process supernova thrrough spectrum template.')
    parser.add_argument('supernova', metavar='supernova',
                        type=str, nargs=1, help='A supernova to process.')
    parser.add_argument('template', metavar='template', type=str,
                        nargs=1, help='A template file to process supernova with.')
    parser.add_argument('csv', metavar='csv', type=str, nargs='?', default='y', choices=[
                        'y', 'n', 'Y', 'N'], help='Save data as csv, y/n.')
    parser.add_argument('uvot', metavar='uvot', type=str, nargs='?', default='n', choices=[
                        'y', 'n', 'Y', 'N'], help='Process uvot supernova file.')
    args = parser.parse_args()
    
    # Assign the arguments to variables
    sn_name = args.supernova[0]
    template_spectrum = args.template[0]
    store_as_csv = args.csv[0].upper() == 'Y'
    reference_epoch_mjd = 0.0
    process_uvot = args.uvot[0].upper() == 'Y'

    # If the files are not uvot we call the sn_data_online and check_filter_data
    if(not process_uvot):
        bool_error, bool_online_data=sn_data_online(sn_name)
        if not bool_error:
            check_filter_data(sn_name)

        # Function call 1
        # Convert the magnitudes from the sn data to count rates
        observedmags_to_counts_2(sn_name, desired_filter_list, template_spectrum)

        with open('../output/Test_A.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([1, "Filterlist", desired_filter_list])
    
    else:
        uvot(sn_name, "y")
        sn_name = sn_name+'_uvot'

    file = open('../input/'+sn_name+'_countsarray'+'.csv', 'r', newline='').readlines()
    reader = csv.reader(file, delimiter=',')

    #  these are the filters actually present in the csv file
    #  blank columns are removed by observedmags_to_counts

    # This reads in the filter name headers and skips the error columnts
    filters_from_csv = next(reader)[1::2]
    # Function call 2
    filter_file_list, zeropointlist, pivotlist = filterlist_to_filterfiles(
        filters_from_csv, template_spectrum)

    # Dropping file into output
    # '../output/' + sn_name +
    with open('../output/Test_A.csv', 'a', newline='') as out:
        writer = csv.writer(out)
        writer.writerow([7, "Filter File List", filter_file_list])
        writer.writerow([8, "Zeropoint List", zeropointlist])
        writer.writerow([9, "Pivot List", pivotlist])

    mangled_counts, mjd_list, data, counts_list, mangled_spec_wave, wavelength_list, epoch_list, flux_matrix =mangle_data(file, pivotlist, template_spectrum, filter_file_list, reader, reference_epoch_mjd, zeropointlist)

    df = pd.DataFrame(columns=['MJD', 'Wavelength', 'Flux'], data=data)

    # format is different than input template (see vega.dat.csv)
    output_file = '../output/'+sn_name+'_template.csv'
    if store_as_csv:
        df.to_csv(output_file, index=False, float_format='%g')

    # Function Call 5
    # Creates an output file of the mangled counts for each filter band for each epoch
    mangled_to_counts(
        sn_name, filters_from_csv, mangled_counts, mjd_list)

    # Convert the mangled count rates to magnitudes
    countrates2mags(sn_name, template_spectrum)

    counts_list = np.array(counts_list, dtype='float')

    with open('../output/Test_A.csv', 'a', newline='') as out:
        writer = csv.writer(out)
        writer.writerow([10, "Input Wave", mangled_spec_wave])
        #writer.writerow([11, "Mangled Spectrum Flux", spec])
        writer.writerow([11, "Counts List", counts_list])

#    filtered_df = df[(df.Wavelength > 1000) & (df.Wavelength < 10000) & (df.MJD < 54330)] #filters data to remove outliers
#    filtered_df.to_csv('../output/'+sn_name+'_filtered.csv',index=False)

    # The bool statment was to ensure that we only delete the temporary online data file we downloaded.
    if(not process_uvot):
        if bool_online_data == True:
            print("Removing" + sn_name + "_osc.csv from input folder")
            os.remove('../input/'+sn_name+'_osc.csv')

    plots(sn_name, wavelength_list, epoch_list, flux_matrix)

if __name__ == "__main__":
    main()