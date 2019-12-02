# code to take in emily's csv file and make plot of count rate vs mjd including all filters_curves
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

# applying the file to be passed through the entire code
def validation_plotting(filters_curve,count_rate,mjd,mangled_counts, sn_name):
    # pull the count rate, mangled counts, and mjd for u filters_curve
    pd.read_csv('../input/'+str(sn_name)+'_countsarray.csv', skiprows=1)
    pd.read_csv('../input/'+str(sn_name)+'_mangledcounts.csv', skiprows=1)
    for i in range(len(filters_curve)):
        cur_count = count_rate[:,i]
        mng_count = mangled_counts[:,i]
        x = mjd
        y = cur_count
        y2 = mng_count
        # commenting this out eliminates the extra blank figure
        #plt.figure()
        plt.plot(x, y, color='blue', linewidth=2)
        plt.plot(x, y2, color='red', linewidth=2)
        plt.title('Comparison Plot')
        plt.xlabel('Time (mjd)')
        plt.ylabel('Count rate')
        legend_items = ("Observed" +filters_curve[i], "Output "+filters_curve[i])
        plt.legend(legend_items)
        if filters_curve[i] == 'UVW1':
            plt.show()
        plt.savefig("../output/"+sn_name+filters_curve[i]+".png")
        plt.clf()

 