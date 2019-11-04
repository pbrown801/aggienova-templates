import pandas as pd
import numpy as np
from matplotlib import pyplot as plot
from speccounts import *
from utilities import *
from total_counts import *

def mangle_simple(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in):

    #input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    input_wave,input_flux,counts_array = total_counts(templatespectrum,filter_file_list)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

########  We can optimize this and only have it run the above code once. It does the same thing every time.
########  Noah is adding the pivot wavelength into filterlist_to_filterfiles.py so it can make this array once rather than
########  maybe make filter_pivot_list an optional input so that if it isn't already computed it can make it
#a filter has a pivot wavelength, check lookup table and call if not present. Similar to zero point
#We can optimize this and only have it run the above code once. It does the same thing every time.

    #######  This comes as previous code (under old/ for just the UVOT filters)
    #input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
    #counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))
    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]
    manglefunction= np.interp(input_wave, pivotlist, ratio)

#    something similar to this is what I did in IDL.  It seems like this is already how numpy.interpolate extrapolates
#    but something wierd is still going on.
#    manglefunction= np.interp(input_wave, [0,pivotlist,100000], [ratio[0],ratio,ratio[len(ratio)-1]] )

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


