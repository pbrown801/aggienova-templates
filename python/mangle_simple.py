

import pandas as pd
import numpy as np
from speccounts import *


def pivot_wavelength(Filter):

    filter_wave,filter_tp = np.loadtxt(Filter, dtype = float, usecols=(0,1), unpack=True)

    numerator = np.trapz(filter_tp*filter_wave,filter_wave)
    denominator = np.trapz(filter_tp/filter_wave,filter_wave)

    pivot_lambda = np.sqrt(numerator/denominator)

    return pivot_lambda



def mangle_simple(templatespectrum,filtercurves_list, counts_in):

    input_wave,input_flux = np.loadtxt(templatespectrum, dtype=float,usecols=(0,1),unpack=True)


    for l in range(len(filtercurves_list)):
    	pivot_array.append(pivot_wavelength(Filters[l]))



    #######  This comes as previous code (under old/ for just the UVOT filters)
    input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)

    counts_array=specin_countsout(input_wave, input_flux)
    print(counts_array)

    ratio=counts_in/counts_array

    manglefunction= np.interp(input_wave, pivot_array, ratio)

    mangledspectrumflux=input_flux*ratio


    return input_wave, mangledspectrumflux
