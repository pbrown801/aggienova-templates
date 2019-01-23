'''


'''


import numpy as np
from astropy.cosmology import FlatLambdaCDM



npz_file = 'SN1987A.npz' # raw_input('Which .npz file?: ')
SN_name = npz_file[:-4]
data = np.load(npz_file)

cosmo = FlatLambdaCDM(H0=73, Om0=0.3)

redshift = 0.005871
lumidist = cosmo.luminosity_distance(redshift)

print lumidist

distance_sn = 50
redwavelength, flux = [], []

redwavelength.append(data['wavelengthlist'])
flux.append(data['fluxlist'])

deredwavelength = np.divide(redwavelength,(1+redshift))

deredflux = np.multiply(distance_sn**2,flux)
deredflux = np.divide(deredflux, lumidist**2)
deredflux = np.divide(deredflux, 1+redshift)

print deredflux

# np.savetxt()
