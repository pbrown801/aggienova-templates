import pandas as pd
import time
import numpy as np
from matplotlib import pyplot as plot
from speccounts import *
from observedmags_to_counts import *
from utilities import *

def mangle_simple(spectraWavelengths, flux, filter_file_list, zeropointlist, pivotlist, counts_in, st):
    #######  Calculate the counts in each filter from the template and compare to counts_in]
	
    counts_array = []
    count = 0
    for fileName in filter_file_list:
      fileName = "../filters/"+fileName
      print("clean filter start")
      effectiveAreas = clean_filter(fileName, spectraWavelengths)
      print(effectiveAreas)
      en = time.time()
      print(en-st)
      print("clean filter end")
      print("calc counts start")
      count = calculate_counts(spectraWavelengths, flux, effectiveAreas)#dtype=float,usecols=(0,1),unpack=True)
      en = time.time()
      print(en-st)
      print("calc counts end")
      counts_array +=[count]
      print(counts_array)
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


