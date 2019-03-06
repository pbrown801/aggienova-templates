# code to take in emily's csv file and make plot of count rate vs mjd including all filters_curves
import numpy as np
import matplotlib.pyplot as plt
import csv

# applying the file to be passed through the entire code
def validation_plotting(filters_curve,count_rate,mjd):
    # pull the count rate and mjd for u filters_curve to then graph only that filters_curve
    # unsure if i add in any a general code for error bars


    for i in range(len(filters_curve)):
        cur_count = []
        cur_count = count_rate[:,i]
        x = mjd
        y = cur_count
        plt.plot(y,x)
        plt.title('Data for all bands')
        plt.ylabel('Time (mjd)')
        plt.xlabel('Count rate')
    legend_items = list(map('{0} band'.format,filters_curve))
    plt.legend(legend_items)
    plt.show()
