import matplotlib.pyplot as plt
import scipy.interpolate as interp
import numpy as np
import pandas as pd
import csv
import math
from decimal import *
#from pathlib import Path
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)


def spectrum_plot(supernova):
    ###
    ### Create log(flux) + C vs Wavelength plt
    ###
    
    # Open data file
    file = open('../output/' + supernova + 'template.csv').readlines()
    row_count = sum(1 for row in file)
    print('Rows = ' + str(row_count))

    # Read in output data
    wave = []
    log_flux = []
    log_fluxTot = []
    log_fluxCount = []
    log_fluxAvg = []
    for row in range(1, row_count):
        r = file[row].split(',')
        if(float(r[2]) > 0):
            #print('Adding ' + r[1] + ', ' + str(math.log(float(r[2]), 10)))
            if(not float(r[1]) in wave):
                wave.append(int(r[1]))
                log_fluxTot.append( math.log(float(r[2]), 10) )
                log_fluxCount.append(1)
            else:
                waveInd = wave.index(int(r[1]))
                log_fluxTot[waveInd] += math.log(float(r[2]), 10)
                log_fluxCount[waveInd] += 1
    
    # Avg. flux values
    for i in range(len(wave)):
        log_fluxAvg.append( log_fluxTot[i] / log_fluxCount[i] )

    # Create subplot
    plt.subplot(211)
    plt.plot(wave, log_fluxAvg, label='SN2007af')
    plt.legend()


    ###
    ### Create Area vs Wavelength plot
    ###

    plt.savefig('../testing.png')
    plt.show()

spectrum_plot('SN2007af')