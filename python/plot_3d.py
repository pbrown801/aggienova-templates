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
plt.title('Name')

plt.show()
'''

#Plots file with filename in 3 dimensions: epoch, wavelength, and flux
#Assumes first row is 'Epoch, Wavelength, Flux' and following rows correspond to those values
#Does not currently validate file existence
def plot_3D(df,name):
    ax.plot(df.Epoch,df.Wavelength,df.Flux)
    plt.title(name)
    ax.set_xlabel('Time (mjd)')
    ax.set_ylabel('Wavelength')
    ax.set_zlabel('Flux')
    plt.show()
