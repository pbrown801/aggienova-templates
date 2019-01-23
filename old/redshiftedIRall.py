import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
#import pysynphot as S
from abspecphot import abspecphot

cosmo = FlatLambdaCDM(H0=73, Om0=0.3)

# testing
#vega_wave,vega_flux = np.loadtxt('spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)
#vega_u=abspecphot(vega_wave,vega_flux, 'filters/U_UVOT.txt')
#print(vega_u)

# Here is the input spectrum and the corresponding distance

input_wave,input_flux = np.loadtxt('spectra/Gaia16apd_uv.dat', dtype=float,usecols=(0,1),unpack=True)
# distance in Megaparsecs, here calculated from redshift for Gaia16apd
distance_sn=cosmo.luminosity_distance(0.102).value

wave11fe, flux11fe=np.loadtxt('spectra/SN2011fe_uv.dat', dtype=float,usecols=(0,1),unpack=True)
distance_11fe=6.7

wave16ccj, flux16ccj=np.loadtxt('spectra/SN2016ccj_uv.dat', dtype=float,usecols=(0,1),unpack=True)
distance_16ccj=cosmo.luminosity_distance(0.041).value

wave06aj, flux06aj=np.loadtxt('/Users/pbrown/Desktop/SN/localtemplates/ANT-SN2006aj.20A.sed.restframe.dat_upeakspectrum.dat', dtype=float,usecols=(0,1),unpack=True)
distance_06aj=0.000010
# in megaparsecs

#set redshift array and initialize other arrays which will have the same length
redshifts=[0.1,0.2,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.0,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
redshiftmags=[]
redshiftmags2=[]
redshift11femags=[]
redshift16ccjmags=[]
redshift11femags2=[]
redshift16ccjmags2=[]
redshift06ajmags=[]
redshift06ajmags2=[]
distances=[]
lightyears=[]

for counter in range(0,len(redshifts),1):
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

    redshifted11feflux = np.multiply(distance_11fe**2.0,flux11fe)
    redshifted11feflux = np.divide(redshifted11feflux, lumidist**2.0)
    redshifted11feflux = np.divide(redshifted11feflux, 1.0+z)

    redshifted16ccjflux = np.multiply(distance_16ccj**2.0,flux16ccj)
    redshifted16ccjflux = np.divide(redshifted16ccjflux, lumidist**2.0)
    redshifted16ccjflux = np.divide(redshifted16ccjflux, 1.0+z)

    redshifted06ajflux = np.multiply(distance_06aj**2.0,flux06aj)
    redshifted06ajflux = np.divide(redshifted06ajflux, lumidist**2.0)
    redshifted06ajflux = np.divide(redshifted06ajflux, 1.0+z)



    filter2='filters/F444W_NRC_and_OTE_ModAB_mean.txt'
    filter='filters/F200W_NRC_and_OTE_ModAB_mean.txt'
#    print(z)
#    abmag=[]
    abmag=abspecphot(wave16ccj*(1.0+z),redshifted16ccjflux,filter )
    ab16ccjmag=abmag
    ab16ccjmag2=abspecphot(wave16ccj*(1.0+z),redshifted16ccjflux,filter2 )

#    abmag=[]
    abmag=abspecphot(wave11fe*(1.0+z),redshifted11feflux,filter )
    ab11femag=abmag
    ab11femag2=abspecphot(wave11fe*(1.0+z),redshifted11feflux,filter2 )


    ab06ajmag=abspecphot(wave06aj*(1.0+z),redshifted06ajflux,filter )
    ab06ajmag2=abspecphot(wave06aj*(1.0+z),redshifted06ajflux,filter2 )

#    abmag=[]
    abmag=abspecphot(input_wave*(1.0+z),redshiftedflux,filter )
    abmag2=abspecphot(input_wave*(1.0+z),redshiftedflux,filter2 )

#    print(mag_array[5])
    redshiftmags.append(abmag)
    redshiftmags2.append(abmag2)
    redshift11femags.append(ab11femag)
    redshift11femags2.append(ab11femag2)
    redshift16ccjmags.append(ab16ccjmag)
    redshift16ccjmags2.append(ab16ccjmag2)
    redshift06ajmags.append(ab06ajmag)
    redshift06ajmags2.append(ab06ajmag2)
#    print(abmag)
goodmags,=(np.where(redshiftmags > 0))

color=np.subtract(redshiftmags,redshiftmags2)
color11fe=np.subtract(redshift11femags,redshift11femags2)
#color16ccj=np.subtract(redshift16ccjmags,redshift16ccjmags2)

#best fit line and plotting
#plt.ylabel(filter)
plt.ylabel('JWST F200 AB Mag')
#plt.ylabel('JWST F200-F444 AB Mag')
plt.xlabel('Redshift')
# plt.title('Gaia16apd Spectrum')
#plt.plot(redshifts[goodmags[0][:]],redshiftmags[goodmags[0][:]],'b*')
#plt.plot(redshifts,color, 'b*',color='black')
#plt.plot(redshifts,color11fe, 'b*',color='blue')
#plt.plot(redshifts,color16ccj, 'b*',color='purple')
plt.plot(redshifts,redshiftmags, 'b*',color='black')
plt.plot(redshifts,redshift11femags,'b*',color='blue')
plt.plot(redshifts,redshift06ajmags,'b*',color='green')
# 16ccj has [] in mag array
#plt.plot(redshifts,redshift16ccjmags,'b*',color='green')
#plt.plot([4.5, 5.5], [28, 28], color='k', linestyle='--', linewidth=2)
## invert y axis makes the brighter magnitude higher
plt.gca().invert_yaxis()
#plt.ylim([29,24])
plt.show()
