import numpy as np
import matplotlib.pyplot as plt

#####################

def findzeropoints(Filter):

    h = 6.6260755e-27
    c = 2.99792458e18
    hc = h*c #units of erg*A

    #Vega for reference#
    vega_wave,vega_flux = np.loadtxt('../spectra/vega.dat',dtype=float,usecols=(0,1),unpack=True)


    filter_lambda,filter_area = np.loadtxt(Filter,comments='#',usecols=(0,1), unpack=True)

    nonzero = np.where(filter_area > 0.0)
        
    filter_lambda = filter_lambda[nonzero]
    filter_area = filter_area[nonzero]


    ##############   calculate vega zeropoint for every filter from vega spectrum

    in_lambda_range = np.where((vega_wave>=min(filter_lambda))&(vega_wave<=max(filter_lambda)))
    interpolated_flux = np.interp(filter_lambda,vega_wave[in_lambda_range[0]],vega_flux[in_lambda_range[0]])
    zeropoint = round(2.5*np.log10(np.trapz(filter_area*interpolated_flux*filter_lambda/hc,filter_lambda)),2)

    return zeropoint




filterlist=['../filters/UVW2_2010.txt','../filters/UVM2_2010.txt', '../filters/UVW1_2010.txt','../filters/U_UVOT.txt','../filters/B_UVOT.txt','../filters/V_UVOT.txt']
zeropointlist=[]
for f in filterlist:
	zeropointlist.append(findzeropoints(f))
print(zeropointlist)	 





    

