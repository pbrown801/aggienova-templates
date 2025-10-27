#total_counts Modules
import matplotlib
import time
from matplotlib import pyplot as plt
import numpy as np
import csv
from speccounts import *
#utilities Modules
import os.path
import sys
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

import math

import scipy.interpolate as interpolate
import matplotlib.pyplot as plt  




def sn_data_online(sn_name):
    '''
    If the data for the sn_name does not exist we retrieve it frrom the supernova catalog at api.sne.space.
    Returns two boolean values:
    bool_online_data - If we have sucessfully retrieve the online data we make bool_online_data True otherwise false.
    bool_error -  If we have an error in gathering the specified superrnova we make bool_error True otherwise false
    '''
    bool_error = False
    bool_online_data = False
    files = os.listdir('../input')
    if sn_name + "_osc.csv" not in files:
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
            
            bool_error = True
    return bool_error, bool_online_data


'''
sn_name is a string with the desired supernova name
desired_filter_list is an array of the filters which have data
program writes two csv files
--magarray.csv has the magnitudes and errors for the desired filters
--countsarray.csv has the interpolated counts for all times at all filters
'''


def oscmags_to_counts(sn_name, desired_filter_list, template_spectrum, interpFilter = "UVW1"):
    input_file = open('../input/'+ sn_name + '_osc.csv', 'r+')
    data = input_file.read()
    data = data.splitlines()
    data_list = []
    for line in data:
        data_list.append(line.split(','))

    time = []
    mag  = []
    emag = []
    band = []
    
    for x, line in enumerate(data_list):
        if x != 0 and str(line[5]).upper() in desired_filter_list:
            # This checks if there is an uncertainty (error) given.  
            # If not, skip it as the magnitude is an upper limit not a measurement
            if line[3] != '':
                time.append(float(line[1]))
                mag.append(float(line[2]))
                emag.append(float(line[3]))
                band.append((str(line[5])).upper())

    filter_file_list,zeropointlist,pivotlist = filterlist_to_filterfiles(desired_filter_list, template_spectrum)

    interpFirst = 1000000000000000
    interpLast = -1000000000000000
    for i in range(0, len(time)):
        if(band[i] == interpFilter and mag[i] > 0):
            if(time[i] < interpFirst):
                interpFirst = time[i]
            if(time[i] > interpLast):
                interpLast = time[i]

    interpTimes = []
    #for nonzero filters in interval of interpolation
    for i in range(0, len(time)):
        if interpFirst <= time[i] <= interpLast:
            if band[i] == interpFilter:
                interpTimes.append(time[i])

    #Adding the variables
    with open('../output/Test_A.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([2, "Time", time])
        writer.writerow([3, "Mag", mag])
        writer.writerow([4, "Emag", emag])
        writer.writerow([5, "Band", band])
        writer.writerow([6, "Interptimes", interpTimes])


    #contains counts directly from measured values
    counts_matrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)
    counterrs_matrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)
    #contains measured magnitudes
    magMatrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)
    #contains measured error on magnitudes
    emagMatrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)

    #contains interpolated count values for all filters over all times
    interp_counts_matrix =  np.zeros((len(desired_filter_list),len(interpTimes)))
    interp_counterrs_matrix =  np.zeros((len(desired_filter_list),len(interpTimes)))
    interpMatrix = np.zeros((len(desired_filter_list),len(interpTimes)))

    for i in range(len(desired_filter_list)):
        measured_counts = np.zeros(len(time))
        measured_counterrs = np.zeros(len(time))
        measured_times = np.zeros(len(time))
        length = 0

###### does this have to be done in a for loop or can python operate on the whole row/column at once?

        for j in range(len(time)):

            if band[j] == desired_filter_list[i]:

                counts_matrix[i][j] = str(math.pow(10, -0.4*(mag[j]-zeropointlist[i])))  
                counterrs_matrix[i][j] = str(abs(float(counts_matrix[i][j])*float(emag[j])*-1.0857)) # need to check if this works

                magMatrix[i][j] = str(mag[j])
                emagMatrix[i][j] = emag[j]
                measured_counts[length] = float(counts_matrix[i][j])
                measured_counterrs[length] = float(counterrs_matrix[i][j])
                measured_times[length] = time[j]
                length += 1
            else:
                counts_matrix[i][j] = ''
                counterrs_matrix[i][j] = ''
                magMatrix[i][j] = ''
                emagMatrix[i][j] = ''
        measured_counts.resize(length)
        measured_counterrs.resize(length)
        measured_times.resize(length)
        interp_counts_matrix[i] = np.interp(interpTimes, measured_times, measured_counts)
        interp_counterrs_matrix[i] = np.interp(interpTimes, measured_times, measured_counterrs)

    column_err_names = []

    for l in range(len(desired_filter_list)):
        column_err_names.append(desired_filter_list[l]+'err')

    column_names = ['Time (MJD)']

    for l in range(len(desired_filter_list)):
        column_names.append(desired_filter_list[l])
        column_names.append(column_err_names[l])


    with open('../output/MAGS/'+ sn_name + '_magarray.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([column_names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+2*len(desired_filter_list),dtype=object)
            line[0] = str(interpTimes[i])
            for j in range(0,len(desired_filter_list)):
                line[2*j + 1] = magMatrix[j][i]
                line[2*j + 2] = emagMatrix[j][i]
            writer.writerow(line)


    with open('../input/COUNTS/'+ sn_name + '_countsarray.csv', 'w', newline ='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([column_names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+2*len(desired_filter_list))
            line[0] = interpTimes[i]
            for j in range(0,len(desired_filter_list)):
                line[2*j+1] = interp_counts_matrix[j][i]
                line[2*j+2] = interp_counterrs_matrix[j][i]
            writer.writerow(line)

    counts_frame = pd.read_csv('../input/COUNTS/'+ sn_name + '_countsarray.csv')
    return counts_frame



# Main function to run the program
def uvotmags_to_counts(sn_name, template_spectrum):
    file_path='../input/'+sn_name+'_uvotB15.1.dat'
    tolerance=0.15
    # Parse the data from the file
    columns = ['Filter', 'MJD', 'Mag', 'MagErr', '3SigMagLim', '0.98SatLim', 'Rate', 'RateErr', 'Ap', 'Frametime', 'Exp', 'Telapse']
    data = []

    # Open and read the file
    with open(file_path, 'r') as f:
        for line in f:
            # Ignore lines starting with '#' (comments)
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 12:  # Ensure correct number of columns
                filter_name, mjd, mag, mag_err, sig_lim, sat_lim, rate, rate_err, ap, frame_time, exp, telapse = parts
                # Handle 'NULL' entries as None
                rate = np.nan if rate == 'NULL' else float(rate)
                mjd = float(mjd)
                data.append([filter_name, mjd, rate, rate_err,telapse])

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(data,columns=['Filter','MJD','Rate','RateErr','Telapse'])  # Only use Filter, MJD, and Rate

    ## mjd_groups=group_mjds(df, tolerance=0.15)
    
    # Organize the data by MJD with the tolerance of 0.15 days
    # Initialize an empty list to store rows
    result = []

    # Get unique MJDs
    unique_mjd = sorted(df['MJD'].unique())

    avgmjd_list=[]
    # Iterate through each unique MJD
    for mjd in unique_mjd:
        # Filter data within 0.15 days of the current MJD
        subset = df[np.abs(df['MJD'] - mjd) <= tolerance ]
        #subset = df[np.abs(df['MJD'] - mjd) <= tolerance or (((df['MJD'] - df['Telapse']/60/60/24/2) < mjd) and ((df['MJD'] + df['Telapse']/60/60/24/2) > mjd))]
        avgmjd=np.mean(subset['MJD'])
        #print(avgmjd)
        avgmjd_list.append(avgmjd)
    mjddf=pd.DataFrame(avgmjd_list)
    #print(mjddf)
    mjd_groups=sorted(mjddf[0].unique())
    

    
    # Iterate through each unique MJD
    for mjd in mjd_groups:
        # Filter data within 0.15 days of the current MJD
        subset = df[np.abs(df['MJD'] - mjd) <= tolerance]
        #print(subset)
        # Initialize a row with MJD and placeholders for each filter
        row = [mjd, None, None, None, None, None, None, None, None, None, None, None, None]  # MJD, UVW2, UVM2, UVW1, U, B, V
        
        # Fill in the count rates for each filter
        for _, entry in subset.iterrows():
            #print(entry)
            if entry['Filter'] == 'UVW2':
                row[1] = entry['Rate']
                row[2] = entry['RateErr']
            elif entry['Filter'] == 'UVM2':
                row[3] = entry['Rate']
                row[4] = entry['RateErr']
            elif entry['Filter'] == 'UVW1':
                row[5] = entry['Rate']
                row[6] = entry['RateErr']
            elif entry['Filter'] == 'U':
                row[7] = entry['Rate']
                row[8] = entry['RateErr']
            elif entry['Filter'] == 'B':
                row[9] = entry['Rate']
                row[10] = entry['RateErr']
            elif entry['Filter'] == 'V':
                row[11] = entry['Rate']
                row[12] = entry['RateErr']
        
        # Append the row to the result
        result.append(row)

    # Convert result to a numpy array for convenience
    result_array = np.array(result)

    # Convert to a DataFrame for better visualization
    result_df = pd.DataFrame(result_array, columns=['MJD', 'UVW2', 'UVW2err', 'UVM2', 'UVM2err', 'UVW1', 'UVW1err', 'U', 'Uerr', 'B', 'Berr', 'V', 'Verr'])
    
    desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V']


    filter_file_list,zeropointlist,pivotlist = filterlist_to_filterfiles(desired_filter_list, template_spectrum)


    counts_matrix = np.zeros((len(desired_filter_list),len(df['MJD'])), dtype=object)
    counterrs_matrix = np.zeros((len(desired_filter_list),len(df['MJD'])), dtype=object)
    

    column_err_names = []

    for l in range(len(desired_filter_list)):
        column_err_names.append(desired_filter_list[l]+'err')

    column_names = ['Time (MJD)']


    for l in range(len(desired_filter_list)):
        column_names.append(desired_filter_list[l])
        column_names.append(column_err_names[l])

    result_df = result_df.fillna(value=np.nan)

    
    with open('../input/COUNTS/'+ sn_name + '_countsarray.csv', 'w', newline ='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([column_names])
        for i in range(0,len(result_df['MJD'])-1):
            
            line = np.zeros(1+2*len(desired_filter_list))
            
            line = [result_df.loc[i,'MJD'],result_df.loc[i,'UVW2'],result_df.loc[i,'UVW2err'],result_df.loc[i,'UVM2'],result_df.loc[i,'UVM2err'], result_df.loc[i,'UVW1'],result_df.loc[i,'UVW1err'],result_df.loc[i,'U'],result_df.loc[i,'Uerr'], result_df.loc[i,'B'],result_df.loc[i,'Berr'],result_df.loc[i,'V'],result_df.loc[i,'Verr']]

            writer.writerow(line)

    #print(result_df)
    return result_df


def check_filter_data(sn_name):
    '''
    Nathan's code: Check if filter data exists for current supernova before running observed mags
    '''
    desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V']
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

def plots3d(sn_name, output_file_name, wavelength_list, epoch_list, flux_matrix, template_spectrum):
    '''
    Function to house all the plotting that is to be done at the end of the pipeline.
    '''
    # Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis
    # spectrum_plot([sn_name])
    # validation_plotting(filters_from_csv,counts_list,mjd_list, mangled_counts, sn_name)

    #    from plot_3d import plot_3D       
    # filtered_df = pd.read_csv(output_file,header=0) 
    #uncomment this if you have a saved df you just want to read and plot in 3d

    # mjd_list = np.array(filtered_df['MJD'],dtype='float')
    # wavelengths = np.array(filtered_df['Wavelength'],dtype='float')
    # flux_matrix = np.array(filtered_df['Flux'],dtype='float')
    #
    # 3dplot not working. only uncomment if fixed.
    # plot_3D(df,sn_name)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
#    ax = Axes3D(fig,auto_add_to_figure=False)  2022 07 06 commented out, then was working
    X, Y = np.meshgrid(wavelength_list, epoch_list)
    Z = flux_matrix

    surf = ax.plot_surface(
        X, Y, flux_matrix, rstride=1, cstride=1, cmap='hot')
   
    ax.set_zlim(0, np.amax(Z[Z>0]))
    save_name=r'../output/PLOTS/'+output_file_name
    if "series" in template_spectrum:
        save_name += '_series_3d_surface.png'
    else:
        save_name += '_3d_surface.png'
    plt.savefig(save_name)


def mangled_to_counts(output_file_name, filter_list, mangled_counts, epochs):

    # print('epochs')
    # print(epochs)

    df = pd.DataFrame(data = mangled_counts,
                      index = epochs,
                      columns = filter_list)

    df.to_csv('../input/COUNTS/'+output_file_name+'_mangledcounts.csv',index_label = 'Time (MJD)')


def pivot_wavelength(Filter):

    filter_wave,filter_tp = np.loadtxt(Filter, dtype = float, usecols=(0,1), unpack=True)

    numerator = np.trapz(filter_tp*filter_wave,filter_wave)
    denominator = np.trapz(filter_tp/filter_wave,filter_wave)

    pivot_lambda = np.sqrt(numerator/denominator)

    return pivot_lambda


def test_file(sn_name,):
    with open('../input/'+ sn_name + '_test_array.csv', 'w', newline ='') as test:
        #Writing the magarray and counts array
        writer=csv.writer(test,delimiter=',')


def csv_to_ascii(inFile,outFile):
    """
        Converts csv file to ascii file
    """
    outFile = outFile+'.txt'
    with open(outFile,'w') as output:
        with open(inFile) as csvinp:
            reader = csv.reader(csvinp,delimiter = ',')
            for row in reader:
                for col in row:
                    output.write(str(col) + ' ')
                output.write('\n')


def dat_to_csv(dat):
    """
        converter function between .dat and .csv
    """
    input_file = '../input/'+dat
    output_file = '../output/'+dat+'.csv'
    df = pd.read_csv(input_file,skiprows=1,header=None,skipinitialspace=True,sep=' ',names=['Wavelength','Flux'])
    out_df = pd.DataFrame({'Epoch':[0]*len(df)})
    out_df = out_df.join(df)
    out_df.to_csv(output_file,index=False)

def specarray_to_counts(spectrum, filter_file_list):
    # Calculate counts based on the spectrum wavelength vs flux and filter wavelength vs effectiveAreas
    # spectraWavelengths, flux, and effectiveAreas are np_arrays with the same length
    # Value returned is counts, which is a floating-point numeric value
    # Calculate counts
    toPhotonFlux = 5.03 * (10 ** 7)
    spectraWavelengths=spectrum[:,0]
    flux=spectrum[:,1]

    counts_array = []
    counts=0
    for fileName in filter_file_list:
        fileName = "../filters/" + fileName
 
        try:
            filterFile = open(fileName)
        except(FileNotFoundError):
            print("Unable to open filter file")
            exit()

        # All filter wavelenghts
        filterWavelengths = np.array([])
        # Effective areas for filter wavelengths
        effectiveAreas = np.array([])

        filterDelim = ""
        if fileName.endswith(".csv"):
            filterDelim = ","
        else:
            filterDelim = " "

        # Input and interpolate filter data
        with open(fileName, 'r') as csvfile:
            # filterReader = csv.reader(csvfile, delimiter = filterDelim, skipinitialspace = True)
            for line in csvfile:
                row = line.split()
                filterWavelengths = np.append(filterWavelengths, float(row[0]))
                effectiveAreas = np.append(effectiveAreas, float(row[1]))
            effectiveAreas = np.interp(spectraWavelengths, filterWavelengths, effectiveAreas)
            # plt.loglog(spectraWavelengths, effectiveAreas)
            # plt.show()
        #return effectiveAreas

        #PART #3: Calculate counts
        # Calculate counts based on the spectrum wavelength vs flux and filter wavelength vs effectiveAreas
        # spectraWavelengths, flux, and effectiveAreas are np_arrays with the same length
        # Value returned is counts, which is a floating-point numeric value
        # Calculate counts
        toPhotonFlux = 5.03 * (10 ** 7)
        for i in range(0, len(spectraWavelengths) - 1):
            photonFlux = toPhotonFlux * ((flux[i] + flux[i + 1]) / 2) * (
                    (spectraWavelengths[i] + spectraWavelengths[i + 1]) / 2)
            count = ((effectiveAreas[i] + effectiveAreas[i + 1]) / 2) * photonFlux * (
                    spectraWavelengths[i + 1] - spectraWavelengths[i])
            counts += count
        #return counts
        counts_array +=[counts]
    return (counts_array)

#Unified Function which yields spectrawavelength, flux and counts array
def total_counts(spectraFileName,filter_file_list):
    spectraFileName = "../spectra/" + spectraFileName
    counts_array = []
    counts=0
    for fileName in filter_file_list:
        fileName = "../filters/" + fileName
        #PART #1 : CLEAN SPECTRUM
        # Process data from a spectrum file and interpolate missing values
        # spectraFileName is the full path to a spectrum file
        # Tuple of spectraWavelengths and flux is returned
        # spectraWavelengths and flux are np_arrays of the same length
        # spectraWavelengths has the wavelengths that the spectrum was measured at
        # flux is the measured or interpolated flux values for the spectrum
        try:
            spectraFile = open(spectraFileName)
        except(FileNotFoundError):
            print("Unable to open spectrum file")
            exit()
        # For wavelengths with a flux measurement
        measuredWavelengths = np.array([])
        # For all spectra wavelengths
        spectraWavelengths = np.array([])
        # All flux measurements
        flux = np.array([])
        #initialization of dataframe
        specframe = pd.DataFrame(columns=["measuredWavelengths", "spectraWavelengths", "flux"])
        spectraDelim = ""
        if spectraFileName.endswith(".csv"):
            spectraDelim = ","
        else:
            spectraDelim = " "
        # Input and interpolate spectra data
        with open(spectraFileName, 'r') as csvfile:
            spectraReader = csv.reader(csvfile, delimiter=spectraDelim, skipinitialspace=True)
            for row in spectraReader:
                if row[0].startswith('#'):
                    continue
                spectraWavelengths = np.append(spectraWavelengths, float(row[0]))
                if row[1] != "NaN" and float(row[1]) != 0:
                    measuredWavelengths = np.append(measuredWavelengths, float(row[0]))
                    flux = np.append(flux, float(row[1]))
            flux = np.interp(spectraWavelengths, measuredWavelengths, flux)
        specframe = pd.DataFrame(data = measuredWavelengths, columns = ["measuredWavelengths"])
        # print("specframe ", specframe)
        #return (spectraWavelengths, flux)

        #PART #2: CLEAN FILTER
        # Process data from a filter and interpolated to spectraWavelengths
        # filterFileName is the full path to a filter file
        # Value returned is effectiveAreas
        # effectiveAreas is a np_array the same size as spectraWavelengths 
        # with interpolated effective areas from the filter file

        try:
            filterFile = open(fileName)
        except(FileNotFoundError):
            print("Unable to open filter file")
            exit()

        # All filter wavelenghts
        filterWavelengths = np.array([])
        # Effective areas for filter wavelengths
        effectiveAreas = np.array([])

        filterDelim = ""
        if fileName.endswith(".csv"):
            filterDelim = ","
        else:
            filterDelim = " "

        # Input and interpolate filter data
        with open(fileName, 'r') as csvfile:
            # filterReader = csv.reader(csvfile, delimiter = filterDelim, skipinitialspace = True)
            for line in csvfile:
                row = line.split()
                filterWavelengths = np.append(filterWavelengths, float(row[0]))
                effectiveAreas = np.append(effectiveAreas, float(row[1]))
            effectiveAreas = np.interp(spectraWavelengths, filterWavelengths, effectiveAreas)
            # plt.loglog(spectraWavelengths, effectiveAreas)
            # plt.show()
        #return effectiveAreas

        #PART #3: Calculate counts
        # Calculate counts based on the spectrum wavelength vs flux and filter wavelength vs effectiveAreas
        # spectraWavelengths, flux, and effectiveAreas are np_arrays with the same length
        # Value returned is counts, which is a floating-point numeric value
        # Calculate counts
        toPhotonFlux = 5.03 * (10 ** 7)
        for i in range(0, len(spectraWavelengths) - 1):
            photonFlux = toPhotonFlux * ((flux[i] + flux[i + 1]) / 2) * (
                    (spectraWavelengths[i] + spectraWavelengths[i + 1]) / 2)
            count = ((effectiveAreas[i] + effectiveAreas[i + 1]) / 2) * photonFlux * (
                    spectraWavelengths[i + 1] - spectraWavelengths[i])
            counts += count
        #return counts
        counts_array +=[counts]
    return (spectraWavelengths,flux,counts_array)
    #spectraFileName = "../spectra/" + spectraFileName
    #filterFileName = "../filters/" + filterFileName
    #spectraWavelengths, flux = clean_spectrum(spectraFileName)
    #effectiveAreas = clean_filter(filterFileName, spectraWavelengths)
    #counts = calculate_counts(spectraWavelengths, flux, effectiveAreas)
    #return counts

    #counts_array = []
    #for fileName in filter_file_list:
    #   counts_array += [get_counts(spectraFileName, fileName)]
    #return counts_array

#Total counts split into individual functions

#Caculate counts based on the spectrum wavelength vs flux and filter wavelength vs effectiveAreas
#spectraWavelengths, flux, and effectiveAreas are np_arrays with the same length
#Value returned is counts, which is a floating-point numeric value
def calculate_counts(spectraWavelengths, flux, effectiveAreas):
    counts = 0
    # Calculate counts
    toPhotonFlux = 50300000
    for i in range(0, len(spectraWavelengths) - 1):
        photonFlux = toPhotonFlux * ((flux[i] + flux[i + 1]) / 2) * (
                    (spectraWavelengths[i] + spectraWavelengths[i + 1]) / 2)
        count = ((effectiveAreas[i] + effectiveAreas[i + 1]) / 2) * photonFlux * (
                    spectraWavelengths[i + 1] - spectraWavelengths[i])
        counts += count
    return counts

#Process data from a spectrum file and interpolate missing values
#spectraFileName is the full path to a spectrum file
#Tuple of spectraWavelengths and flux is returned
#spectraWavelengths and flux are np_arrays of the same length
#spectraWavelengths has the wavelengths that the spectrum was measured at
#flux is the measured or interpolated flux values for the spectrum
def clean_spectrum(spectraFileName):
    # Make sure that the spectra file can be opened
    try:
        spectraFile = open(spectraFileName)
    except(FileNotFoundError):
        print("Unable to open spectrum file")
        exit()

    # For wavelengths with a flux measurement
    #specframe = pd.DataFrame(columns = ["measuredWavelengths", "spectraWavelengths", "flux"])
    measuredWavelengths = np.array([])
    # For all spectra wavelengths
    spectraWavelengths = np.array([])
    # All flux measurements
    flux = np.array([])

    spectraDelim = ""
    if spectraFileName.endswith(".csv"):
        spectraDelim = ","
    else:
        spectraDelim = " "

    # Input and interpolate spectra data
    with open(spectraFileName, 'r') as csvfile:
        spectraReader = csv.reader(csvfile, delimiter=spectraDelim, skipinitialspace=True)
        for row in spectraReader:
            if row[0].startswith('#'):
                continue
            #specframe = specframe.append({"spectraWavelengths" : float(row[0])}, ignore_index = True)
            spectraWavelengths = np.append(spectraWavelengths, float(row[0]))
            if row[1] != "NaN" and float(row[1]) != 0:
                #specframe = specframe.append({"measuredWavelengths" : float(row[0])}, ignore_index = True)
                measuredWavelengths = np.append(measuredWavelengths, float(row[0]))
                #specframe = specframe.append({"flux" : float(row[1])}, ignore_index = True)
                flux = np.append(flux, float(row[1]))
        #pd.concat(specframe)
        #flux = specframe.interpolate(method = 'linear', limit_direction = 'forward')
        flux = np.interp(spectraWavelengths, measuredWavelengths, flux)
    #return (specframe)
    return (spectraWavelengths, flux)

#Process data from a filter and interpolated to spectraWavelengths
#filterFileName is the full path to a filter file
#Value returned is effectiveAreas
#effectiveAreas is a np_array the same size as spectraWavelengths with interpolated effective areas from the filter file
def clean_filter(filterFileName, spectraWavelengths):
    try:
        filterFile = open(filterFileName)
    except(FileNotFoundError):
        print("Unable to open filter file")
        exit()

    # All filter wavelenghts
    filterWavelengths = np.array([])
    # Effective areas for filter wavelengths
    effectiveAreas = np.array([])

    # filterDelim = ""
    # if filterFileName.endswith(".csv"):
        # filterDelim = ","
    # else:
        # filterDelim = " "

    # Input and interpolate filter data
    with open(filterFileName, 'r') as csvfile:
        # filterReader = csv.reader(csvfile, delimiter = filterDelim, skipinitialspace = True)
        for line in csvfile:
            row = line.split()
            filterWavelengths = np.append(filterWavelengths, float(row[0]))
            effectiveAreas = np.append(effectiveAreas, float(row[1]))
        effectiveAreas = np.interp(spectraWavelengths, filterWavelengths, effectiveAreas)
        # plt.loglog(spectraWavelengths, effectiveAreas)
        # plt.show()
    return effectiveAreas

#Find the counts from a spectrum with a specific filter
#spectraFileName is the name of a spectrum file in aggienova-templates/spectra/
#filterFileName is the name of a filter file in aggienova-templates/filters/
#Value returned is counts, a floating-point numeric type
def get_counts(spectra, filterFileName):
    filterFileName = "../filters/" + filterFileName
    effectiveAreas = clean_filter(filterFileName, spectra[:,0])
    counts = calculate_counts(spectra[:,0], spectra[:,1], effectiveAreas)
    return counts

#Find the counts from a spectrum with multiple specific filters
#spectraFileName is the name of a spectrum file in aggienova-templates/spectra/
#filter_file_list is a list of filter files in aggienova-templates/filters/
#Value returned is counts_array, an array of floating-point numeric types
def get_counts_multi_filter(spectra, filter_file_list):
    counts_array = []
    for fileName in filter_file_list:
        counts_array += [get_counts(spectra, fileName)]
    return counts_array

# conversion function of mangled count rates to magnitudes. 
# Call filterlist_to_filterfiles to get the pivotlists in the same order as the column in the df since order can change
def countrates2mags(output_file_name, template_spectrum):
    counts_df=pd.read_csv('../input/COUNTS/'+output_file_name+'_mangledcounts.csv')
    filter_bands= list(counts_df.columns[1:])
    filter_file_list, zeropointlist, pivotlist = filterlist_to_filterfiles(
       filter_bands , template_spectrum)
    counts_df[counts_df<=0]=np.nan
    for idx,zeropoint in enumerate(zeropointlist):
        #if counts_df[filter_bands[idx]] > 0:
        counts_df[filter_bands[idx]]=counts_df[filter_bands[idx]].apply(lambda count: (math.log10(count)/-0.4)+zeropoint)            
        #else:
            #counts_df[filter_bands[idx]]=np.nan
    counts_df.to_csv('../output/MAGS/'+output_file_name+'_mangledmagsarray.csv', index=False)


def mangle_simple(spectraWavelengths, flux, filter_file_list, zeropointlist, pivotlist, counts_in):
    #######  Calculate the counts in each filter from the template and compare to counts_in]
	
    counts_array = []
    count = 0
    for fileName in filter_file_list:
      fileName = "../filters/"+fileName
      # print("clean filter start")
      effectiveAreas = clean_filter(fileName, spectraWavelengths)
      # print(effectiveAreas)
      en = time.time()
      # print(en-st)
      # print("clean filter end")
      # print("calc counts start")
      count = calculate_counts(spectraWavelengths, flux, effectiveAreas)#dtype=float,usecols=(0,1),unpack=True)
      en = time.time()
      # print(en-st)
      # print("calc counts end")
      counts_array +=[count]
      # print(counts_array)
    # input_wave,input_flux,counts_array = total_counts(templatespectrum,filter_file_list)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((spectraWavelengths,flux))

    #input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
    #counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))
    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]
    manglefunction= np.interp(spectraWavelengths, pivotlist, ratio)

    mangledspectrumflux=manglefunction*flux
    return spectraWavelengths, mangledspectrumflux



#  this one takes n as the degrees of the polynomial fit
def mangle_poly(spectrum_wave,spectrum_flux,filter_file_list, zeropointlist, pivotlist, counts_in,n):

    #input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((spectrum_wave,spectrum_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]

    p=np.polyfit(pivotlist, ratio,n)
    manglefunction= np.polyval(p,input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


def mangle_poly2(spectrum_wave,spectrum_flux,filter_file_list, zeropointlist, pivotlist, counts_in,n):

    #input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((spectrum_wave,spectrum_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]

    p2=np.polyfit(pivotlist, ratio,2)
    manglefunction= np.polyval(p2,input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


def mangle_poly3(spectrum_wave,spectrum_flux,filter_file_list, zeropointlist, pivotlist, counts_in,n):

    #input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((spectrum_wave,spectrum_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]

    p3=np.polyfit(pivotlist, ratio,3)
    manglefunction= np.polyval(p3,input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


def mangle_poly4(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in):

    input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]

    p4=np.polyfit(pivotlist, ratio,4)
    manglefunction= np.polyval(p4,input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


def mangle_Bspline(spectrum_wave,spectrum_flux,filter_file_list, zeropointlist, pivotlist, counts_in,n):

    #input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((spectrum_wave,spectrum_flux))

    #input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
    #counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))
    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]
    t, c, k = interpolate.splrep(pivotlist,ratio,s=0,k=4)
    print('''\
    t: {}
    c: {}
    k: {}
    '''.format(t,c,k))
    xx = input_wave
    spline = interpolate.BSpline(t,c,k, extrapolate=True)
    manglefunction= spline(xx)

    mangledspectrumflux=input_flux*manglefunction
    return input_wave, mangledspectrumflux


def valid_wavelength(wavelength, template_minmax):
    if(wavelength <= template_minmax[1]) and (wavelength >= template_minmax[0]):
        return True
    return False


def sel_template(epoch, series_path):
    '''
    Round epoch to the nearest value in the input series file that correspond to template files
    '''
    with open(series_path) as f:
        lines=f.readlines()
    # make a dictionary out of the epooch and file
    file_data = dict([line.strip().split(" ") for line in lines])
    # use the smallest difference between the input epoch and the keys in the dict as the file to use
    return file_data[min(file_data, key=lambda x: abs(float(x)-epoch))]


def filterlist_to_filterfiles(filterlist,template_spectrum):
    from utilities import pivot_wavelength


    # wavelengths_template_spectrum contains lowest and highest value in range of template_spectrum
    spectra_path = '../spectra/' + template_spectrum
    spectra_file = open(spectra_path, "r")
    wavelengths_template_spectrum = []
    spectra_file_lines = spectra_file.readlines()
    spectra_file.close()
    line_0 = True
    for line_number, line in enumerate(spectra_file_lines, start=0):
        line = line.strip()
        if (line_number == 0) and (line[0] != "#"):
            line = line.split(" ")
            wavelengths_template_spectrum.append(float(line[0]))
            line_0 = False
        if line_0 and line_number == 1:
            line = line.split(" ")
            wavelengths_template_spectrum.append(float(line[0]))
        if line_number == len(spectra_file_lines) - 1:
            line = line.split(" ")
            wavelengths_template_spectrum.append(float(line[0]))

    zeropointlist = []
    pivotlist = []
    filterfilelist=[' '] * len(filterlist)

    for idx,filtertocheck in enumerate(filterlist):
        if filtertocheck == 'UVW2':
            filterfilelist[idx]='../filters/UVW2_2010.txt'
            pivot=pivot_wavelength('../filters/UVW2_2010.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(17.39)
        if filtertocheck == 'UVM2':
            filterfilelist[idx]='../filters/UVM2_2010.txt'
            pivot=pivot_wavelength('../filters/UVM2_2010.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(16.86)
        if filtertocheck == 'UVW1':
            filterfilelist[idx]='../filters/UVW1_2010.txt'
            pivot=pivot_wavelength('../filters/UVW1_2010.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(17.44)
        if filtertocheck == 'U':
            filterfilelist[idx]='../filters/U_UVOT.txt'
            pivot=pivot_wavelength('../filters/U_UVOT.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(18.34)
        if filtertocheck == 'B':
            filterfilelist[idx]='../filters/B_UVOT.txt'
            pivot=pivot_wavelength('../filters/B_UVOT.txt')
            pivotlist.append(pivot)
            zeropointlist.append(19.1)
        if filtertocheck == 'V':
            filterfilelist[idx]='../filters/V_UVOT.txt'
            pivot=pivot_wavelength('../filters/V_UVOT.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(17.88)
        if filtertocheck == 'R':
            filterfilelist[idx]='../filters/R_Harris_c6004.txt'
            pivot=pivot_wavelength('../filters/R_Harris_c6004.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(19.86)
        if filtertocheck == 'I':
            filterfilelist[idx]='../filters/johnson_i.txt'
            pivot=pivot_wavelength('../filters/johnson_i.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(14.91)
        if filtertocheck == 'g':
            filterfilelist[idx]='../filters/LSST_g.dat'
            pivot=pivot_wavelength('../filters/LSST_g.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(14.91)
        if filtertocheck == 'r':
            filterfilelist[idx]='../filters/LSST_r.dat'
            pivot=pivot_wavelength('../filters/LSST_r.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(14.42)
        if filtertocheck == 'i':
            filterfilelist[idx]='../filters/LSST_i.dat'
            pivot=pivot_wavelength('../filters/LSST_i.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(13.87)
        if filtertocheck == 'u':
            filterfilelist[idx]='../filters/LSST_u.dat'
            pivot=pivot_wavelength('../filters/LSST_u.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.84)
        if filtertocheck == 'z':
            filterfilelist[idx]='../filters/LSST_z.dat'
            pivot=pivot_wavelength('../filters/LSST_z.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(13.33)
        if filtertocheck == 'y':
            filterfilelist[idx]='../filters/LSST_y4.dat'
            pivot=pivot_wavelength('../filters/LSST_y4.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.59)
        if filtertocheck == 'F200W':
            filterfilelist[idx]='../filters/F200W_NRC_and_OTE_ModAB_mean.txt'
            pivot=pivot_wavelength('../filters/F200W_NRC_and_OTE_ModAB_mean.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(22.8)
        if filtertocheck == 'F444W':
            filterfilelist[idx]='../filters/F444W_NRC_and_OTE_ModAB_mean.txt'
            pivot=pivot_wavelength('../filters/F444W_NRC_and_OTE_ModAB_mean.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(21.34)
        if filtertocheck == 'J':
            filterfilelist[idx]='../filters/J_2mass.txt'
            pivot=pivot_wavelength('../filters/J_2mass.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.95)
        if filtertocheck == 'H':
            filterfilelist[idx]='../filters/H_2mass.txt'
            pivot=pivot_wavelength('../filters/H_2mass.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.45)
        if filtertocheck == 'K':
            filterfilelist[idx]='../filters/Ks_2mass.txt'
            pivot=pivot_wavelength('../filters/Ks_2mass.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(11.77)
    #print(pivotlist)
    return(filterfilelist,zeropointlist,pivotlist)

#checks the efficieny of mangling and how much it differs from actual observation
def mangle_check(input_counts, mangled_counts, epoch_list, filters_from_csv, counts_frame):
    mangle_diff = input_counts - mangled_counts
    mangle_ratio = (input_counts - mangled_counts) / input_counts
    #using counts_frame from earlier, which holds all the input counts and their error in a pandas dataframe
    #order of filters is UVW2, UVM2, UVW1, U, B, V (in either uvot or non-uvot case)
    #extracting counts erorr for each filter
    err_data = np.zeros((len(epoch_list))) #array to hold all filter errors over all epochs
    for filter in filters_from_csv:
        err_data = np.vstack((err_data, counts_frame.loc[:, filter].to_numpy(dtype = float)))
    err_data = np.transpose(err_data[1:])
    mangle_error = False
    mangle_error_num = 0
    for err,mang in zip(err_data, np.abs(mangle_diff)): #grabs 6 filter measurements per epoch for both arrays
        for i,j in zip(err,mang):
            if(j > 2*i):
                mangle_error = True
                mangle_error_num += 1
    if(mangle_error):
        print("warning: mangling counts > 2*count error for", mangle_error_num, "observations")
    print("Spectra mangled outside of parameters:", '{0:.2f}'.format((mangle_error_num) / (len(err_data)*len(err_data[0])) * 100), "%")    
    
    #producing graphs showing mangling
    #6 residual graphs for each filter, 
    fig, ax = plt.subplots(6,1,sharex=True, figsize=(4,8))
    plt.subplots_adjust(hspace= 0.35)
    ax[0].set_xlim([epoch_list[0], epoch_list[-1]])
    #ax[0].set_ylim([-3,3])
    ax[-1].set_xlabel("Epoch")
    
    #use filters_from_csv as array for titles
    #rows in arrays are epochs, columns are filters
    for i in np.arange(0,len(ax)):
        ax[i].axhline(y=0, c="red")
        #ax[i].plot(epoch_list, mangle_ratio[:,i], color="black")
        ax[i].scatter(epoch_list, mangle_ratio[:,i], color = "black", s = 5)
        #ax[i].set_ylim([-0.25*max(mangle_diff[:,i]), 1.25*max(mangle_diff[:,i])])
        
    plt.show()