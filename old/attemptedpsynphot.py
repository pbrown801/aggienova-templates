
'''
trying to use the pysynphot version so we could use the LSST or WFIRST bands

from astropy import units as u
from pysynphot import units


import os
import numpy as np
import pysynphot as S



filter_array='/Users/pbrown/Desktop/Dropbox/SN/snscripts/csp/CSP_filter_package/'+['u_texas_WLcorr_atm.txt','g_texas_WLcorr_atm.txt', 'r_texas_WLcorr_atm.txt', 'i_texas_WLcorr_atm.txt', 'yfilter', 'jfilter', 'hfilter', 'kfilter' ]

filter_array=["$SNSCRIPTS/UVW2_2010.txt","$SNSCRIPTS/UVM2_2010.txt","$SNSCRIPTS/UVW1_2010.txt","$SNSCRIPTS/U_UVOT.txt", '$SNFOLDER/filters/LSST/LSST_u.dat','$SNFOLDER/filters/LSST/LSST_g.dat', '$SNFOLDER/filters/LSST/LSST_r.dat', '$SNFOLDER/filters/LSST/LSST_i.dat', '$SNFOLDER/filters/LSST/LSST_z.dat', '$SNFOLDER/filters/LSST/LSST_y4.dat', '$SNFOLDER/filters/VIDEO/Bessell_J.dat', '$SNFOLDER/filters/VIDEO/Bessell_H.dat', '$SNFOLDER/filters/VIDEO/Bessell_K.dat' ]



bp = S.FileBandpass('johnson,v')

sp = S.Vega

from pysynphot import Observation
obs = Observation(sp, bp)

print(obs)
'''

import numpy as np


from spectrophot_array_in import *


vega_wave,vega_flux = np.loadtxt('spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)

w_f_in(vega_wave,vega_flux)

print(mag_array)

