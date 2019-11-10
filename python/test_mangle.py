import numpy as np
import matplotlib.pyplot as plt
from mangle_simple import *
from mangle_poly import *
from validation_plotting import *
import argparse
from observedmags_to_counts import *
from filterlist_to_filterfiles import *
from mangled_to_counts import *

#####################

if __name__ == "__main__":

    spectrum_file='../spectra/SN2011fe_uv.dat'
#    template_file='../spectra/vega.dat'
    template_file='../spectra/SN2006bp_uvmodel.dat'

    h = 6.6260755e-27
    c = 2.99792458e18
    hc = h*c #units of erg*A

    #input spectrum for test#
    spectrum_wave,spectrum_flux = np.loadtxt(spectrum_file,dtype=float,usecols=(0,1),unpack=True)

    # calculate bolometric flux for test spectrum
    spectrumbolo_lambda_range = np.where((spectrum_wave>=2000.0)&(spectrum_wave<=10000.0))
    spectrum_integrated_flux = np.trapz(spectrum_flux[spectrumbolo_lambda_range[0]]*spectrum_wave[spectrumbolo_lambda_range[0]]/hc,spectrum_wave[spectrumbolo_lambda_range[0]])

    test_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I', 'J', 'H', 'K']
    filter_file_list,zeropointlist,pivotlist = filterlist_to_filterfiles(test_filter_list)
    
    spectrum_spec =np.column_stack((spectrum_wave,spectrum_flux))
    counts_in = get_counts_multi_filter(spectrum_spec,filter_file_list)





    #   Now test a mangling method to see how well the template spectrum can be forced to match the input spectrum

    mangled_spec_wave, mangled_spec_flux = mangle_simple(template_file, filter_file_list, zeropointlist,pivotlist, counts_in) 
     
    mangledbolo_lambda_range = np.where((mangled_spec_wave>=2000.0)&(mangled_spec_wave<=10000.0))
    mangled_integrated_flux = np.trapz(mangled_spec_flux[mangledbolo_lambda_range[0]]*mangled_spec_wave[mangledbolo_lambda_range[0]]/hc,mangled_spec_wave[mangledbolo_lambda_range[0]])
    
    print(' ')
    print('mangle_simple % difference = ', 100.0*(mangled_integrated_flux-spectrum_integrated_flux)/spectrum_integrated_flux)
     
    plot.plot(spectrum_wave[spectrumbolo_lambda_range[0]], spectrum_flux[spectrumbolo_lambda_range[0]])
    plot.plot(mangled_spec_wave[mangledbolo_lambda_range[0]], mangled_spec_flux[mangledbolo_lambda_range[0]])
    plot.show()

    #  this completes one test


    
    #   Now test a different method

    mangled_spec_wave, mangled_spec_flux = mangle_poly(template_file, filter_file_list, zeropointlist,pivotlist, counts_in) 
     
    mangledbolo_lambda_range = np.where((mangled_spec_wave>=2000.0)&(mangled_spec_wave<=10000.0))
    mangled_integrated_flux = np.trapz(mangled_spec_flux[mangledbolo_lambda_range[0]]*mangled_spec_wave[mangledbolo_lambda_range[0]]/hc,mangled_spec_wave[mangledbolo_lambda_range[0]])
    
    print(' ')
    print('mangle_simple % difference = ', 100.0*(mangled_integrated_flux-spectrum_integrated_flux)/spectrum_integrated_flux)
     
    plot.plot(spectrum_wave[spectrumbolo_lambda_range[0]], spectrum_flux[spectrumbolo_lambda_range[0]])
    plot.plot(mangled_spec_wave[mangledbolo_lambda_range[0]], mangled_spec_flux[mangledbolo_lambda_range[0]])
    plot.show()



