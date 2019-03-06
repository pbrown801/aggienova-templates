#an extension of the first code
#Emily adding on to readcsv.py


import numpy as np
import matplotlib.pyplot as plt
#import csv

#set something here where we can type the input file name
#then change data below to pick which file to use

sn_name = input('Supernova name: ')
dataSN2007af = open('../input/'+'SN2007af_osc.csv', 'r+')

data = dataSN2007af.read()
data = data.splitlines()
data_list = []
for line in data:
    data_list.append(line.split(','))

time = []
mag = []
emag = []
band = []

for x, line in enumerate(data_list):
    if x != 0:
        time.append(float(line[1]))
        mag.append(float(line[2]))
        emag.append(str(line[3]))
        band.append(str(line[5]))

#print(band.count('UVM2'))
#bands: B(263), V(262), UVW2(156), UVM2(136), UVW1, U(48), H, J, Y

#float_emag = []
#float_k = []
#for i in range(len(emag)):
    #if emag[i] =='':
        #emag[i] = '0'
#it changed blank spaces to 0!

#for k in range(len(emag)):
    #float_k = float(emag[k])
    #float_emag.append(float_k)
#print(float_emag)
#it converted everything to floats!

u_time = []
u_mag = []
u_emag = []
u_band = []
#new_data = []

#this section specifies data points based on which band was used
for j in range(len(band)):
    if band[j] =='U':
        u_time.append(time[j])
        u_mag.append(mag[j])
        u_emag.append(emag[j])
        u_band.append(band[j])
#print(band)
#to test that this piece of code is working


names = ['Time (MJD)', 'Magnitude', 'Magnitude Error', 'Band']

import csv

with open('../output/'+'SN2007af_countsarray.csv', 'w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',')
    writer.writerows([names])
    for i in range(0,len(u_time)):
        line = [u_time[i], u_mag[i], u_emag[i], u_band[i]]
        writer.writerow(line)
    #print('Points written sucessfully to file')


#changes every time the code runs




#notes 2/20/19:
#input SNname_osc.csv
#output SNname_countarray.csv
# columns MJD, filtername1, ...
#filters we want uvw2, uvm2, uvw1, u, b, g, v, r, i, j, h, k
#j, h, k are the only ones withough corresponding filters


#end of code
