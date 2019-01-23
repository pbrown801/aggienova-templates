pro createmagarrayuvotcfairii, SNname, bigmjdarray, bigmagarray, filterarray

; .run pjb_phot_array_B141
;; for testing
;SNname='SN2008in'
;z=0.005

;referenceepoch=54828.0

;;;;;;;;;; now read in photometry data

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
uvotmjd_array=dt.time_array

;;; read in CfA optical data

readcol, 'CFA_SNII_NATSYSTEM_LC.txt', cfaName, cfaBand, cfaMJD, cfaN, cfaNatMag,  cfadMag,   cfaCampaign,  cfaCamera, format='(A, A, F, I, F, F, A, A)', /silent

vlines=where(cfaName eq SNname and cfaband eq 'V')
blines=where(cfaName eq SNname and cfaband eq 'B')
rlines=where(cfaName eq SNname and cfaband eq "r'")
ilines=where(cfaName eq SNname and cfaband eq "i'")

;;;;;; read in CfA NIR data

readcol, 'CFA_SNII_NIR_LC.txt', cfairName, cfairBand, cfairMJD, cfairNatMag,  cfadMag, format='(A, A, F, F, F)', /silent

jlines=where(cfairName eq SNname and cfairband eq 'J')
hlines=where(cfairName eq SNname and cfairband eq 'H')
klines=where(cfairName eq SNname and cfairband eq "K")


;;; v band index
vbandindex=5


beyonduvot=where(cfaMJD[vlines] gt max(uvotmjd_array))

;; for type IIP supernovae I only use those with young UVOT observations so I don't need to extrapolate to early times

bigMJDarray=[uvotmjd_array, cfaMJD[vlines[beyonduvot]] ]
n_epochs=n_elements(bigMJDarray)

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt', '$SNSCRIPTS/filters/J_2mass.txt', '$SNSCRIPTS/filters/H_2mass.txt', '$SNSCRIPTS/filters/Ks_2mass.txt']
n_filters=n_elements(filters)

filterarray=filters

bigmagarray=fltarr(n_filters,n_epochs)

;  first put in UVOT data
for n=0,n_elements(uvotmjd_array)-1 do for f=0,5 do bigmagarray[f,n]=uvotmag_array[f,n]

;;;;;;;;;;;;;;
plot, bigmjdarray, bigmagarray[vbandindex,*], psym=-3, thick=3, symsize=2, yrange=[30,14]

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]
for f=0,5 do oplot, uvotmjd_array, uvotmag_array[f,*], psym=4

;;;;;;;;;;;;;;;;;;;




f=5   ;for v
for n=0, n_elements(beyonduvot)-1 do bigmagarray[f,n_elements(uvotmjd_array)+n]=cfanatmag[vlines[beyonduvot[n]]]

f=4   ;for b
for n=n_elements(uvotmjd_array),n_elements(bigmjdarray)-1 do bigmagarray[f,n]=interpol(cfanatmag[blines],cfamjd[blines],bigmjdarray[n])

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]


;;; interpolate R,I,J,H,K data to UVOT and V epochs


f=5
flines=vlines
min=min(cfaMJD[flines])
max=max(cfaMJD[flines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(cfaNatMag[flines], cfaMJD[flines], bigMJDarray[within[n]])

f=6
min=min(cfaMJD[rlines])
max=max(cfaMJD[rlines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(cfaNatMag[rlines], cfaMJD[rlines], bigMJDarray[within[n]])

f=7
flines=ilines
min=min(cfaMJD[flines])
max=max(cfaMJD[flines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(cfaNatMag[flines], cfaMJD[flines], bigMJDarray[within[n]])

f=8
flines=jlines
min=min(cfairMJD[flines])
max=max(cfairMJD[flines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(cfairNatMag[flines], cfairMJD[flines], bigMJDarray[within[n]])

f=9
flines=hlines
min=min(cfairMJD[flines])
max=max(cfairMJD[flines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(cfairNatMag[flines], cfairMJD[flines], bigMJDarray[within[n]])

f=10
flines=klines
min=min(cfairMJD[flines])
max=max(cfairMJD[flines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(cfairNatMag[flines], cfairMJD[flines], bigMJDarray[within[n]])

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]

;;; extrapolate or interpolate missing values based on the color

for f=0, n_filters-1 do begin

missing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 , missingcount )
color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )

;;; this extrapolates based on the slope of the last two colors
;; if missingcount ne -1 then bigmagarray[f,missing] = interpol( bigmagarray[f,color]-bigmagarray[vbandindex,color], bigmjdarray[color], bigmjdarray[missing] )+ bigmagarray[vbandindex,missing]

;;; this extrapolates based on the last color

if missingcount ne -1 then bigmagarray[f,missing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[vbandindex,color[colorcount-1]]+ bigmagarray[vbandindex,missing]

for n=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[n,*]

endfor


plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, yrange=[30,14]

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]
for f=0,5 do oplot, uvotmjd_array, uvotmag_array[f,*], psym=4

oplot, bigmjdarray, bigmagarray[vbandindex,*], thick=3



;print, 'final stop'
;stop
end
