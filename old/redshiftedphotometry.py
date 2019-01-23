

import numpy as np

from spectrophot_array_in import *
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=73, Om0=0.3)

# this was for testing the spectrophotometry code
# vega_wave,vega_flux = np.loadtxt('spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)


# Here is the input spectrum and the corresponding distance

input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
# distance in Megaparsecs, here calculated from redshift for Gaia16apd
distance_sn=cosmo.luminosity_distance(0.102).value
print('distance to supernova originally ',distance_sn)
#mag_array = [1,1,1,1,1,1];
#mag_array=w_f_in(input_wave,input_flux)

#set redshift array and initialize other arrays which will have the same length
redshifts=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1]
redshiftmags=[]
distances=[]
lightyears=[]

comovinggigalightyears=np.multiply(cosmo.comoving_distance(redshifts).value,3.26*10.0**-3.0)

for counter in range(0,22,1):
    z=redshifts[counter]
#   calculate distance in Megaparsecs 
    lumidist = cosmo.luminosity_distance(z).value
    distances.append(lumidist)
#    distances[counter]=lumidist
#    lightyears[counter]=lumidist*3.26*10.0**6.0
    lightyears.append(lumidist*3.26*10.0**6.0)
#    print(lightyears[counter])
#   correct for the effects of distance and flux dilution
    redshiftedflux = np.multiply(distance_sn**2.0,input_flux)
    redshiftedflux = np.divide(redshiftedflux, lumidist**2.0)
    redshiftedflux = np.divide(redshiftedflux, 1.0+z)
    gigalightyears = np.divide(lightyears, 10**9)
    print(z)
    print(lightyears[counter])
    print(gigalightyears[counter])


    mag_array=w_f_in(input_wave*(1.0+z),redshiftedflux)
#    print(mag_array[5])
    redshiftmags.append(mag_array[5])

#    print(redshifts[counter], redshiftmags[counter])	
#    print(lightyears[counter],redshiftmags[counter])	

#    print(z,redshifts[counter])

print(comovinggigalightyears)

# plotting
#plt.plot(t, np.poly1d(np.polyfit(t, y, 1))(t))
plt.ylabel('Observed Peak Magnitude (V)')
plt.xlabel('Distance [ Billion Light Years]')
#plt.title('Magnitudes versus redshift')
plt.plot(comovinggigalightyears, redshiftmags,'b*')
plt.plot([13, 17], [24, 24], color='k', linestyle='--', linewidth=2)
## invert y axis makes the brighter magnitude higher
plt.gca().invert_yaxis()
plt.show()

