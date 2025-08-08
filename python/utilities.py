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

import scipy.interpolate as interpolate
import matplotlib.pyplot as plt  


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
    print(pivotlist)
    return(filterfilelist,zeropointlist,pivotlist)

