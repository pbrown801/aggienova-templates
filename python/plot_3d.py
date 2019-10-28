import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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

#color change along wavelength instead of flux like it is now
def plot_3D(x,y,z,name):
    X,Y = np.meshgrid(x,y)
    # Gx, Gy = np.gradient(z)
    surf = ax.plot_surface(X, z, Y, cmap=cm.hsv,
                       linewidth=0, antialiased=False)
    '''
    surf = ax.plot_surface(X, Y, z, cmap=cm.coolwarm,
    surf = ax.plot_surface(X, Y, z, cmap=[('Sequential', ['Reds', 'Oranges', 'Greens', 'Blues', 'Purples', 'Greys'])],
                       linewidth=0, antialiased=False)
    #cmaps['Sequential'] = ['Reds', 'Oranges', 'Greens', 'Blues', 'Purples', 'Greys']
    '''
    # cm['Sequential'] = ['Reds', 'Oranges', 'Greens', 'Blues', 'Purples', 'Greys']
    # ax.set_color_cycle(['red','orange','yellow','green','blue','8000FF','purple','808080','660000'])
    # ax.plot(x,y,z)
    plt.title(name)
    ax.set_xlabel('Time (mjd)')
    ax.set_ylabel('Wavelength')
    ax.set_zlabel('Flux')
    plt.show()
