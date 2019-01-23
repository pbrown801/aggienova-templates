import numpy as np
import matplotlib.pyplot as plt
from operator import truediv

### Here you would need to input an array of counts to start with
### Previously attached this code to the end of spectrophot.

counts_array=[

### Starting with the factors associated with Pickles

factor = [5.77E-16, 7.47E-16, 4.06E-16, 1.53E-16, 1.31E-16, 2.61E-16]
factor = np.asarray(factor, dtype=float)

new_WL = [1928,2246,2600,3465,4392,5468]
flux_top=[]
new_counts=[12341,12341234,123412341,1234134,12341234,1234132]
flag = [0,0,0,0,0,0]


### Iterating over until we are within 10% of the input counts
### Will print the value for the flux for each iteration

while sum(flag) != 6:
    flux_top=[]
    for count in range(0,len(counts_array)):

        flux_top.append(counts_array[count]*factor[count])

    for x in range(len(flux_top)):
    
        new_spec = np.interp(filter_wave[x], new_WL, flux_top)
        
        new_counts[x] = np.trapz(new_spec*filter_array[x]*filter_wave[x]/hc,filter_wave[x])
        
        factor = map(truediv, flux_top, new_counts)

        if abs(new_counts[x] - counts_array[x]) <= 0.1*counts_array[x]:
            flag[x] = 1
        else:
            flag[x] = 0
    print flux_top

plt.plot(new_WL, flux_top, 'ko')

plt.show()
