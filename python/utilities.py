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

import math
from filterlist_to_filterfiles import filterlist_to_filterfiles

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
        print(specframe)
        #return (spectraWavelengths, flux)

        #PART #2: CLEAN FILTER
        # Process data from a filter and interpolated to spectraWavelengths
        # filterFileName is the full path to a filter file
        # Value returned is effectiveAreas
        # effectiveAreas is a np_array the same size as spectraWavelengths with interpolated effective areas from the filter file

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
    for idx,zeropoint in enumerate(zeropointlist):
        counts_df[filter_bands[idx]]=counts_df[filter_bands[idx]].apply(lambda count: (math.log10(count)/-0.4)+zeropoint)
    counts_df.to_csv('../output/MAGS/'+output_file_name+'_mangledmagsarray.csv', index=False)