import numpy as np
import matplotlib.pyplot as plt
import csv
import math as math
from scipy import interpolate

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
mag  = []
emag = []
band = []

for x, line in enumerate(data_list):
    if x != 0:
        time.append(float(line[1]))
        mag.append(float(line[2]))
        emag.append(str(line[3]))
        band.append(str(line[5]))


filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B','V']



uvw2_counts = []
uvw2_mag = []
uvw2_emag = []
for j in range(len(time)):
    if band[j] == 'UVW2':
        uvw2_mag.append(mag[j])
        uvw2_emag.append(emag[j])
        uvw2_counts.append(math.pow(10, -0.4*(mag[j]-17.38)))
    else:
        uvw2_mag.append(0)
        uvw2_emag.append('')
        uvw2_counts.append('')

#new_uvw2_mag = [float(i) for i in uvw2_mag]
good=np.nonzero(uvw2_mag)[0]

goodtime=[]
goodmag=[]
for l in range(len(good)):
	goodtime.append(time[good[l]])
	goodmag.append(uvw2_counts[good[l]])

uvw2_interpcounts=np.interp(time, goodtime, goodmag)

uvm2_counts = []
uvm2_mag = []
uvm2_emag = []
for j in range(len(time)):
    if band[j] == 'UVM2':
        uvm2_mag.append(mag[j])
        uvm2_emag.append(emag[j])
        uvm2_counts.append(math.pow(10, -0.4*(mag[j]-16.85)))
    else:
        uvm2_mag.append(0)
        uvm2_emag.append('')
        uvm2_counts.append('')

good=np.nonzero(uvm2_mag)[0]
print(good)
goodtime=[]
goodmag=[]
for l in range(len(good)):
	goodtime.append(time[good[l]])
	goodmag.append(uvm2_counts[good[l]])

uvm2_interpcounts=np.interp(time, goodtime, goodmag)


uvw1_counts = []
uvw1_mag = []
uvw1_emag = []
for j in range(len(time)):
    if band[j] == 'UVW1':
        uvw1_mag.append(mag[j])
        uvw1_emag.append(emag[j])
        uvw1_counts.append(math.pow(10, -0.4*(mag[j]-17.44)))
    else:
        uvw1_mag.append(0)
        uvw1_emag.append('')
        uvw1_counts.append('')

good=np.nonzero(uvw1_mag)[0]

goodtime=[]
goodmag=[]
for l in range(len(good)):
	goodtime.append(time[good[l]])
	goodmag.append(uvw1_counts[good[l]])

uvw1_interpcounts=np.interp(time, goodtime, goodmag)


u_counts = []
u_mag = []
u_emag = []
for j in range(len(time)):
    if band[j] == 'U':
        u_mag.append(mag[j])
        u_emag.append(emag[j])
        u_counts.append(math.pow(10, -0.4*(mag[j]-18.34)))
    else:
        u_mag.append(0)
        u_emag.append('')
        u_counts.append('')


good=np.nonzero(u_mag)[0]

goodtime=[]
goodmag=[]
for l in range(len(good)):
	goodtime.append(time[good[l]])
	goodmag.append(u_counts[good[l]])

u_interpcounts=np.interp(time, goodtime, goodmag)

b_counts = []

b_mag = []
b_emag = []
for j in range(len(time)):
    if band[j] == 'B':
        b_mag.append(mag[j])
        b_emag.append(emag[j])
        b_counts.append(math.pow(10, -0.4*(mag[j]-19.11)))
    else:
        b_mag.append(0)
        b_emag.append('')
        b_counts.append('')

good=np.nonzero(b_mag)[0]

goodtime=[]
goodmag=[]
for l in range(len(good)):
	goodtime.append(time[good[l]])
	goodmag.append(b_counts[good[l]])

b_interpcounts=np.interp(time, goodtime, goodmag)


g_mag = []
g_emag = []
for j in range(len(time)):
    if band[j] == 'G':
        g_mag.append(mag[j])
        g_emag.append(emag[j])
    else:
        g_mag.append('')
        g_emag.append('')

v_counts = []
v_mag = []
v_emag = []
for j in range(len(time)):
    if band[j] == 'V':
        v_mag.append(mag[j])
        v_emag.append(emag[j])
        v_counts.append(math.pow(10, -0.4*(mag[j]-17.89)))
    else:
        v_mag.append(0)
        v_emag.append('')
        v_counts.append('')

good=np.nonzero(v_mag)[0]

goodtime=[]
goodmag=[]
for l in range(len(good)):
	goodtime.append(time[good[l]])
	goodmag.append(v_counts[good[l]])

v_interpcounts=np.interp(time, goodtime, goodmag)


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
        line = [time[i], uvw2_interpcounts[i], uvm2_interpcounts[i], uvw1_interpcounts[i], u_interpcounts[i], b_interpcounts[i],v_interpcounts[i] ]
        writer.writerow(line)



#notes 2/20/19:
#input SNname_osc.csv
#output SNname_countarray.csv
# columns MJD, filtername1, ...
#filters we want uvw2, uvm2, uvw1, u, b, g, v, r, i, j, h, k
#j, h, k are the only ones withough corresponding filters


#end of code
