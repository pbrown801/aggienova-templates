import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import csv

def getCounts(spectraWavelengths, flux, filterFileName):
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

    counts = 0

    # Calculate counts
    toPhotonFlux = 5.03 * (10 ** 7)
    for i in range(0, len(spectraWavelengths) - 1):
        photonFlux = toPhotonFlux * ((flux[i] + flux[i + 1]) / 2) * (
                    (spectraWavelengths[i] + spectraWavelengths[i + 1]) / 2)
        count = ((effectiveAreas[i] + effectiveAreas[i + 1]) / 2) * photonFlux * (
                    spectraWavelengths[i + 1] - spectraWavelengths[i])
        counts += count

    # convert from angstroms to m
    # counts *= 10**-10

    return counts


#Filter and spectrum are expected to be in the filter and spectrum folders
spectraFileName = input("What is the file name for the desired spectrum: ")
spectraFileName = "../spectra/" + spectraFileName

#Make sure that the spectra file can be opened
try:
    spectraFile = open(spectraFileName)
except(FileNotFoundError):
    print("Unable to open spectrum file")
    exit()

outputFileName = "../output/Counts_" + spectraFileName[11:len(spectraFileName) - 4] + ".csv"
outputFile = open(outputFileName, 'w')

filterFileName = input("What is the file name for the desired filter (\"quit\" to quit): ")
filterFileName = "../filters/" + filterFileName

#Make sure that the filter file can be opened
try:
    filterFile = open(filterFileName)
    filterFileFound = True
    goodFilter = True
    outputFile.write(filterFileName[11:len(filterFileName) - 4] + ",")
except(FileNotFoundError):
    if filterFileName == "../filters/quit":
        exit()
    print("Unable to open filter file")
    goodFilter = False

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
    # Just some debugging code to make sure you are reading in file data correctly
    '''
    for i in range(0, len(measuredWavelengths)):
        print(measuredWavelengths[i], end = '\t')
        print(flux[i])
    '''
    flux = np.interp(spectraWavelengths, measuredWavelengths, flux)
    #plt.loglog(spectraWavelengths, flux)
    #plt.show()


while(filterFileFound):
    if goodFilter:
        counts = getCounts(spectraWavelengths, flux, filterFileName)
        print(counts)
        outputFile.write(str(counts) + "\n")
    filterFileName = input("What is the file name for the desired filter (\"quit\" to quit): ")
    filterFileName = "../filters/" + filterFileName
    # Make sure that the filter file can be opened
    try:
        filterFile = open(filterFileName)
        goodFilter = True
        outputFile.write(filterFileName[11:len(filterFileName) - 4] + ",")
    except(FileNotFoundError):
        if filterFileName == "../filters/quit":
            filterFileFound = False
            exit()
        print("Unable to open filter file")
        goodFilter = False

exit()
