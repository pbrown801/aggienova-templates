import matplotlib.pyplot as plt
import numpy as np
import math
import os
import sys

os.chdir(os.path.expanduser('~/Dropbox/SN/SOUSA/data'))

snname = sys.argv[1]
filename =  snname + '_uvotB15.1.dat'
savename = snname + '_pylightcurve.jpg'
data = open(filename, 'r')


#Initializing lists needed to plot the different filters separately
uvw2mjd = []
uvw2mag = []
uvw2magerr = []
uvm2mjd = []
uvm2mag = []
uvm2magerr = []
uvw1mjd = []
uvw1mag = []
uvw1magerr = []
umjd = []
umag = []
umagerr = []
bmjd = []
bmag = []
bmagerr = []
vmjd = []
vmag = []
vmagerr = []


#Reading the data in from the file
for line in data:
	if not line[0] == "#":
		continue
	lines= np.genfromtxt(data, dtype=[('filter','S20'),('mjd',float),('mag',None),('magerr',None)], usecols = (0,1,2,3), unpack=True)
filters1 = lines['filter']
mjd1 = lines['mjd']
mag1 = lines['mag']
magerr1 = lines['magerr']

#I needed to get rid of the NULL values in the ...15.1.dat files, so the next several lines are to make sure the 
#program doesn't shut down because of them
filterslist = []
mjdlist  = []
maglist = []
magerrlist = []
for i in range(len(filters1)):
	if not np.isnan(mag1[i]):
		filterslist.append(filters1[i])
		maglist.append(mag1[i])
		mjdlist.append(mjd1[i])
		magerrlist.append(magerr1[i])
filters = np.array(filterslist)
mjd = np.array(mjdlist)
mag = np.array(maglist)
magerr = np.array(magerrlist)	



#breaking up the filters, mjd, mag, and magerr arrays into separate arrays to make plotting easier
for i in range(len(filters)):
	if filters[i] == 'UVW2':
		uvw2mjd.append(mjd[i])
		uvw2mag.append(mag[i])
		uvw2magerr.append(magerr[i])
	if filters[i] == 'UVM2':
		uvm2mjd.append(mjd[i])
		uvm2mag.append(mag[i])
		uvm2magerr.append(magerr[i])
	if filters[i] == 'UVW1':
		uvw1mjd.append(mjd[i])
		uvw1mag.append(mag[i])
		uvw1magerr.append(magerr[i])
	if filters[i] == 'U':
		umjd.append(mjd[i])
		umag.append(mag[i])
		umagerr.append(magerr[i])
	if filters[i] == 'B':
		bmjd.append(mjd[i])
		bmag.append(mag[i])
		bmagerr.append(magerr[i])
	if filters[i] == 'V':
		vmjd.append(mjd[i])
		vmag.append(mag[i])
		vmagerr.append(magerr[i])

##########This begins plotting portion##########
plt.ion() #turns on interactive plotting
fig =plt.figure()
ax = fig.add_subplot(111)
#The next several lines are just to make sure the program doesn't shut down if one of the filters is missing 
if len(uvw2mag) > 0:
	plt.scatter(uvw2mjd, uvw2mag, linestyle='-', linewidth=1,marker='o', facecolors='none', edgecolors='r', s=30, label='uvw2', color = 'r')
	plt.errorbar(uvw2mjd, uvw2mag, yerr=uvw2magerr, elinewidth=2, capthick = 2, color = 'r')
if len(uvm2mag) > 0:
	plt.scatter(uvm2mjd, uvm2mag, linestyle='-', linewidth=1,marker='v',facecolors='none', edgecolors='m', s=30, label='uvm2', color= 'm')
	plt.errorbar(uvm2mjd, uvm2mag, yerr=uvm2magerr, elinewidth=2, capthick = 2, color='m')
if len(uvw1mag) > 0:
	plt.scatter(uvw1mjd, uvw1mag, linestyle='-', linewidth=1,marker='^', facecolors='none', edgecolors='k', s=30, label='uvw1', color= 'k')
	plt.errorbar(uvw1mjd, uvw1mag, yerr=uvw1magerr, elinewidth=2, capthick = 2, color='k')
if len(umag) > 0:
	plt.scatter(umjd, umag, linestyle='-', linewidth=1,marker='D',facecolors='none', edgecolors='c', s=30, label='uvot u', color= 'c')
	plt.errorbar(umjd, umag, yerr=umagerr, elinewidth=2, capthick = 2, color='c')
if len(bmag) > 0:
	plt.scatter(bmjd, bmag, linestyle='-', linewidth=1,marker='*',facecolors='none', edgecolors='b', s=50, label='uvot b', color= 'b')
	plt.errorbar(bmjd, bmag, yerr=bmagerr, elinewidth=2, capthick = 2, color='b')
if len(vmag) > 0:
	plt.scatter(vmjd, vmag, linestyle='-', linewidth=1,marker='s',facecolors='none', edgecolors='g', s=30, label='uvot v', color= 'g')
	plt.errorbar(vmjd, vmag, yerr=vmagerr, elinewidth=2, capthick = 2, color='g')


#ax.legend(bbox_to_anchor=(1.32,0.83))
#If you have labels specified in the plotting commands above, all you have to do is add this line to make a legend
#Also, apparently you can set the location to 'best' so it'll place it wherever python thinks it's the best
ax.set_xlabel('Modified Julian Date')

#ax.set_ylabel('Observed Vega Magnitude')

ax.set_title(snname, fontsize = 16)
#plt.title('UVOT Light Curves', fontsize = 12) 
#there aren't title and subtitle commands so instead I used suptitle and title to get a makeshift main title and subtitle

ax.axis([int(mjd.min())-1, math.ceil(np.amax(mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
'''
In order to make the axis format correctly, I used the minimum and maxiumum values for the MJD +/- 1 (in order to give the plots some extra
 space) on the x-axis, and the min and max values for the magnitude. The functions int() and math.ceil() are used to round the numbers to the
 nearest whole number to make the ends of the graph neater.
'''
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
#The line above makes sure that the x axis is formatted correctly. The Offset option in matplotlib is automatically activated, so for big
#numbers like the MJD, it cuts it off in a strange way that is awful to look at. This makes it readable.
os.chdir(os.path.expanduser('~/Dropbox/SN/madison/'))
fig.savefig(savename) #you can uncomment this line if you want to save the figure to the SN file

fig.show()
os.chdir(os.path.expanduser('~/Dropbox/SN/madison/'))