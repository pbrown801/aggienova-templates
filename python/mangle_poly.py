import pandas as pd
import numpy as np
from matplotlib import pyplot as plot
from speccounts import *
from utilities import *

def mangle_poly(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in):

    input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]
    manglefunction= np.polyval([pivotlist, ratio],input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


for num in range(3):
    mangle_poly(mangledspectrumflux,filter_file_list,zeropointlist,pivotlist,counts_in)