import numpy as np
from spectrophot_array_in import *
from astropy.cosmology import FlatLambdaCDM
import pysynphot as S



cosmo = FlatLambdaCDM(H0=73, Om0=0.3)



F200_wave,F200_tp = np.loadtxt('F200W_NRC_and_OTE_ModAB_mean.txt',dtype=float,
                               usecols=(0,1), unpack=True,skiprows=1)

F200_filter = [F200_wave, F200_tp] ### tp is throughput


F444_wave,F444_tp = np.loadtxt('F444W_NRC_and_OTE_ModAB_mean.txt',dtype=float,
                               usecols=(0,1), unpack=True,skiprows=1)

F444_filter = [F444_wave, F444_tp]


F200_bp = S.ArrayBandpass(F200_filter[0],F200_filter[1],name='F200') ###Wavelength in microns
F444_bp = S.ArrayBandpass(F444_filter[0],F444_filter[1],name='F444') ###Wavelength in microns









# this was for testing the spectrophotometry code
# vega_wave,vega_flux = np.loadtxt('spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)


# Here is the input spectrum and the corresponding distance

input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
# distance in Megaparsecs, here calculated from redshift for Gaia16apd
distance_sn=cosmo.luminosity_distance(0.102)

#mag_array = [1,1,1,1,1,1];
#mag_array=w_f_in(input_wave,input_flux)

#set redshift array and initialize other arrays which will have the same length
redshifts=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1]
redshiftmags=[]
distances=[]
lightyears=[]

for counter in range(0,22,1):
    z=redshifts[counter]
#   calculate distance in Megaparsecs 
    lumidist = cosmo.luminosity_distance(z)
    distances.append(lumidist)
#    distances[counter]=lumidist
#    lightyears[counter]=lumidist*3.26*10.0**6.0
    lightyears.append(lumidist*3.26*10.0**6.0)
#    print(lightyears[counter])
#   correct for the effects of distance and flux dilution
    redshiftedflux = np.multiply(distance_sn**2.0,input_flux)
    redshiftedflux = np.divide(redshiftedflux, lumidist**2.0)
    redshiftedflux = np.divide(redshiftedflux, 1.0+z)

#    print(z)
    mag_array=w_f_in(F200_filter[0]*(1.0+z),F200_filter[1])
#    print(mag_array[5])
    redshiftmags.append(mag_array[5])

#    print(redshifts[counter], redshiftmags[counter])	
#    print(lightyears[counter],redshiftmags[counter])	

#    print(z,redshifts[counter])

print(redshiftmags)
print(lightyears)

import matplotlib.pyplot as plt

#plt.plot(lightyears,redshiftmags)

##t = np.linspace(1,5,6)




#best fit line and plotting
plt.ylabel('Observed Peak Magnitude (V)')
plt.xlabel('Redshift')
plt.title('Magnitudes versus redshift')
plt.plot(lightyears,redshiftmags,'b*')
plt.plot([4.5, 5.5], [28, 28], color='k', linestyle='--', linewidth=2)
## invert y axis makes the brighter magnitude higher
plt.gca().invert_yaxis()
plt.show()
