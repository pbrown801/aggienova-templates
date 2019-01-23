import numpy as np
import matplotlib.pyplot as plt

#First I am grabbing each of the files in the folder

f1 = raw_input('Enter first file here:')
g1 = raw_input('Enter second file here:')

#Then I am telling the program to read the files

f2 = open(f1,'r')
g2 = open(g1,'r')

#Just defining variables here

bb_time = []
bb_mag = []
bb_err = []

vv_time = []
vv_mag = []
vv_err = []

#Now stripping each of the lists into columns
# and then assigning each column to time,mag,err respectively

for line in f2:
    
    line = line.rstrip()
    
    column = line.split()
    bb_time.append(column[0])
    bb_mag.append(column[1])
    bb_err.append(column[2])

for line in g2:
    
    line = line.rstrip()
    column1 = line.split()
    vv_time.append(column1[0])
    vv_mag.append(column1[1])
    vv_err.append(column1[2])

#stripping out the Null rows

i = 0
n=len(bb_time)

while i<n+1:
    for item in bb_mag:
        if item == 'NULL':
            a = bb_mag.index('NULL')
            del bb_time[a]
            del bb_mag[a]
            del bb_err[a]


    for item in vv_mag:
        if item == 'NULL':
            b = vv_mag.index('NULL')
            del vv_time[b]
            del vv_mag[b]
            del vv_err[b]
    i=i+1

#Changing strings into usable items

bb_time = map(float,bb_time)
bb_mag = map(float,bb_mag)
bb_err = map(float,bb_err)

vv_time = map(float,vv_time)
vv_mag = map(float,vv_mag)
vv_err = map(float,vv_err)

#Subtracting B-V

from operator import sub
bv_mag = map(sub, bb_mag, vv_mag)

#creating best fit line

bb_coeff = np.polyfit(bb_time,bb_mag,1)
vv_coeff = np.polyfit(vv_time,vv_mag,1)

#Best fit for color

bv_coeff = np.polyfit(bb_time,bv_mag,1)

#now plotting the points and their best fit lines
plt.plot(bb_time, np.poly1d(bb_coeff)(bb_time),'b')
plt.plot(vv_time, np.poly1d(vv_coeff)(vv_time),'y')
bb = plt.errorbar(bb_time,bb_mag,xerr=0,yerr=bb_err, fmt='o')
vv = plt.errorbar(vv_time,vv_mag,xerr=0,yerr=vv_err, fmt='^')
plt.legend([bb,vv],['bb','vv'])
plt.xlabel('Modified Julian Date')
plt.ylabel('Magnitude')
plt.gca().invert_yaxis()
plt.show()

plt.plot(bb_time,bv_mag,'bo')
plt.plot(bb_time, np.poly1d(bv_coeff)(bb_time),'r')
plt.xlabel('Modified Julian Date')
plt.ylabel('B-V')
plt.show()

#Determining the time of max light
bv_mag = np.asarray(bv_mag)
vv_time = np.asarray(vv_time)
t_v = -(bv_mag - 0.725)/(0.0118)+60
j=0
max_light = []
m = len(bv_mag)
while j<m:
    if t_v[j]>30 and t_v[j]<95:
        max_light.append(vv_time[j]-t_v[j])
    else:
        pass
    j=j+1

avg_time = sum(max_light) / len(max_light)

print('The estimated time of maximum light is:')
print(avg_time)
