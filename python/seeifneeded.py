import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import csv

#Caculate counts based on the spectrum wavelength vs flux and filter wavelength vs effectiveAreas
#spectraWavelengths, flux, and effectiveAreas are np_arrays with the same length
#Value returned is counts, which is a floating-point numeric value
def calculate_counts(spectraWavelengths, flux, effectiveAreas):
    counts = 0
    # Calculate counts
    toPhotonFlux = 5.03 * (10 ** 7)
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
            spectraWavelengths = np.append(spectraWavelengths, float(row[0]))
            if row[1] != "NaN" and float(row[1]) != 0:
                measuredWavelengths = np.append(measuredWavelengths, float(row[0]))
                flux = np.append(flux, float(row[1]))
        flux = np.interp(spectraWavelengths, measuredWavelengths, flux)
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

    filterDelim = ""
    if filterFileName.endswith(".csv"):
        filterDelim = ","
    else:
        filterDelim = " "

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
#filterFileList is a list of filter files in aggienova-templates/filters/
#Value returned is counts_array, an array of floating-point numeric types
def get_counts_multi_filter(spectra, filterFileList):
    counts_array = []
    for fileName in filterFileList:
        counts_array += [get_counts(spectra, fileName)]
    return counts_array

#spectraFileName = input("What is the file name for the desired spectrum: ")
#filterFileName = input("What is the file name for the desired filter: ")
#print(get_counts_multi_filter(spectraFileName, filterFileName))
