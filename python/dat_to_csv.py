#converter script between .dat to .csv
import pandas as pd
import numpy as np

df = pd.read_csv('../input/vega.dat',skiprows=1,header=None,skipinitialspace=True,sep=' ',names=['Wavelength','Flux'])
out_df = pd.DataFrame({'Epoch':[0]*len(df/2)})
out_df = out_df.join(df)
out_df.to_csv('../output/dat_to_csv.csv',index=False)
