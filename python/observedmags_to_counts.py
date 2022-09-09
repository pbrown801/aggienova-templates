import numpy as np
import csv
import math as math
from utilities import *
#from scipy import interpolate
import requests
from contextlib import closing
from filterlist_to_filterfiles import *
import string

'''
sn_name is a string with the desired supernova name
desired_filter_list is an array of the filters which have data
program writes two csv files
--magarray.csv has the magnitudes and errors for the desired filters
--countsarray.csv has the interpolated counts for all times at all filters
'''


def observedmags_to_counts_2(sn_name, desired_filter_list, template_spectrum, interpFilter = "UVW1"):
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
    
    for x, line in enumerate(data_list):
        if x != 0 and str(line[5]).upper() in desired_filter_list:
            # This checks if there is an uncertainty (error) given.  
            # If not, skip it as the magnitude is an upper limit not a measurement
            if line[3] != '':
                time.append(float(line[1]))
                mag.append(float(line[2]))
                emag.append(float(line[3]))
                band.append((str(line[5])).upper())

    filter_file_list,zeropointlist,pivotlist = filterlist_to_filterfiles(desired_filter_list, template_spectrum)

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

    #Adding the variables
    with open('../output/Test_A.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([2, "Time", time])
        writer.writerow([3, "Mag", mag])
        writer.writerow([4, "Emag", emag])
        writer.writerow([5, "Band", band])
        writer.writerow([6, "Interptimes", interpTimes])


    #contains counts directly from measured values
    counts_matrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)
    counterrs_matrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)
    #contains measured magnitudes
    magMatrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)
    #contains measured error on magnitudes
    emagMatrix = np.zeros((len(desired_filter_list),len(time)), dtype=object)

    #contains interpolated count values for all filters over all times
    interp_counts_matrix =  np.zeros((len(desired_filter_list),len(interpTimes)))
    interp_counterrs_matrix =  np.zeros((len(desired_filter_list),len(interpTimes)))
    interpMatrix = np.zeros((len(desired_filter_list),len(interpTimes)))

    for i in range(len(desired_filter_list)):
        measured_counts = np.zeros(len(time))
        measured_counterrs = np.zeros(len(time))
        measured_times = np.zeros(len(time))
        length = 0

###### does this have to be done in a for loop or can python operate on the whole row/column at once?

        for j in range(len(time)):

            if band[j] == desired_filter_list[i]:

                counts_matrix[i][j] = str(math.pow(10, -0.4*(mag[j]-zeropointlist[i])))  
                counterrs_matrix[i][j] = str(abs(float(counts_matrix[i][j])*float(emag[j])*-1.0857)) # need to check if this works

                magMatrix[i][j] = str(mag[j])
                emagMatrix[i][j] = emag[j]
                measured_counts[length] = float(counts_matrix[i][j])
                measured_counterrs[length] = float(counterrs_matrix[i][j])
                measured_times[length] = time[j]
                length += 1
            else:
                counts_matrix[i][j] = ''
                counterrs_matrix[i][j] = ''
                magMatrix[i][j] = ''
                emagMatrix[i][j] = ''
        measured_counts.resize(length)
        measured_counterrs.resize(length)
        measured_times.resize(length)
        interp_counts_matrix[i] = np.interp(interpTimes, measured_times, measured_counts)
        interp_counterrs_matrix[i] = np.interp(interpTimes, measured_times, measured_counterrs)

    column_err_names = []

    for l in range(len(desired_filter_list)):
        column_err_names.append(desired_filter_list[l]+'err')

    column_names = ['Time (MJD)']

    for l in range(len(desired_filter_list)):
        column_names.append(desired_filter_list[l])
        column_names.append(column_err_names[l])


    with open('../output/MAGS/'+ sn_name + '_magarray.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([column_names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+2*len(desired_filter_list),dtype=object)
            line[0] = str(interpTimes[i])
            for j in range(0,len(desired_filter_list)):
                line[2*j + 1] = magMatrix[j][i]
                line[2*j + 2] = emagMatrix[j][i]
            writer.writerow(line)


    with open('../input/COUNTS/'+ sn_name + '_countsarray.csv', 'w', newline ='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([column_names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+2*len(desired_filter_list))
            line[0] = interpTimes[i]
            for j in range(0,len(desired_filter_list)):
                line[2*j+1] = interp_counts_matrix[j][i]
                line[2*j+2] = interp_counterrs_matrix[j][i]
            writer.writerow(line)