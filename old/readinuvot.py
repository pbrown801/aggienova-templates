import matplotlib.pyplot as plt
import numpy as np
import math
from operator import itemgetter


snname = 'SN2015F'
filename = snname + '_uvotB15.1.dat'
data = open(filename, 'r')

for line in data:
	if not line[0]== '#':
		continue
	lines = np.genfromtxt(data, dtype=[('filter', 'S20'),('mjd',float),('mag',None),('magerr',None),('exposure',float),('elapse',float)], usecols=(0,1,2,3,10,11), unpack= True)

#Sorting SN into groups based on MJD +/- dt
mjdsorted = sorted(lines, key=itemgetter(1))
dt = 0.1500
ends = mjdsorted[0][1]
mjdgrouped = []
start = 0 
count = 1
filter1 ='UVW1'
filter2 = 'UVW2'


mjds = []
for j in mjdsorted:
	mjds.append(j[1])
'''
bins= np.arange(mjds[0],mjds[-1],dt)
grouped = np.digitize(mjds,bins)
groups = []

for i in range(len(grouped)):
	groups.append(grouped[i])
'''

for i in range(len(mjdsorted)):
	if i ==0:
		start=0
		
	else:
		if mjdsorted[i][1] < mjdsorted[i-1][1] + dt:
			count +=1
		
		else:
			mjdgrouped.append(mjdsorted[start:i])
			start = i
mjdgrouped.append(mjdsorted[start:])



def colorseries(filter1, filter2):
	mag1s = []
	mag2s = []
	error1temp = []
	error2temp = []
	errors = []
	dates = []
	for j in mjdgrouped:	

		for m in range(len(j)):
			dates.append(j[m][0])
	
		if filter1 in dates and filter2 in dates:
				
			for k in range(len(j)):
				if j[k][0] == filter1:
					mag1s.append(j[k][2])
					error1temp.append(j[k][3])
					
				if j[k][0] == filter2:
					mag2s.append(j[k][2])
					error2temp.append(j[k][3])
		if filter1 not in dates:
			mag1s.append(np.nan)
			error1temp.append(np.nan)
			for k in range(len(j)):
				if j[k][0] == filter2:
					mag2s.append(j[k][2])		
					error2temp.append(j[k][3])
		if filter2 not in dates:
			mag2s.append(np.nan)
			error2temp.append(np.nan)
			for k in range(len(j)):
				if j[k][0] == filter1:
					mag1s.append(j[k][2])		
					error1temp.append(j[k][3])
		del dates[:]
	maga = np.asarray(mag1s)
	magb = np.asarray(mag2s)
	error1temps = np.asarray(error1temp)
	error2temps = np.asarray(error2temp)
	errors = np.sqrt(error1temps**2 + (error2temps)**2)	
	color = maga-magb		
	return color, mag1s, mag2s, errors
colorseries, mag1, mag2, errorseries= colorseries(filter1,filter2)

def epochseries(unavg, checkfilter1, checkfilter2):
	sum = 0
	skip = 0
	num = 0	
	avgepoch = []
	temp=[]
	
	for k in unavg:
		sum = 0
		num = 0	
		for j in range(len(k)):
			if k[j][0] not in temp:	
				temp.append(k[j][0])
		
			
		for step in range(len(k)):
			
			if checkfilter1 not in temp and checkfilter2 not in temp:
				skip += 1
				avgepoch.append(np.nan)

			else:

				#print k[step][0]
				sum += k[step][1]
				num += 1.0
				
		del temp[:]
		
		
		if num != 0:
			avgt = sum/num
			avgepoch.append(avgt)
		
	return avgepoch
timeseries = epochseries(mjdgrouped,filter1, filter2)





plt.ion()
plt.figure()
plt.plot(timeseries,colorseries, 'o', linestyle = 'None', c = 'r')
plt.errorbar(timeseries, colorseries, yerr = errorseries, c='r', fmt='o')
plt.xlabel('MJD')
ylabel = filter1 + '-'+filter2
plt.ylabel(ylabel)
plt.title(snname)
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

plt.show()





data.close()
