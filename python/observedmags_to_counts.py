import numpy as np
import csv
import math as math
from scipy import interpolate
import string

'''
sn_name is a string with the desired supernova name
filterlist is an array of the filters being used
program writes two csv files
--magarray.csv has the magnitudes and errors for the desired filters
--countsarray.csv has the interpolated counts for all times at all filters
'''


#def observedmags_to_counts(sn_name, filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I'], interpFilter = "UVW1"):

#^^OLD do we need to hardcode the filters in like this?

def observedmags_to_counts(sn_name, filterlist, interpFilter = "UVW1"):
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

    '''
    #contains true or false depending on whether or not there is a non-zero observation for that filter
    filterFound = []
    for i in range(0, len(filterlist)):
        filterFound.append(False)
    '''

    for x, line in enumerate(data_list):
        if x != 0:
            time.append(float(line[1]))
            mag.append(float(line[2]))
            emag.append(str(line[3]))
            band.append((str(line[5])).upper())
            '''
            if mag[-1] > 0:
                filterFound[filterList.index(band[-1])] = True
            '''
    '''
    observed_bands = []
    for i in range(0, len(filterlist)):
        if filterFound[i]:
            observed_bands.append(band[i])
    band = observed_bands
    '''

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
    #filterSet = set([])
    for i in range(0, len(time)):
        if interpFirst <= time[i] <= interpLast:
            if band[i] == interpFilter:
                interpTimes.append(time[i])
            #if mag[i] > 0:
                #filterSet.add(band[i])

    #contains counts directly from measured values
    countsMatrix = np.zeros((len(filterlist),len(time)), dtype=object)
    #contains measured magnitudes
    magMatrix = np.zeros((len(filterlist),len(time)), dtype=object)
    #contains measured error on magnitudes
    emagMatrix = np.zeros((len(filterlist),len(time)), dtype=object)
    #contains interpolated count values for all filters over all times
    interpMatrix = np.zeros((len(filterlist),len(interpTimes)))

    for i in range(len(filterlist)):
        measured_counts = np.zeros(len(time))
        measured_times = np.zeros(len(time))
        length = 0

###### does this have to be done in a for loop or can python operate on the whole row/column at once?

        for j in range(len(time)):
            if band[j] == filterlist[i]:
                countsMatrix[i][j] = str(math.pow(10, -0.4*(mag[j]-17.38)))


#######      the 17.38 needs to be replaced with a filter-dependent zeropoint

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

    for l in range(len(filterlist)):
        names.append(filterlist[l])

    with open('../output/'+ sn_name + '_magarray.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+2*len(filterlist),dtype=object)
            line[0] = str(interpTimes[i])
            for j in range(0,len(filterlist)):
                line[2*j + 1] = magMatrix[j][i]
                line[2*j + 2] = emagMatrix[j][i]
            writer.writerow(line)

    with open('../input/'+ sn_name + '_countsarray.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows([names])
        for i in range(0,len(interpTimes)):
            line = np.zeros(1+len(filterlist))
            line[0] = interpTimes[i]
            for j in range(0,len(filterlist)):
                line[j+1] = interpMatrix[j][i]
            writer.writerow(line)



# sn_name1 = 'SN2007af'
# filterlist1 = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I']

# observedmags_to_counts(sn_name1, filterlist1)


#notes 2/20/19:
#input SNname_osc.csv
#output SNname_countarray.csv
# columns MJD, filtername1, ...
#filters we want uvw2, uvm2, uvw1, u, b, g, v, r, i, j, h, k
#j, h, k are the only ones withough corresponding filters

#end of code
