import numpy as np
import matplotlib.pyplot as plt
import os
import pysynphot as S
import math

Gaia16apd_redshift=0.1018

#  read in data
wave_fuv, flux_fuv, fluxerr_fuv, dq_fuv = np.loadtxt('spectra/Gaia16apd_fuv_20160602_col.dat',comments='#', usecols = (0,1,2,3), unpack = True)
wave_muv, flux_muv, fluxerr_muv, dq_muv = np.loadtxt('spectra/Gaia16apd_muv_20160602_col.dat',comments='#', usecols = (0,1,2,3), unpack = True)
wave_opt, flux_opt                      = np.loadtxt('spectra/gaia16apd-20160604-fast.dat',   comments='#', usecols = (0,1), unpack = True)

#trim data
'''
https://stackoverflow.com/questions/16343752/numpy-where-function-multiple-conditions
You don't actually need where if you're just trying to filter out the elements of dists that don't fit your criteria:

dists[(dists >= r) & (dists <= r+dr)]
Because the & will give you an elementwise and (the parentheses are necessary).

Or, if you do want to use where for some reason, you can do:

 dists[(np.where((dists >= r) & (dists <= r + dr)))]


'''

#goodindexes=where(dq_fuv==0 and wave_fuv GT 900)
print(wave_fuv[0:10])
print(len(wave_fuv))
flux_fuv=flux_fuv[(wave_fuv <= 1650.0) & (wave_fuv >= 1030.0) & (dq_fuv==0 )]
fluxerr_fuv=fluxerr_fuv[(wave_fuv <= 1650.0) & (wave_fuv >= 1030.0) & (dq_fuv==0 )]
dq_fuv_full=dq_fuv
dq_fuv=dq_fuv[(wave_fuv <= 1650.0) & (wave_fuv >= 1030.0) & (dq_fuv==0 )]
wave_fuv=wave_fuv[(wave_fuv <= 1650.0) & (wave_fuv >= 1030.0) & (dq_fuv_full==0 )]

#  this takes out the lyman alpha geocoronal lines
flux_fuv[(wave_fuv <= 1225.0) & (wave_fuv >= 1205.0)]=np.mean(flux_fuv[(wave_fuv <= 1205.0) & (wave_fuv >= 1200.0)])
flux_fuv[(wave_fuv >= 1290.0) & (wave_fuv <= 1310.0)]=np.mean(flux_fuv[(wave_fuv >= 1290.0) & (wave_fuv <= 1295.0)])


flux_muv   =flux_muv[(wave_muv >= 1650.0) & (wave_muv <= 4030.0) & (dq_muv==0 )]
fluxerr_muv=fluxerr_muv[(wave_muv >= 1650.0) & (wave_muv <= 4030.0) & (dq_muv==0 )]
dq_muv_full=dq_muv
dq_muv     =dq_muv[(wave_muv >= 1650.0) & (wave_muv <= 4030.0) & (dq_muv==0 )]
wave_muv   =wave_muv[(wave_muv >= 1650.0) & (wave_muv <= 4030.0) & (dq_muv_full==0 )]


fig =plt.figure()
ax = fig.add_subplot(111)
#plt.plot(wave_fuv, flux_fuv, '-',color='purple')
#plt.plot(wave_muv, flux_muv, '-',color='blue')
#plt.plot(wave_opt, flux_opt, '-',color='red')
#ax.axis([900, 4000,0, 0.5E-14])

#plt.show()

Temp=17000
bb = S.BlackBody(Temp)
bb.convert('flam')  #Get in proper cgs units

#print(bb.wave[0:10])

#calculate scaling factor between blackbody and spectrum at 6000 Angstroms
factor=np.mean(flux_opt[(wave_opt/(1.0+Gaia16apd_redshift) >= 5995) &  (wave_opt/(1.0+Gaia16apd_redshift) <= 6005)]) / np.mean(bb.flux[(bb.wave >= 5995) & (bb.wave <= 6005)])
bigrest_wave=[]
bigrest_flux=[]

bigrest_wave.extend(wave_fuv/(1.0+Gaia16apd_redshift))
bigrest_wave.extend(wave_muv/(1.0+Gaia16apd_redshift))

bigrest_flux.extend(flux_fuv)
bigrest_flux.extend(flux_muv)


list1=range(200)
template_flux=range(200)

template_wave=[x*10.0+1000.0 for x in list1]
for l in list1:

        dummyindex = (np.abs( np.array(bigrest_wave)-template_wave[l]) < 5).nonzero()
        
        #print(dummyindex)
        dummyindex,=np.array(dummyindex)
        #print(dummyindex)
        fluxinbin=[]
        #print(len(dummyindex))
        for i in range(len(dummyindex)):
            #print(dummyindex[i])
            #print(bigmjdlist[dummyindex[i]])
            #print(magsinbin)
            fluxinbin.append(bigrest_flux[dummyindex[i]])

        template_flux[l] = np.mean(fluxinbin)

#print(bigrest_wave[0:10])
bigobs_wave=[x*(1.0+Gaia16apd_redshift) for x in bigrest_wave]

snfluxbbrange=range(len(bb.wave))

for f in range(len(bb.wave)):
        dummyindex = (np.abs(np.array(bigrest_wave)-bb.wave[f]) < 5).nonzero()
        dummyindex,=np.array(dummyindex)
        fluxinbin=[]
        for r in range(len(dummyindex)):
           fluxinbin.append(bigrest_flux[dummyindex[r]])
        snfluxbbrange[f] = np.mean(fluxinbin)
        
#plt.plot(bb.wave*(1.0+Gaia16apd_redshift),bb.flux*factor, '-',color='blue')
#plt.plot(bigobs_wave,bigrest_flux, '-',color='blue')
#plt.plot(template_wave,template_flux, '-', color='black')


#plt.plot(bb.wave,snfluxbbrange, '-', color='red')

#plt.show()


bbfluxscaled=np.multiply(bb.flux,factor)
#print(snfluxbbrange)
snfluxbbrange=np.array(snfluxbbrange)
snfluxbbrange[np.isnan(snfluxbbrange)]=bbfluxscaled[np.isnan(snfluxbbrange)]

absorptionspectrum=(snfluxbbrange)/bbfluxscaled
absorptionspectrum[bb.wave <=1000]=0
absorptionspectrum[bb.wave >=3000]=1
#print(absorptionspectrum[0:300])
fig=plt.figure
#plt.plot(bb.wave, bbfluxscaled, '-', color='blue')
#plt.plot(bb.wave, snfluxbbrange, '-', color='red')

plt.plot(bb.wave, absorptionspectrum, '-')
ax.axis([900,4000,0,1])

plt.show()

printabsorption=open('gaia16apd_absorption.dat','write')
for t in range(len(bb.wave)):
        linetoprint=str(bb.wave[t])+ ' '+str(absorptionspectrum[t])
        
        printabsorption.writelines(linetoprint)
        printabsorption.write('\n')
printabsorption.close()

printspectrum=open('gaia16apd_templatespectrum.dat','write')
for t in range(len(bigrest_wave)):
        linetoprint=str(bigrest_wave[t])+ ' '+str(bigrest_flux[t])
        
        printspectrum.writelines(linetoprint)
        printspectrum.write('\n')
printspectrum.close()



