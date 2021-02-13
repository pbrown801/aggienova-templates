import numpy as np
import matplotlib.pyplot as plt

'''
How to call this function:

In the header of your program, type:

from speccounts import *

using the code, type into your program:

specin_countsout(x_array, y_array)

NOTE: the inputs given to w_f_in do not literally have to be 'wavez' and 'fluxz'.
They are just place holder variables for the code below.

Machinery of this code is similar to spectrophot_v2, except without the prompt asking you for a supernova.
Need the all the filter curve .txt in the same directory to run successfully

The variables within the function only exist within the defined function. They can not be called outside of the
function. What this function does is the desired spectrophotometry and spits out the calculated magnitudes
in order w2,m2,w1,u,b,v. So I just recommend running the function with inputs and copy and paste the result into
a new array if you plan to do anything else with the magnitudes.

'''



#Vega for reference#

vega_wave,vega_flux = np.loadtxt('../spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)

# input vega_wave and vega_flux into w_f_in to test #

#####################

def specin_countsout(wavez,fluxz):

    h = 6.6260755e-27
    c = 2.99792458e18
    hc = h*c


    files = ['filters/UVW2_2010.txt','filters/UVM2_2010.txt','filters/UVW1_2010.txt','filters/U_UVOT.txt','filters/B_UVOT.txt', 'filters/V_UVOT.txt']

    filter_WL = []
    filter_A = []

    for item in files:
        #Necessary to have "../" when running in /python/ directory
        f = open("../" + item,'r')

#	print(item)

        filter_lambda = []
        filter_area = []
        for line in f:
               	line = line.rstrip()
                column = line.split()
#		print(column)
                wavelen = column[0]
                area = column[1]
                filter_lambda.append(float(wavelen))
                filter_area.append(float(area))

        filter_lambda = np.asarray(filter_lambda,dtype=float)
        filter_area = np.asarray(filter_area,dtype=float)

        nonzero = np.where(filter_area > 0.0)

        filter_lambda = filter_lambda[nonzero]
        filter_area = filter_area[nonzero]

        filter_WL.append(filter_lambda)
        filter_A.append(filter_area)

        f.close()



    ##########################################


    filtercurves = ['UVW2_2010','UVM2_2010','UVW1_2010','U_UVOT','B_UVOT','V_UVOT'] ### STRING LIST

    zeropoints = [17.38, 16.85, 17.44, 18.34, 19.11, 17.89] ### PHOTOMETRIC ZEROPOINTS BASED ON VEGA


    filtereffwavelength=[2030,2231,2634,3501,4329,5402] ### EFFECTIVE VEGA WAVELENGTH FOR EACH FILTER (IN SAME ORDER)

    mag_array = np.zeros(len(filtercurves))

    counts_array = np.zeros(len(filtercurves))


    filter_array = np.array([filter_A[0],filter_A[1],filter_A[2],filter_A[3],filter_A[4],filter_A[5]])

    filter_wave = np.array([filter_WL[0],filter_WL[1],filter_WL[2],filter_WL[3],filter_WL[4],filter_WL[5]])



    for x in range(len(filtercurves)):

        sp_ea = np.interp(wavez,filter_wave[x],filter_array[x]) ### spectrum effective area

        counts_array[x] = np.trapz(sp_ea*fluxz*wavez/hc,wavez) ### Integrating under the curve using numpy

        mag_array[x] = -2.5*np.log10(counts_array[x])+zeropoints[x] ### Calculated magnitudes

    return counts_array, mag_array



'''
NOTE on mag_array: mag_array has 6 components, one for each filter used. This means that the first
component is the calculated w2 magnitude, the second component is the m2 calculated magnitude, all
the way to v band calculated magnitude. The order of the magnitude reflects the order of filtercurves.
'''

