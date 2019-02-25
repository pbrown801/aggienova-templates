# utilities.py

import os.path
import sys
import csv
import pandas as pd
import numpy as np

def csv_to_ascii(inFile,outFile):
    """
        Converts csv file to ascii file
    """
    outFile = outFile+'.txt'
    with open(outFile,'w') as output:
        with open(inFile) as csvinp:
            reader = csv.reader(csvinp,delimiter = ',')
            for row in reader:
                for col in row:
                    output.write(str(col) + ' ')
                output.write('\n')

def dat_to_csv(dat):
    """
        converter function between .dat and .csv
    """
    input_file = '../input/'+dat
    output_file = '../output/'+dat+'.csv'
    df = pd.read_csv(input_file,skiprows=1,header=None,skipinitialspace=True,sep=' ',names=['Wavelength','Flux'])
    out_df = pd.DataFrame({'Epoch':[0]*len(df)})
    out_df = out_df.join(df)
    out_df.to_csv(output_file,index=False)

def spectrum_to_csv(wavelength,flux,name):
    """
        converter function between spectra and csv
    """
    output_file = '../output/'+name+'.csv'
    data = {'Epoch': [0]*len(wavelength),
            'Wavelength': wavelength,
            'Flux': flux
            }

    df = DataFrame(data,columns= ['Epoch','Wavelength', 'Flux'])
    df.to_csv(output_file,index=False)
