#  take an input spectrum
import pandas as pd
import numpy as np
from utilities import *
from mangle_simple import *
from validation_plotting import *


if __name__ == "__main__":
    sn_name = input('Supernova name: ') #assign sn name at beginning and look for that file as an input
    inFile = '../input/'+sn_name+'_countsarray'+'.csv' #make this generic eventually with sn_name
    mjd_list = []
    counts_list = []

    with open(inFile) as csvinp:
        reader = csv.reader(csvinp,delimiter = ',')
        filter_curves_list_no_format = next(reader)[1:]
        filter_curves_list = list(map('../filters/{0}'.format, filter_curves_list_no_format))
        df = pd.DataFrame(columns= ['Epoch','Wavelength', 'Flux'])
        for row in reader:
            epoch = float(row[0])-0
            counts_in = list(map(float,row[1:]))

            mjd_list.append(epoch)
            counts_list.append(counts_in)

            template_spectrum = "SN2017erp_hst_20170629.dat" #Assign a template spectrum to use

            mangled_spec_wave, mangled_spec_flux = mangle_simple(template_spectrum, filter_curves_list, counts_in) #mangle the spectrum to match the given count rates

            # mangling outputs spectrum that matches input counts by multiplying func by og spec

            data = pd.DataFrame({'Epoch': [epoch]*len(mangled_spec_wave),
                                 'Wavelength': mangled_spec_wave,
                                 'Flux': mangled_spec_flux})
            df = df.append(data)


    output_file = '../output/'+sn_name+'_template.csv'
    df.to_csv(output_file,index=False) #comment this out if you don't want to save everytime FUTURE: make a flag that handles this


    mjd_list = np.array(mjd_list,dtype='float')
    counts_list = np.array(counts_list,dtype='float')
    filter_curves_list_no_format = [x.split('_')[0] for x in filter_curves_list_no_format]

    filtered_df = df[(df.Wavelength > 1000) & (df.Wavelength < 10000) & (df.Epoch < 54330)]
    output_3d = '../output/'+sn_name+'_3d.csv'
    filtered_df.to_csv(output_3d,index=False) #comment this if you already have your df or dont want to save a filtered version FUTURE: flag to do this

    validation_plotting(filter_curves_list_no_format,counts_list,mjd_list) #Plot the mangled template count rates and the input count rates on the same plot with MJD or epoch on the x-axis

    from plot_3d import plot_3D
    # filtered_df = pd.read_csv(output_3d) #uncomment this if you have a saved df you just want to read and plot in 3d
    plot_3D(filtered_df,sn_name)
