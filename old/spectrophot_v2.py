import numpy as np
import matplotlib.pyplot as plt

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


###### VEGA for reference ######


vega_wave,vega_area = np.loadtxt('vega.dat',dtype=float,usecols=(0,1),unpack=True)




##########################################


choice = raw_input("Enter SN name: ")                   

npz = '%s.npz' % (choice) ### VARIABLE THAT TAKES YOUR CHOICE OF SUPERNOVA AND MAKES A STRING WITH .npz OF THAT SUPERNOVA.

SNname = np.load(npz) ### LOAD THE .npz FILE FROM THE DIRECTORY ITS IN.

sp_flux = SNname['fluxlist'][0] ### FLUX FROM ith SPECTRUM. CHANGE INDEX TO USE DIFFERENT SPECTRUM

sp_wave = SNname['wavelengthlist'][0] ### WAVELENGTHS FROM ith SPECTRUM. CHANGE INDEX TO USE DIFFERENT SPECTRUM


filtercurves = ['UVW2_2010','UVM2_2010','UVW1_2010','U_UVOT','B_UVOT','V_UVOT'] ### STRING LIST

zeropoints = [17.38, 16.85, 17.44, 18.34, 19.11, 17.89] ### PHOTOMETRIC ZEROPOINTS BASED ON VEGA


filtereffwavelength=[2030,2231,2634,3501,4329,5402] ### EFFECTIVE WAVELENGTH FOR EACH FILTER (IN SAME ORDER)

mag_array = np.zeros(len(filtercurves))

counts_array = np.zeros(len(filtercurves))


filter_array = np.array([filter_A[0],filter_A[1],filter_A[2],filter_A[3],filter_A[4],filter_A[5]])

filter_wave = np.array([filter_WL[0],filter_WL[1],filter_WL[2],filter_WL[3],filter_WL[4],filter_WL[5]])

    

for x in range(len(filtercurves)):    
    
    sp_ea = np.interp(sp_wave, filter_array[x], filter_wave[x]) ### spectrum effective area 
    
    counts_array[x] = np.trapz(sp_ea*sp_flux*sp_wave/hc,sp_wave) ### Integrating under the curve using numpy
    
    mag_array[x] = -2.5*np.log10(counts_array[x])+zeropoints[x]
    
    

'''
NOTE on mag_array: mag_array has 6 components, one for each filter used. This means that the first
component is the calculated w2 magnitude, the second component is the m2 calculated magnitude, all
the way to v band calculated magnitude. The order of the magnitude reflects the order of filtercurves.
'''

