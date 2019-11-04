import numpy as np
import csv
import math as math
from scipy import interpolate
import string
import pandas as pd

'''
sn_name is a string with the desired supernova name
observed_filter_list is an array of the filters which have data
program writes two csv files
--magarray.csv has the magnitudes and errors for the desired filters
--countsarray.csv has the interpolated counts for all times at all filters
'''


def observedmags_to_counts(sn_name, desired_filter_list, interpFilter = "UVW1"):
    input_file = open('../input/'+ sn_name + '_osc.csv', 'r+')

    data = input_file.read()
    data = data.splitlines()
    data_list = []
    for line in data:
        data_list.append(line.split(','))

    time = []
    mag  = []
    emag = []
    band = []

    
    #contains true or false depending on whether or not there is a non-zero observation for that filter
    # start with false and change to true if the filter is found
    filterFound = [False for i in range(len(desired_filter_list))]
    #for i in range(0, len(desired_filter_list)):
        #filterFound.append(False)
    
    for x, line in enumerate(data_list):
        if x != 0 and str(line[5]).upper() in desired_filter_list:
            time.append(float(line[1]))
            mag.append(float(line[2]))
            emag.append(str(line[3]))
            band.append((str(line[5])).upper())
            
            # this sets the flag to true if there.
            # probably a little slower since it doesn't need to be set so many times
            if mag[-1] > 0:              
                filterFound[desired_filter_list.index(band[-1])] = True
          
    # make a new list of which of the desired filters is actually observed  
    observed_filter_list = []
    for i in range(0, len(desired_filter_list)):
        if filterFound[i]:
            observed_filter_list.append(desired_filter_list[i])
 
    interpFirst = 1000000000000000
    interpLast = -1000000000000000
    for i in range(0, len(time)):
        if(band[i] == interpFilter and mag[i] > 0):
            if(time[i] < interpFirst):
                interpFirst = time[i]
            if(time[i] > interpLast):
                interpLast = time[i]

    interpTimes = []
    #for nonzero filters in interval of interpolation
    for i in range(0, len(time)):
        if interpFirst <= time[i] <= interpLast:
            if band[i] == interpFilter:
                interpTimes.append(time[i])


    #contains counts directly from measured values
    countsMatrix = np.zeros((len(observed_filter_list),len(time)), dtype=object)
    #contains measured magnitudes
    magMatrix = np.zeros((len(observed_filter_list),len(time)), dtype=object)
    #contains measured error on magnitudes
    emagMatrix = np.zeros((len(observed_filter_list),len(time)), dtype=object)
    #contains interpolated count values for all filters over all times
    interpMatrix = np.zeros((len(observed_filter_list),len(interpTimes)))

    for i in range(len(observed_filter_list)):
        measured_counts = np.zeros(len(time))
        measured_times = np.zeros(len(time))
        length = 0

# make dataframe from pandas
# operator on rows and columns from that
###### does this have to be done in a for loop or can python operate on the whole row/column at once?
        for j in range(len(time)):


            if band[j] == observed_filter_list[i]:
                import zeropointdictionary
                countsMatrix[i][j] = str(math.pow(10, -0.4*(mag[j]-20.0)))  # fake zeropoint added in until filterlist_to_filterfiles is updated to have zeropoints
#                countsMatrix[i][j] = str(math.pow(10, -0.4*(mag[j]-zeropointdictionary[j])))

                magMatrix[i][j] = str(mag[j])
                emagMatrix[i][j] = emag[j]
                measured_counts[length] = float(countsMatrix[i][j])
                measured_times[length] = time[j]
                length += 1
            else:
                countsMatrix[i][j] = ''
                magMatrix[i][j] = ''
                emagMatrix[i][j] = ''
        measured_counts.resize(length)
        measured_times.resize(length)
        interpMatrix[i] = np.interp(interpTimes, measured_times, measured_counts)

    names = ['Time (MJD)']

    for l in range(len(observed_filter_list)):
        names.append(observed_filter_list[l])

    with open('../output/'+ sn_name + '_magarray.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+2*len(observed_filter_list),dtype=object)
            line[0] = str(interpTimes[i])
            for j in range(0,len(observed_filter_list)):
                line[2*j + 1] = magMatrix[j][i]
                line[2*j + 2] = emagMatrix[j][i]
            writer.writerow(line)

    with open('../input/'+ sn_name + '_countsarray.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+len(observed_filter_list))
            line[0] = interpTimes[i]
            for j in range(0,len(observed_filter_list)):
                line[j+1] = interpMatrix[j][i]
            writer.writerow(line)



#end of code
