from spectrophot_array_in import *
from countsin_sedout import *
from speccounts import *
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=73, Om0=0.3)
import numpy as np
import matplotlib.pyplot as plt
from operator import truediv



file = 'filters/UVW2_2010.txt'

filter_WL = []
filter_A = []

f = open(file, 'r')

filter_lambda = []
filter_area = []
for line in f:
    line = line.rstrip()
    column = line.split()
    wavelen = column[0]
    area = column[1]
    filter_lambda.append(float(wavelen))
    filter_area.append(float(area))

filter_lambda = np.asarray(filter_lambda,dtype=float)
filter_area = np.asarray(filter_area,dtype=float)


# this was for testing the spectrophotometry code
# vega_wave,vega_flux = np.loadtxt('spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)

# Here is the input spectrum and the corresponding distance

input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)

counts_array=specin_countsout(input_wave, input_flux)
print(counts_array)




#sed6=countsin_sedout(counts_array)
sedspec=countsin_sedout(counts_array)

effwaves = [1928,2246,2600,3465,4392,5468]
factor = [5.77E-16, 7.47E-16, 4.06E-16, 1.53E-16, 1.31E-16, 2.61E-16]
factor = np.asarray(factor, dtype=float)
oldsed=[]
for count in range(0,len(counts_array)):

    oldsed.append(counts_array[count]*factor[count])


plt.ylabel('Flux Density')
plt.xlabel('Wavelength [ Angstroms]')
#plt.title('Magnitudes versus redshift')
#plt.plot(effwaves,sed6,'b*', linestyle='--', linewidth=1)
plt.plot(filter_lambda,sedspec,'b*', linestyle='--', linewidth=1)

plt.plot(effwaves,oldsed,'b')

plt.plot(input_wave, input_flux, color='k', linewidth=1)

plt.show()
