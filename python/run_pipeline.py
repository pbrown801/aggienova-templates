#  take an input spectrum
import pandas as pd
import numpy as np
from utilities import *
from mangle_simple import *
from validation_plotting import *

if __name__ == "__main__":
    sn_name = input('Supernova name: ') #assign sn name at beginning and look for that file as an input
    inFile = '../input/'+'SNtest_countsarray'+'.csv' #make this generic eventually with sn_name
    mjd_list = []
    counts_list = []

    with open(inFile) as csvinp:
        reader = csv.reader(csvinp,delimiter = ',')
        filter_curves_list_no_format = next(reader)[1:]
        filter_curves_list = list(map('../filters/{0}'.format, filter_curves_list_no_format))
        for row in reader:
            epoch = float(row[0])-0
            counts_in = list(map(float,row[1:]))

            mjd_list.append(epoch)
            counts_list.append(counts_in)

            template_spectrum = "SN2017erp_hst_20170629.dat" #Assign a template spectrum to use

            # mangled_spec_wave, mangled_spec_flux = mangle_simple(template_spectrum, filter_curves_list, counts_in) #mangle the spectrum to match the given count rates

            # mangling outputs spectrum that matches input counts by multiplying func by og spec

            # spectrum_to_csv(epoch,mangled_spec_wave,mangled_spec_flux,sn_name) #write csv with epoch, mangled_spec_wave, and mangled_spec_flux


    mjd_list = np.array(mjd_list,dtype='float')
    counts_list = np.array(counts_list,dtype='float')
    filter_curves_list_no_format = [x.split('_')[0] for x in filter_curves_list_no_format]
    print(mjd_list)
    print(counts_list)
    print(filter_curves_list_no_format)
    validation_plotting(filter_curves_list_no_format,counts_list,mjd_list) #Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis
