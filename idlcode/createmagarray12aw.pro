pro createmagarray12aw, bigmjdarray, bigmagarray, filterarray
; .run pjb_phot_array_B141
SNname='SN2012aw'

explosiondate=56002.0  ;; Fraser et al. 2012
explosiondate_err=0.8  ;; Fraser et al. 2012

referenceepoch=explosiondate

earlyoffset=-1.5

readcol, 'earlyIIPcurve.dat', earlyepoch, earlyvmag, earlyvmagerr,  /silent


;;;;;;;;;; now read in photometry data

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
uvotmagerr_array=dt.magerr_array
uvotmjd_array=dt.time_array


earlyoffset=dt.vv[1,0]-interpol(earlyvmag, earlyepoch, dt.vv[0,0]-referenceepoch)

plot, uvotmjd_array-referenceepoch, uvotmag_array[5,*], psym=4, xrange=[-10,20], yrange=[18,12]

oplot, earlyepoch, earlyvmag+earlyoffset

earlymjd_array=referenceepoch+earlyepoch[where(earlyepoch+referenceepoch lt dt.vv[0,0])]
earlyv_array=earlyoffset+earlyvmag[where(earlyepoch+referenceepoch lt dt.vv[0,0])]


;;; read in Dall'ora et al. 2014  optical data
; 2013-06-24 &  2456467.661 &  20.678 0.153 & $uw2$ &  $Swift$ & 2013-05-29 &  2456441.823 &  15.112 0.049 & $B$ &  $Swift$ \\ 

readcol, 'SN2012aw_UBVRI.dat', JDshort, phase, Umag, Umagerr, Bmag, Bmagerr, Vmag, Vmagerr, Rmag, Rmagerr, Imag, Imagerr,  /silent

Umag[where(umag eq 0)]=!Values.F_NAN
Umagerr[where(umagerr eq 0)]=!Values.F_NAN
Bmag[where(bmag eq 0)]=!Values.F_NAN
Bmagerr[where(bmagerr eq 0)]=!Values.F_NAN
Vmag[where(vmag eq 0)]=!Values.F_NAN
Vmagerr[where(vmagerr eq 0)]=!Values.F_NAN
Rmag[where(rmag eq 0)]=!Values.F_NAN
Rmagerr[where(rmagerr eq 0)]=!Values.F_NAN
imag[where(imag eq 0)]=!Values.F_NAN
imagerr[where(imagerr eq 0)]=!Values.F_NAN

mjd=jdshort-0.5

beyonduvot=where(MJD  gt max(uvotmjd_array))


;; make late array
;;; Quimby et al. decay rate
;;; 0.0098 mag day-1 decline expected from the decay of 56Co into 56Fe 

; extend by 400 days so that light curve drops by  4 magnitudes 
latemjdarray=fltarr(40)
for f=0,39 do latemjdarray[f]=f*10.0+max(mjd)
latevmagarray=fltarr(80)
for f=0,39 do latevmagarray[f]=f*10.0*0.0098+vmag[where(mjd eq max(mjd))]




readcol, 'SN2012aw_JHK.dat', irJDshort, irphase, Jmag, Jmagerr, Hmag, Hmagerr, Kmag, Kmagerr,  /silent

irmjd=irjdshort-0.5

jmag[where(jmag eq 0)]=!Values.F_NAN
jmagerr[where(jmagerr eq 0)]=!Values.F_NAN
hmag[where(hmag eq 0)]=!Values.F_NAN
hmagerr[where(hmagerr eq 0)]=!Values.F_NAN
kmag[where(kmag eq 0)]=!Values.F_NAN
kmagerr[where(kmagerr eq 0)]=!Values.F_NAN

;; for type IIP supernovae I only use those with young UVOT observations so I don't need to extrapolate to early times

bigMJDarray=[earlymjd_array, uvotmjd_array, mjd[beyonduvot],latemjdarray ]
n_epochs=n_elements(bigMJDarray)

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt', '$SNSCRIPTS/filters/J_2mass.txt', '$SNSCRIPTS/filters/H_2mass.txt', '$SNSCRIPTS/filters/Ks_2mass.txt']
n_filters=n_elements(filters)

filterarray=filters
vbandindex=5
bigmagarray=make_array(n_filters,n_epochs,value=!Values.F_NAN)
bigmagerrarray=make_array(n_filters,n_epochs,value=!Values.F_NAN)

;  first put in UVOT data
for n=0,n_elements(uvotmjd_array)-1 do for f=0,5 do bigmagarray[f,n_elements(earlymjd_array)+n]=uvotmag_array[f,n]
for n=0,n_elements(uvotmjd_array)-1 do for f=0,5 do bigmagerrarray[f,n_elements(earlymjd_array)+n]=uvotmagerr_array[f,n]

;;;;;;;;;;;;;;
plot, bigmjdarray, bigmagarray[vbandindex,*], psym=-3, thick=3, symsize=2, yrange=[30,14]

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]
for f=0,5 do oplot, uvotmjd_array, uvotmag_array[f,*], psym=4

;;;;;;;;;;;;;;;;;;;


;;; add b and v data

f=5   ;for v

earlyv_array=earlyoffset+earlyvmag[where(earlyepoch+referenceepoch lt dt.vv[0,0])]

for n=0, n_elements(earlyv_array)-1 do bigmagarray[f,n]=earlyv_array[n]
for n=0, n_elements(beyonduvot)-1 do bigmagarray[f,n_elements(earlymjd_array)+n_elements(uvotmjd_array)+n]=vmag[beyonduvot[n]]
for n=0, n_elements(latevmagarray)-1 do bigmagarray[f,n_elements(earlymjd_array)+n_elements(uvotmjd_array)+n_elements(beyonduvot)+n]=latevmagarray[n]

f=4   ;for b
for n=n_elements(uvotmjd_array),n_elements(bigmjdarray)-1 do bigmagarray[f,n]=interpol(bmag,mjd,bigmjdarray[n])


for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]


;;; interpolate R,I to UVOT and V epochs


;f=5
;flines=vlines
;min=min(mjdall[flines])
;max=max(mjdall[flines])
;within=where(bigMJDarray lt max and bigMJDarray gt min)
;for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(magall[flines], mjdall[flines], bigMJDarray[within[n]])

f=6
min=min(mjd)
max=max(mjd)
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(rmag, mjd, bigMJDarray[within[n]])

f=7
min=min(mjd)
max=max(mjd)
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(imag, mjd, bigMJDarray[within[n]])

f=8
min=min(irmjd)
max=max(irmjd)
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(jmag, irmjd, bigMJDarray[within[n]])

f=9
min=min(irmjd)
max=max(irmjd)
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(hmag, irmjd, bigMJDarray[within[n]])

f=10
min=min(irmjd)
max=max(irmjd)
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(kmag, irmjd, bigMJDarray[within[n]])


;;;;;;; now loop through all filters to fill in missing blanks in the interior region
for f=0,n_filters-1 do begin
	present=where(finite(bigmagarray[f,*]) eq 1)
	min=min(bigmjdarray[present])
	max=max(bigmjdarray[present])
	notpresentwithin=where(bigMJDarray lt max and bigMJDarray gt min and finite(bigmagarray[f,*]) eq 0)
	for n=0,n_elements(notpresentwithin)-1 do bigmagarray[f,notpresentwithin[n]]=interpol(bigmagarray[f,present], bigmjdarray[present], bigMJDarray[notpresentwithin[n]])


endfor


for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]

;;; extrapolate or interpolate missing values based on the color

for f=0, n_filters-1 do begin

color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )
earlymissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 and bigmjdarray lt bigmjdarray[color[0]], earlymissingcount )
latemissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0  and bigmjdarray gt bigmjdarray[color[0]], latemissingcount )

;if missingcount ne -1 then bigmagarray[f,missing] = interpol( bigmagarray[f,color]-bigmagarray[vbandindex,color], bigmjdarray[color], bigmjdarray[missing] )+bigmagarray[vbandindex,missing]

;;; this extrapolates based on the last color

if latemissingcount ne -1 then bigmagarray[f,latemissing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[vbandindex,color[colorcount-1]]+ bigmagarray[vbandindex,latemissing]

;;; this extrapolates to early times based on the first color

if earlymissingcount ne -1 then bigmagarray[f,earlymissing] = bigmagarray[f,color[0]]-bigmagarray[vbandindex,color[0]]+ bigmagarray[vbandindex,earlymissing]



for n=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[n,*]

endfor

;stop
plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, yrange=[24,10], xrange=[referenceepoch,referenceepoch+50]

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]
for f=0,5 do oplot, uvotmjd_array, uvotmag_array[f,*], psym=4

oplot, bigmjdarray, bigmagarray[vbandindex,*], thick=3


print, 'final stop'
stop
end
