import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import csv
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

'''
x = [1,2,3,4,5,6,7]
y = [1,4,9,16,25,36,49]
z = [0,1,0,-1,0,1,0]

ax.plot(x,y,z)
plt.show()
'''

#Plots file with filename in 3 dimensions: epoch, wavelength, and flux
#Assumes first row is 'Epoch, Wavelength, Flux' and following rows correspond to those values
#Does not currently validate file existence
#Currently only plots wavelengths between 1000 and 10000
def plot_3D(filename):
    epoch = np.zeros(0)
    wavelength = np.zeros(0)
    flux = np.zeros(0)
    firstline = True
    with open(filename) as csvfile:
        file_3D = csv.reader(csvfile, delimiter = ",")
        for row in file_3D:
            if(firstline):
                firstline = False
            elif(float(row[1]) < 10000 and float(row[1]) > 1000):
                epoch = np.append(epoch, [float(row[0])])
                wavelength = np.append(wavelength,[float(row[1])])
                flux = np.append(flux, [float(row[2])])
        ax.plot(epoch,wavelength,flux)
        plt.show()

plot_3D("../output/dat_to_csv.csv")
