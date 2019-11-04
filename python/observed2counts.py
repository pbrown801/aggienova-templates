import numpy as np
import matplotlib.pyplot as plt
import csv

#commented out below where we can type the input file name
#then change data below to pick which file to use

#sn_name = input('Supernova name: ')
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


filterlist = ['UVW2','UVW2 error', 'U', 'U error', 'UVM2', 'UVM2 error', 'UVW1', 'UVW1 error', 'B', 'B error', 'G', 'G error', 'V', 'V error', 'R', 'R error', 'I', 'I error', 'J', 'J error', 'H', 'H error', 'K', 'K error']


uvw2_mag = []
uvw2_emag = []
uvw2_mag = [mag[j] for j in xrange(len(time)) if band[j] == 'UVW2' else '']
uvw2_emag = [emag[j] for j in xrange(len(time)) if band[j] == 'UVW2' else '']
'''
for j in range(len(time)):
    if band[j] == 'UVW2':
        uvw2_mag.append(mag[j])
        uvw2_emag.append(emag[j])
    else:
        uvw2_mag.append('')
        uvw2_emag.append('')
'''

u_mag = []
u_emag = []
for j in range(len(time)):
    if band[j] == 'U':
        u_mag.append(mag[j])
        u_emag.append(emag[j])
    else:
        u_mag.append('')
        u_emag.append('')

uvm2_mag = []
uvm2_emag = []
for j in range(len(time)):
    if band[j] == 'UVM2':
        uvm2_mag.append(mag[j])
        uvm2_emag.append(emag[j])
    else:
        uvm2_mag.append('')
        uvm2_emag.append('')

uvw1_mag = []
uvw1_emag = []
for j in range(len(time)):
    if band[j] == 'UVW1':
        uvw1_mag.append(mag[j])
        uvw1_emag.append(emag[j])
    else:
        uvw1_mag.append('')
        uvw1_emag.append('')

b_mag = []
b_emag = []
for j in range(len(time)):
    if band[j] == 'B':
        b_mag.append(mag[j])
        b_emag.append(emag[j])
    else:
        b_mag.append('')
        b_emag.append('')

g_mag = []
g_emag = []
for j in range(len(time)):
    if band[j] == 'G':
        g_mag.append(mag[j])
        g_emag.append(emag[j])
    else:
        g_mag.append('')
        g_emag.append('')

v_mag = []
v_emag = []
for j in range(len(time)):
    if band[j] == 'V':
        v_mag.append(mag[j])
        v_emag.append(emag[j])
    else:
        v_mag.append('')
        v_emag.append('')

r_mag = []
r_emag = []
for j in range(len(time)):
    if band[j] == 'R':
        r_mag.append(mag[j])
        r_emag.append(emag[j])
    else:
        r_mag.append('')
        r_emag.append('')

i_mag = []
i_emag = []
for j in range(len(time)):
    if band[j] == 'I':
        i_mag.append(mag[j])
        i_emag.append(emag[j])
    else:
        i_mag.append('')
        i_emag.append('')

j_mag = []
j_emag = []
for j in range(len(time)):
    if band[j] == 'J':
        j_mag.append(mag[j])
        j_emag.append(emag[j])
    else:
        j_mag.append('')
        j_emag.append('')

h_mag = []
h_emag = []
for j in range(len(time)):
    if band[j] == 'H':
        h_mag.append(mag[j])
        h_emag.append(emag[j])
    else:
        h_mag.append('')
        h_emag.append('')

k_mag = []
k_emag = []
for j in range(len(time)):
    if band[j] == 'K':
        k_mag.append(mag[j])
        k_emag.append(emag[j])
    else:
        k_mag.append('')
        k_emag.append('')

names = ['Time (MJD)']
for l in range(len(filterlist)):
    names.append(filterlist[l])


with open('../output/'+'SN2007af_magarray.csv', 'w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',')
    writer.writerows([names])
    for i in range(0,len(time)):
        line = [time[i], uvw2_mag[i], uvw2_emag[i], uvm2_mag[i], uvm2_emag[i], uvw1_mag[i], uvw1_emag[i], u_emag[i], u_emag[i], b_mag[i], b_emag[i], g_mag[i], g_emag[i], v_mag[i], v_emag[i], r_mag[i], r_emag[i], i_mag[i], i_emag[i], j_mag[i], j_emag[i], h_mag[i], h_emag[i], k_mag[i], k_emag[i]]
        writer.writerow(line)



with open('../output/'+'SN2007af_countsarray.csv', 'w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',')
    writer.writerows([names])
    for i in range(0,len(time)):
        line = [time[i], uvw2_mag[i], uvw2_emag[i], uvm2_mag[i], uvm2_emag[i], uvw1_mag[i], uvw1_emag[i], u_emag[i], u_emag[i], b_mag[i], b_emag[i], g_mag[i], g_emag[i], v_mag[i], v_emag[i], r_mag[i], r_emag[i], i_mag[i], i_emag[i], j_mag[i], j_emag[i], h_mag[i], h_emag[i], k_mag[i], k_emag[i]]
        writer.writerow(line)

flux=math.pow(10, -0.4*(mag[0])) + zeropoint 



#notes 2/20/19:
#input SNname_osc.csv
#output SNname_countarray.csv
# columns MJD, filtername1, ...
#filters we want uvw2, uvm2, uvw1, u, b, g, v, r, i, j, h, k
#j, h, k are the only ones withough corresponding filters


#end of code
