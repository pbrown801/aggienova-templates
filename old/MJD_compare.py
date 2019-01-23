import numpy as np
import matplotlib.pyplot as plt
from operator import truediv

print "Make sure you're in the right directory before running!"
print ""

### Run through jsonphot_extract.py before attempting to run this code!!!
### This will create a .dat file for each of the filters.

SNname = raw_input("Enter supernova name: ")

print ''
SN_U = '%s_phot_U.dat' % (SNname)
SN_B = '%s_phot_B.dat' % (SNname)
SN_V = '%s_phot_V.dat' % (SNname)
SN_W2 = '%s_phot_W2.dat' % (SNname)
SN_W1 = '%s_phot_W1.dat' % (SNname)
SN_M2 = '%s_phot_M2.dat' % (SNname)


U_mag,U_err,U_MJD = np.loadtxt(SN_U,comments='#',delimiter='\t', usecols = (0,1,2), unpack = True)
B_mag,B_err,B_MJD = np.loadtxt(SN_B,comments='#',delimiter='\t', usecols = (0,1,2), unpack = True)
M2_mag,M2_err,M2_MJD = np.loadtxt(SN_M2,comments='#',delimiter='\t', usecols = (0,1,2), unpack = True)
W2_mag,W2_err,W2_MJD = np.loadtxt(SN_W2,comments='#',delimiter='\t', usecols = (0,1,2), unpack = True)
W1_mag,W1_err,W1_MJD = np.loadtxt(SN_W1,comments='#',delimiter='\t', usecols = (0,1,2), unpack = True)
V_mag,V_err,V_MJD = np.loadtxt(SN_V,comments='#',delimiter='\t', usecols = (0,1,2), unpack = True)


ref = []
MJD_list = []
U_mag_new = []
B_mag_new = []
M2_mag_new = []
W2_mag_new = []
W1_mag_new = []
V_mag_new = []

U_err_new = []
B_err_new = []
M2_err_new = []
W2_err_new = []
W1_err_new = []
V_err_new = []

for a in range(len(U_MJD)):
    mean_index = []
    flag = [0,0,0,0,0]
    mean_index.append(a)
    while flag[0] != 1:
        for b in range(len(B_MJD)):
            if B_MJD[b] > U_MJD[a] - 0.1 and B_MJD[b] < U_MJD[a] + 0.1:
                mean_index.append(b)
                flag[0] = 1
                break
            elif b == len(B_MJD) - 1:
                flag[0] = 1
            else:
                flag[0] = 0
    while flag[1] != 1:                   
        for c in range(len(M2_MJD)):
            if M2_MJD[c] > U_MJD[a] - 0.1 and M2_MJD[c] < U_MJD[a] + 0.1:
                mean_index.append(c)
                flag[1] = 1
                break
            elif c == len(M2_MJD) - 1:
                flag[1] = 1
            else:
                flag[1] = 0
    while flag[2] != 1:
        for d in range(len(W2_MJD)):
            if W2_MJD[d] > U_MJD[a] - 0.1 and W2_MJD[d] < U_MJD[a] + 0.1:
                mean_index.append(d)
                flag[2] = 1
                break
            elif d == len(W2_MJD) - 1:
                flag[2] = 1
            else:
                flag[2] = 0
    while flag[3] != 1:
        for e in range(len(W1_MJD)):
            if W1_MJD[e] > U_MJD[a] - 0.1 and W1_MJD[e] < U_MJD[a] + 0.1:
                mean_index.append(e)
                flag[3] = 1
                break
            elif e == len(W1_MJD) - 1:
                flag[3] = 1
            else:
                flag[3] = 0
    while flag[4] != 1:
        for f in range(len(V_MJD)):
            if V_MJD[f] > U_MJD[a] - 0.1 and V_MJD[f] < U_MJD[a] + 0.1:
                mean_index.append(f)
                flag[4] = 1
                break
            elif f == len(V_MJD) - 1:
                flag[4] = 1
            else:
                flag[4] = 0

    if len(mean_index) == 6:
        x = U_MJD[mean_index[0]] + B_MJD[mean_index[1]] + M2_MJD[mean_index[2]] + W2_MJD[mean_index[3]] + W1_MJD[mean_index[4]] + V_MJD[mean_index[5]]
        y = x/6
        MJD_list.append(y)
        U_mag_new.append(U_mag[mean_index[0]])
        U_err_new.append(U_err[mean_index[0]])
        B_mag_new.append(B_mag[mean_index[1]])
        B_err_new.append(B_err[mean_index[1]])
        M2_mag_new.append(M2_mag[mean_index[2]])
        M2_err_new.append(M2_err[mean_index[2]])
        W2_mag_new.append(W2_mag[mean_index[3]])
        W2_err_new.append(W2_err[mean_index[3]])
        W1_mag_new.append(W1_mag[mean_index[4]])
        W1_err_new.append(W1_err[mean_index[4]])
        V_mag_new.append(V_mag[mean_index[5]])
        V_err_new.append(V_err[mean_index[5]])
    else:
        pass

zeropoints = [17.38, 16.85, 17.44, 18.34, 19.11, 17.89]
letters = ['W2','M2','W1','U','B','V']
U_counts = []
B_counts = []
W2_counts = []
W1_counts = []
M2_counts = []
V_counts = []

U_mag_new = np.asarray(U_mag_new)
B_mag_new = np.asarray(B_mag_new)
W1_mag_new = np.asarray(W1_mag_new)
W2_mag_new = np.asarray(W2_mag_new)
M2_mag_new = np.asarray(M2_mag_new)
V_mag_new = np.asarray(V_mag_new)

U_mag_zp = U_mag_new - 18.34
B_mag_zp = B_mag_new - 19.11
W2_mag_zp = W2_mag_new - 17.38
W1_mag_zp = W1_mag_new - 17.44
M2_mag_zp = M2_mag_new - 16.85
V_mag_zp = V_mag_new - 17.89

U_counts=(10**(-U_mag_zp/2.5))
B_counts=(10**(-B_mag_zp/2.5))
W2_counts=(10**(-W2_mag_zp/2.5))
W1_counts=(10**(-W1_mag_zp/2.5))
M2_counts=(10**(-M2_mag_zp/2.5))
V_counts=(10**(-V_mag_zp/2.5))


####Skipping errors for now but am going straight to working on the SEDs


factor = [5.77E-16, 7.47E-16, 4.06E-16, 1.53E-16, 1.31E-16, 2.61E-16]
factor = np.asarray(factor, dtype=float)

new_WL = [1928,2246,2600,3465,4392,5468]
flux_top=[]
new_counts=[12341,12341234,123412341,1234134,12341234,1234132]
flag = [0,0,0,0,0,0]

### Filter Wave!!!!!1

h = 6.6260755e-27
c = 2.99792458e18
hc = h*c

files = ['UVW2_2010.txt','UVM2_2010.txt','UVW1_2010.txt','U_UVOT.txt','B_UVOT.txt',
         'V_UVOT.txt']

filter_WL = []
filter_A = []

for item in files:

    f = open(item,'r')

    filter_lambda = []
    filter_area = []
    for line in f:
        line = line.rstrip()
        column = line.split()
        wavelen = column[0]
        area = column[1]
        filter_lambda.append(float(wavelen))
        filter_area.append(float(area))

    filter_lambda = np.asarray(filter_lambda,dtype=float)
    filter_area = np.asarray(filter_area,dtype=float)
    
    nonzero = np.where(filter_area > 0.0)
    
    filter_lambda = filter_lambda[nonzero]
    filter_area = filter_area[nonzero]

    filter_WL.append(filter_lambda)
    filter_A.append(filter_area)

    f.close()

##########################################


filtercurves = ['UVW2_2010','UVM2_2010','UVW1_2010','U_UVOT','B_UVOT','V_UVOT'] ### STRING LIST

zeropoints = [17.38, 16.85, 17.44, 18.34, 19.11, 17.89] ### PHOTOMETRIC ZEROPOINTS BASED ON VEGA


filtereffwavelength=[2030,2231,2634,3501,4329,5402] ### EFFECTIVE WAVELENGTH FOR EACH FILTER (IN SAME ORDER)

mag_array = np.zeros(len(filtercurves))

counts_array = np.zeros(len(filtercurves))


filter_array = np.array([filter_A[0],filter_A[1],filter_A[2],filter_A[3],filter_A[4],filter_A[5]])

filter_wave = np.array([filter_WL[0],filter_WL[1],filter_WL[2],filter_WL[3],filter_WL[4],filter_WL[5]])



filter_wave = np.array([filter_WL[0],filter_WL[1],filter_WL[2],filter_WL[3],filter_WL[4],filter_WL[5]])

####


### Iterating over until we are within 10% of the input counts
### Will print the value for the flux for each iteration


iterations = 0
test = np.zeros(22)

for k in range(len(W2_counts)):

    counts_array = [W2_counts[k],M2_counts[k],W1_counts[k],U_counts[k],B_counts[k],V_counts[k]]
    counts_array = np.asarray(counts_array)
    flux_top=[]
    new_counts=[12341,12341234,123412341,1234134,12341234,1234132]
    flag = [0,0,0,0,0,0]
    while sum(flag) != 6: #and iterations < 6:
        flux_top=[]
        for count in range(0,len(counts_array)):

            flux_top.append(counts_array[count]*factor[count])

        for x in range(len(flux_top)):
        
            new_spec = np.interp(filter_wave[x], new_WL, flux_top)
            
            new_counts[x] = np.trapz(new_spec*filter_array[x]*filter_wave[x]/hc,filter_wave[x])
            
            factor = map(truediv, flux_top, new_counts)

            #print new_counts

            if abs(new_counts[x] - counts_array[x]) <= 0.1*counts_array[x]:
                flag[x] = 1
            else:
                flag[x] = 0
        iterations = iterations + 1
        #print flux_top

    plt.plot(new_WL, flux_top, 'ko-')



plt.show()



