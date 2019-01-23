pro mangleSNuvotCFAII, SNname, z, referenceepoch, templatespectrumfile

lum_dist=lumdist(z)
distancefactor=(1.0+z)*(lum_dist/10.0)^2.0


;;;;;;;;;; now read in photometry data

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
uvotmjd_array=dt.time_array

;;; read in CfA optical data

readcol, 'CFA_SNII_NATSYSTEM_LC.txt', cfaName, cfaBand, cfaMJD, cfaN, cfaNatMag,  cfadMag,   cfaCampaign,  cfaCamera, /silent

vlines=where(cfaName eq 'V')
blines=where(cfaName eq 'B')
rlines=where(cfaName eq "r'")
ilines=where(cfaName eq "i'")

;;;;;; read in CfA NIR data

readcol, 'CFA_SNII_NIR_LC.txt', cfairName, cfairBand, cfairMJD, cfairNatMag,  cfadMag, /silent

jlines=where(cfairName eq 'J')
hlines=where(cfairName eq 'H')
klines=where(cfairName eq "K")




beyonduvot=where(cfaMJD[vlines] gt max(uvotmjd_array))

;; for type IIP supernovae I only use those with young UVOT observations so I don't need to extrapolate to early times

bigMJDarray=[uvotmjd_array, cfaMJD[beyonduvot] ]
n_epochs=n_elements(bigMJDarray)

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/kpno_r.txt','$SNSCRIPTS/filters/johnson_i.txt', 'J', 'H', 'K']
n_filters=n_elements(filters)

filterarray=filters

bigmagarray=fltarr(n_filters,n_epochs)

;  first put in UVOT data
for n=0,n_elements(uvotmjd_array)-1 do for f=0,5 do bigmagarray[f,n]=uvotmag_array[f,n]


;;; interpolate R,I data to UVOT epochs

f=6
for n=0,n_elements(uvotmjd_array)-1 do bigmagarray[f,n]=interpol(cfaNatMag[rlines], cfaMJD[rlines], bigMJDarray[n])
f=7
for n=0,n_elements(uvotmjd_array)-1 do bigmagarray[f,n]=interpol(cfaNatMag[ilines], cfaMJD[ilines], bigMJDarray[n])
f=8
for n=0,n_elements(uvotmjd_array)-1 do bigmagarray[f,n]=interpol(cfairNatMag[jlines], cfairMJD[jlines], bigMJDarray[n])
f=9
for n=0,n_elements(uvotmjd_array)-1 do bigmagarray[f,n]=interpol(cfairNatMag[hlines], cfairMJD[hlines], bigMJDarray[n])
f=10
for n=0,n_elements(uvotmjd_array)-1 do bigmagarray[f,n]=interpol(cfairNatMag[klines], cfairMJD[klines], bigMJDarray[n])
;;;;;;;;;;;;;;;;;;;bigMJDarray ?
interpolate colors?

;;; add BVRI beyond UVOT
f=4
for n=0,n_elements(beyonduvot)-1 do bigmagarray[f,n_elements(uvotmjd_array)+n]=B_k[beyonduvot[n]]
f=5
for n=0,n_elements(beyonduvot)-1 do bigmagarray[f,n_elements(uvotmjd_array)+n]=V_k[beyonduvot[n]]

f=6
for n=0,n_elements(beyonduvot)-1 do bigmagarray[f,n_elements(uvotmjd_array)+n]=R_k[beyonduvot[n]]
f=7
for n=0,n_elements(beyonduvot)-1 do bigmagarray[f,n_elements(uvotmjd_array)+n]=I_k[beyonduvot[n]]

;;; find the latest one with a x-v color
w2v=where( finite(uvotmag_array[0,*]) eq 1 and finite(uvotmag_array[5,*]) eq 1  )
m2v=where( finite(uvotmag_array[1,*]) eq 1 and finite(uvotmag_array[5,*]) eq 1  )
w1v=where( finite(uvotmag_array[2,*]) eq 1 and finite(uvotmag_array[5,*]) eq 1  )
uuv=where( finite(uvotmag_array[3,*]) eq 1 and finite(uvotmag_array[5,*]) eq 1  )

colorarray=fltarr(4)
colorarray[0]= uvotmag_array[0, w2v[n_elements(w2v)-1]]-uvotmag_array[5, w2v[n_elements(w2v)-1]]
colorarray[1]= uvotmag_array[1, m2v[n_elements(m2v)-1]]-uvotmag_array[5, m2v[n_elements(m2v)-1]]
colorarray[2]= uvotmag_array[2, w1v[n_elements(w1v)-1]]-uvotmag_array[5, w1v[n_elements(w1v)-1]]
colorarray[3]= uvotmag_array[3, uuv[n_elements(uuv)-1]]-uvotmag_array[5, uuv[n_elements(uuv)-1]]

;; fillin uvot mags assuming a constant color

for n=0, n_elements(beyonduvot)-1 do for f=0,3 do bigmagarray[f,n_elements(uvotmjd_array)+n]=colorarray[f]+bigmagarray[5,n_elements(uvotmjd_array)+n]



for f=0,7 do bigmagarray[f,where( finite(bigmagarray[f,*]) eq 0)]=interpol(bigmagarray[f,where( finite(bigmagarray[f,*]) eq 1)],bigmjdarray[where( finite(bigmagarray[f,*]) eq 1)], bigmjdarray[where( finite(bigmagarray[f,*]) eq 0)])



plot, MJD_k, V_k, psym=3, yrange=[22,15]

for f=0,7 do oplot, bigmjdarray, bigmagarray[f,*]
for f=0,5 do oplot, uvotmjd_array, uvotmag_array[f,*], psym=4


n_filters=n_elements(filters)

filterarray=filters

plot, bigmjdarray, bigmagarray[5,*], psym=3, yrange=[22,15]



for f=0,5 do oplot, bigmjdarray, bigmagarray[f,*]



nepochs=n_elements(bigmjdarray)


; open data file for writing
openw,lun2, 'ANT-'+SNname+'.sed.restframe.dat', /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UVOT photometry is fit by a mangled template of SN2016ccj '
printf, lun2, '# using HST and NOT spectra and a blackbody extension. '

sniimodelepochs=[1.5, 2.5, 7.5, 9.5, 10.7, 11.6, 14.5, 15.5, 20.6, 21.7, 22.5, 23.6, 24.5, 27.6, 32.6, 41.6, 56.6, 72.5]

sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n7_j12b_v4_s1_l3_v1_B.fl', 'n7_j12b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl', 'n16_n10_s0_v1_B_new5.fl', 'n16_n10_s0_v1_B_new5.fl', 'n16_n10_s0_v1_B_new4.fl', 'n16_n10_s0_v1_B_new4.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']


for n=0,nepochs-1 do begin

	;;;;;;;;; pick the spectroscopic template

	closest=where(abs(epoch-sniimodelepochs) eq min(abs(epoch-sniimodelepochs)) )

	templatespectrumfile=sniimodelspecs[closest]
	readcol, templatespectrumfile, sp_wave,sp_flux,/silent
	templatespectrum=[transpose(sp_wave),transpose(sp_flux)]


;;; put it in the observer frame
templatespectrum[0,*]=templatespectrum[0,*]*(1.0+z)
mangledspectra_array=fltarr(n_elements(templatespectrum[1,*]),nepochs)


;;;;;;;

phase=bigmjdarray[n]-referenceepoch
print, bigmagarray[*,n]
print, filterarray
plot, templatespectrum[0,*], templatespectrum[1,*]

	mangletemplate, bigmagarray[*,n], filterarray, templatespectrum, mangledspectrum
plot, mangledspectrum[0,*], mangledspectrum[1,*]
	mangledspectra_array[*,n]=mangledspectrum[1,*]
	for t=0,n_elements(mangledspectrum[0,*])-1 do printf, lun2, phase/(1.0+z), mangledspectrum[0,t]/(1.0+z),  distancefactor*mangledspectrum[1,t]


endfor


; close spectrum file
close, lun2
free_lun, lun2

save, filename=SNname+'_bolospec.sav', mangledspectra_array, bigmjdarray, bigmagarray, templatespectrum

print, 'final stop'
stop
end
