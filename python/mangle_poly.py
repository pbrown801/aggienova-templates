import pandas as pd
import numpy as np
from matplotlib import pyplot as plot
from speccounts import *
from utilities import *

#  this one takes n as the degrees of the polynomial fit
def mangle_poly(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in,n):

    input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]

    p=np.polyfit(pivotlist, ratio,n)
    manglefunction= np.polyval(p,input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux


def mangle_poly2(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in):

    input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

    #######  Calculate the counts in each filter from the template and compare to counts_in

    counts_array=get_counts_multi_filter(clean_template, filter_file_list)
    ratio = np.zeros(len(counts_array))

    for x in range(0,len(counts_array)):
        ratio[x]=counts_in[x]/counts_array[x]

    p2=np.polyfit(pivotlist, ratio,2)
    manglefunction= np.polyval(p2,input_wave)

    mangledspectrumflux=input_flux*manglefunction

    return input_wave, mangledspectrumflux

def mangle_poly3(templatespectrum,filter_file_list, zeropointlist, pivotlist, counts_in):

    input_wave,input_flux = clean_spectrum("../spectra/" + templatespectrum)#dtype=float,usecols=(0,1),unpack=True)
    clean_template = np.column_stack((input_wave,input_flux))

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

