import numpy as np
import matplotlib.pyplot as plt
import os
import pysynphot as S
from spectrophot_array_in import *
from countsin_sedout import *

SNname = raw_input("Enter SN: ")


#####Changing directory into my created SN folder#####
new_path = '/Users/brittonbeeny/astroresearch/%s' % (SNname)

os.chdir(new_path)


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

obs_mags = [W2_mag_new,M2_mag_new,W1_mag_new,U_mag_new,B_mag_new,V_mag_new]
obs_mags_errs = [W2_err_new,M2_err_new,W1_err_new,U_err_new,B_err_new,V_err_new]


dof = 2


###Changing directories into a Filters folders to be able to do spectrophot#####
newer_path = '/Users/brittonbeeny/astroresearch'

os.chdir(newer_path)


#####Defining a temperature range in Kelvin#####
T = np.linspace(1000,30000,num=100,endpoint=True)

Good_temps = []
UV_col = []
UB_col = []
BV_col = []

for index in range(len(MJD_list)):

    obs_UV_col = obs_mags[3][index]-obs_mags[5][index]
    UV_col.append(round(obs_UV_col,2))
    
    obs_UB_col = obs_mags[3][index]-obs_mags[4][index]
    UB_col.append(round(obs_UB_col,2))
    
    obs_BV_col = obs_mags[4][index]-obs_mags[5][index]
    BV_col.append(round(obs_BV_col,2))


    obs_UV_col_err = np.sqrt((obs_mags_errs[3][index]**2+obs_mags_errs[5][index]**2))
    obs_UB_col_err = np.sqrt((obs_mags_errs[3][index]**2+obs_mags_errs[4][index]**2))
    obs_BV_col_err = np.sqrt((obs_mags_errs[4][index]**2+obs_mags_errs[5][index]**2))

    chi_sq = []
    for t in range(0,len(T)):
        bb = S.BlackBody(T[t])
        bb.convert('flam')  #Get in proper cgs units

        ###call spectrophotometry_array_in code###
        ###inputs are blackbody wavelengths and fluxes
        
        mag_array = w_f_in(bb.wave,bb.flux)

        ###deterimine calculated UV color
        exp_UV_col = mag_array[3]-mag_array[5]
        exp_UB_col = mag_array[3]-mag_array[4]
        exp_BV_col = mag_array[4]-mag_array[5]

        X_sq_val_UV = (obs_UV_col-exp_UV_col)**2/obs_UV_col_err**2
        X_sq_val_UB = (obs_UB_col-exp_UB_col)**2/obs_UB_col_err**2
        X_sq_val_BV = (obs_BV_col-exp_BV_col)**2/obs_BV_col_err**2


        SUM = sum((X_sq_val_UV,X_sq_val_UB,X_sq_val_BV))

        chi_sq.append(SUM)

    reduced_X_sq = np.divide(chi_sq,dof)    
    good_T = np.where(chi_sq == min(chi_sq))
    Good_temps.append(T[good_T[0][0]])

        

###Lets make a temperature evolution plot!!###

##plt.plot(MJD_list,Good_temps,'k--')
##plt.xlabel('MJD')
##plt.ylabel('Temperature (K)')
##plt.title('Temperature Evolution of ' + SNname)


###Color plots###

