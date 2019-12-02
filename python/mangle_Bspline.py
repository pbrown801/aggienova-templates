import scipy.interpolate as interpolate
import matplotlib.pyplot as plt  
import pandas as pd
import numpy as np
from matplotlib import pyplot as plot
from speccounts import *
from utilities import *

def mangle_Bspline(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in):

    #######  Calculate the counts in each filter from the template and compare to counts_in
    input_wave,input_flux,counts_array = total_counts(templatespectrum,filter_file_list)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

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



