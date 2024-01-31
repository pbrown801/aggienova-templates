import numpy as np
import matplotlib.pyplot as plt

'''
How to call this function:

In the header of your program, type:
from spectrophot_array_in import *
using the code, type into your program:
abspecphot(x_array, y_array,filter)
'''
#Vega for reference#
vega_wave,vega_flux = np.loadtxt('../spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)
# input vega_wave and vega_flux into w_f_in to test #

#####################

def abspecphot(wavez,fluxz,filter):

    abmag=[]
    h = 6.6260755e-27
    c = 2.99792458e18
    hc = h*c

    #wavez=vega_wave
    #fluxz=vega_flux

    #filter= '../filters/U_UVOT.txt'
    f = open(filter,'r')

    filter_lambda = []
    filter_area = []
    for line in f:
        line = line.rstrip()
        column = line.split()
        wavelen = column[0]
        area = column[1]
        if wavelen[0] != '#':
       	    filter_lambda.append(float(wavelen))
            filter_area.append(float(area))

    filter_lambda = np.asarray(filter_lambda,dtype=float)
    filter_area = np.asarray(filter_area,dtype=float)
        
    #nonzero = np.where(filter_area > 0.0)
        
    #filter_lambda = filter_lambda[nonzero]
    #filter_area = filter_area[nonzero]
        
    bulk = np.where(filter_area > 0.1*np.amax(filter_area))
    bulk = np.where(filter_area > 0.1*np.amax(filter_area))
#    print(bulk)
    first=bulk[0][0]
 #   print(first)
 #   print(' ')
    #filter_lambda = filter_lambda[nonzero]
    #filter_area = filter_area[nonzero]

    f.close()

    if filter_lambda[11] < 10:
        filter_lambda = filter_lambda * 10000.0

    ##############   calculate ab zeropoint from ab spectrum
    abfluxspec=[]
    for l in filter_lambda:
        abfluxspec.append(np.divide(3.63*10.0**(-20.00)*c,l**2.0))

    nabfluxspec=np.asarray(abfluxspec,dtype=float)

    zeropoint = -2.5*np.log10( np.trapz(filter_area*abfluxspec*filter_lambda/hc,filter_lambda))

    ### Calculated magnitudes

    sp_ea = np.interp(wavez,filter_lambda,filter_area) ### spectrum effective area         
    counts = np.trapz(sp_ea*fluxz*wavez/hc,wavez) ### Integrating under the curve using numpy
    if counts > 0:
        abmag = -2.5*np.log10( counts ) - zeropoint ### Calculated magnitudes
#    print(wavez[0],filter_lambda[bulk[0]][0])
 #   print(wavez[len(wavez)-1],filter_lambda[bulk[0][len(bulk)-1]])
 #   print(len(bulk))
    if wavez[0] > filter_lambda[bulk[0][0]]:
        abmag=float('NaN')
    if wavez[len(wavez)-1] < filter_lambda[bulk[0][len(bulk)-1]]:
        abmag=float('NaN')
#    print abmag	
    return(abmag);
    
