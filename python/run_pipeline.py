#  take an input spectrum
import pandas as pd
import numpy as np


####### this would come from the data input side
#######  output is a list of filters and an array of count rates 
#######  with the number of rows equal to the number of epochs 
#######  and the number of columns equal to the number of filters.
#######  If that is output as a csv file, then this needs to read that in
#######  or call a file to do so.

filtercurves_list = ['UVW2_2010','UVM2_2010','UVW1_2010','U_UVOT','B_UVOT','V_UVOT'] ### STRING LIST
filtercurves_list = "../filters/" + filtercurves_list + ".dat"
print(filtercurves_list)



#######  This would come from a code for reading in each filter from the list and outputting the effective wavelength in each filter

    filtereffwavelengths=[2030,2231,2634,3501,4329,5402] 

####### read in the first row of count rates
singleepochtestmagcounts=[99.2572, 40.0928, 391.629, 3538.04, 4730.92, 1505.18]  #  these come from SN2011fe

epoch=3.4

#######  Assign a template spectrum to use

templatespectrum="../spectra/SN2017erp_hst_20170629.dat"

#######  mangle the spectrum to match the given countrates

counts_in=singleepochtestmagcounts
mangledspecwave,mangledspecflux= specfilterscountsin_mangledspecout(templatespectrum,filtercurves_list, counts_in)



####### write a 3 column csv file with the epoch (constant for each spectrum), mangledspecwave, mangledspecflux for each row of mangledspecwave,mangledspecflux



#######  Now read in that file
#######  and for each epoch, read in the spectrum and compute count rates in each filter and store in an array



######  Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis
