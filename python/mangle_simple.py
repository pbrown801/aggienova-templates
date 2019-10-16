import pandas as pd
import numpy as np
from matplotlib import pyplot as plot
from speccounts import *
from total_counts import *

def pivot_wavelength(Filter):

    filter_wave,filter_tp = np.loadtxt(Filter, dtype = float, usecols=(0,1), unpack=True)

    numerator = np.trapz(filter_tp*filter_wave,filter_wave)
    denominator = np.trapz(filter_tp/filter_wave,filter_wave)

    pivot_lambda = np.sqrt(numerator/denominator)

    return pivot_lambda


def mangle_simple(templatespectrum,filter_file_list, counts_in):

    input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))
    pivot_array = np.zeros(len(filter_file_list))
    for l in range(len(filter_file_list)):
        pivot_array[l] = pivot_wavelength(filter_file_list[l])

########  We can optimize this and only have it run the above code once. It does the same thing every time.
########  Noah is adding the pivot wavelength into filterlist_to_filterfiles.py so it can make this array once rather than
########  maybe make filter_pivot_list an optional input so that if it isn't already computed it can make it

    #######  This comes as previous code (under old/ for just the UVOT filters)
    #input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))
    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]
    manglefunction= np.interp(input_wave, pivot_array, ratio)

#    something similar to this is what I did in IDL.  It seems like this is already how numpy.interpolate extrapolates
#    but something wierd is still going on.
#    manglefunction= np.interp(input_wave, [0,pivot_array,100000], [ratio[0],ratio,ratio[len(ratio)-1]] )


    mangledspectrumflux=input_flux*manglefunction
    return input_wave, mangledspectrumflux

'''
spectrum = "vega.dat"
filters = ['UVW2_2010.txt','UVM2_2010.txt','UVW1_2010.txt','U_UVOT.txt','B_UVOT.txt','V_UVOT.txt'] ### STRING LIST
counts_array = get_counts_multi_filter(spectrum, filters)
wavelengths, mangled_flux = mangle_simple(spectrum, filters, counts_array)
plot.loglog(wavelengths, mangled_flux)
plot.show()
'''
