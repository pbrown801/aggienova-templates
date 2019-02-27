#  take an input spectrum
import pandas as pd
import numpy as np
from utilities import *
from mangle_simple import *


####### this would come from the data input side
#######  output is a list of filters and an array of count rates
#######  with the number of rows equal to the number of epochs
#######  and the number of columns equal to the number of filters.
#######  If that is output as a csv file, then this needs to read that in
#######  or call a file to do so.


#assign sn name at beginning and look for that file as an input
sn_name = input('Supernova name: ')
inFile = '../input/'+'SNtest_countsarray'+'.csv' #make this generic eventually with sn_name
with open(inFile) as csvinp:
    reader = csv.reader(csvinp,delimiter = ',')
    filter_curves_list = next(reader)[1:]
    filter_curves_list = list(map('../filters/{0}'.format, filter_curves_list))
    for row in reader:
        mjd = row[0]
        single_epoch_test_mag_counts = row[1:]


        #do something with this

        epoch = float(mjd)-0
        single_epoch_test_mag_counts = list(map(float,single_epoch_test_mag_counts))
#######  Assign a template spectrum to use

        template_spectrum = "../spectra/SN2017erp_hst_20170629.dat"

####### read in the first row of count rates

# total_counts #this should return an array of count rates
# single_epoch_test_mag_counts = [99.2572, 40.0928, 391.629, 3538.04, 4730.92, 1505.18]  #  these come from SN2011fe #THESE WILL COME FROM SNtest



#######  mangle the spectrum to match the given countrates

        counts_in = single_epoch_test_mag_counts
        mangled_spec_wave, mangled_spec_flux = mangle_simple(template_spectrum, filter_curves_list, counts_in)

# mangling outputs spectrum that matches input counts by multiplying func by og spec

####### write a 3 column csv file with the epoch (constant for each spectrum), mangledspecwave, mangledspecflux for each row of mangledspecwave,mangledspecflux ***TATE WROTE THIS ALREADY***
        spectrum_to_csv(mangled_spec_wave,mangled_spec_flux,sn_name) #ouput name = SNtest_spectral_series.csv


#######  Now read in that file
#######  and for each epoch, read in the spectrum and compute count rates in each filter and store in an array



######  Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis
