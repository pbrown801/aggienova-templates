import numpy as np
import matplotlib.pyplot as plt

'''
How to call this function:

In the header of your program, type:
from vegaspecphot.py import *
To use the code, type into your program:
vegaspecphot(x_array, y_array)
where x_array is the wavelength range of your spectrum
y_array is the flux data

Make sure vega.dat is in the same directory as this code
as well as the filter txt files
'''


#Vega for reference#

vega_wave,vega_flux = np.loadtxt('vega.dat',dtype=float,usecols=(0,1),unpack=True)

Filter = 'U_UVOT.txt' #for test
# input vega_wave and vega_flux into w_f_in to test. input a filter txt file as the Filter argument
# Calculates zeropoints for filter used
# inputting vega should give you a zero for magnitude in the filter used

#####################

def vegaspecphot(wavez,fluxz,Filter):

    h = 6.6260755e-27
    c = 2.99792458e18
    hc = h*c #units of erg*A

    filter_lambda,filter_area = np.loadtxt(Filter,comments='#',usecols=(0,1), unpack=True)

    nonzero = np.where(filter_area > 0.0)
        
    filter_lambda = filter_lambda[nonzero]
    filter_area = filter_area[nonzero]


    ##############   calculate vega zeropoint for every filter from vega spectrum

    in_lambda_range = np.where((vega_wave>=min(filter_lambda))&(vega_wave<=max(filter_lambda)))
    interpolated_flux = np.interp(filter_lambda,vega_wave[in_lambda_range[0]],vega_flux[in_lambda_range[0]])
    zeropoint = round(-2.5*np.log10(np.trapz(filter_area*interpolated_flux*filter_lambda/hc,filter_lambda)),2)

    # Calculated magnitudes

    sp_ea = np.interp(wavez,filter_lambda,filter_area) ### spectrum effective area         
    counts = np.trapz(sp_ea*fluxz*wavez/hc,wavez) ### Integrating under the curve using numpy
    if counts > 0:           
        vegamag = -2.5*np.log10(counts) - zeropoint ### Calculated magnitudes
    return vegamag

mag = vegaspecphot(vega_wave,vega_flux,Filter)



    

