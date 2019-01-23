pro createmagarray13by, bigmjdarray, bigmagarray, bigmagerrarray, filterarray

SNname='SN2013by'
; .run pjb_phot_array_B141
;; for testing
;SNname='SN2008in'
;z=0.005

;referenceepoch=54828.0
;; from Valenti 2456404.00 2.0

explosiondate=56403.5  ;;  Valenti et al. 
explosiondate_err=2.0  ;;  Valenti et al. 

referenceepoch=explosiondate

earlyoffset=-1.5

readcol, 'earlyIIPcurve.dat', earlyepoch, earlyvmag, earlyvmagerr,  /silent



;;;;;;;;;; now read in photometry data

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
uvotmagerr_array=dt.mag_array
uvotmjd_array=dt.time_array

earlyoffset=dt.vv[1,0]-interpol(earlyvmag, earlyepoch, dt.vv[0,0]-referenceepoch)

earlymjd_array=referenceepoch+earlyepoch[where(earlyepoch+referenceepoch lt dt.vv[0,0])]
earlyv_array=earlyoffset+earlyvmag[where(earlyepoch+referenceepoch lt dt.vv[0,0])]


;readcol, 'SN2013by_ValentiPhot.dat', date, amp1, MJD, amp2, Mag, amp3,  MagErr, amp4,  filter,amp5,   instrument, amp6,  date2, amp7, MJD2, amp8, Mag2, amp9,  MagErr2, amp10,  filter2, amp11,   instrument2, slash, $
; format='(A, A, F, A, F, F, A, A, A, A, A, A, A, F, A, F, F, A, A, A, A, A)', /silent

nlines=197

JD=fltarr(nlines)
mag=fltarr(nlines)
magerr=fltarr(nlines)
filter=strarr(nlines)

JD2=fltarr(nlines)
mag2=fltarr(nlines)
magerr2=fltarr(nlines)
filter2=strarr(nlines)


openr, lun, 'SN2013by_ValentiPhot.dat', /get_lun
header = STRARR(2)
   READF, lun, header
p= ' '
for i=0, 196 do begin
	READF, lun, p
	split=strsplit(p, " ", /extract)

	JD[i]=split[2]
	mag[i]=split[4]
	magerr[i]=split[5]
	filter[i]=split[7]

	JD2[i]=split[13]
	mag2[i]=split[15]
	magerr2[i]=split[16]
	filter2[i]=split[18]

endfor
;stop
mjdall=[jd,jd2]-2400000.0
magall=[mag,mag2]
magerrall=[magerr,magerr2]
filterall=[filter,filter2]

vlines=where(filterall eq '$V$')
blines=where(filterall eq '$B$')
rlines=where(filterall eq '$r$')
ilines=where(filterall eq '$i$')

;;; v band index
vbandindex=5

beyonduvot=where(MJDall[vlines] gt max(uvotmjd_array))

;; make late array
;;; Quimby et al. decay rate
;;; 0.0098 mag day-1 decline expected from the decay of 56Co into 56Fe 

; extend by 400 days so that light curve drops by  4 magnitudes 
latemjdarray=fltarr(40)
for f=0,39 do latemjdarray[f]=f*10.0+max(mjdall[vlines])
latevmagarray=fltarr(40)
for f=0,39 do latevmagarray[f]=f*10.0*0.0098+magall[vlines[where(mjdall[vlines] eq max(mjdall[vlines]))]]

;stop
;bigMJDarray=[uvotmjd_array, mjdall[vlines[beyonduvot]] ]
n_epochs=n_elements(bigMJDarray)

bigMJDarray=[earlymjd_array, uvotmjd_array, mjdall[vlines[beyonduvot]], latemjdarray ]
n_epochs=n_elements(bigMJDarray)


filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']
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

f=5   ;for v





;;;
earlyv_array=earlyoffset+earlyvmag[where(earlyepoch+referenceepoch lt dt.vv[0,0])]
earlyverr_array=earlyvmagerr[where(earlyepoch+referenceepoch lt dt.vv[0,0])]

for n=0, n_elements(earlyv_array)-1  do bigmagarray[f,n]=earlyv_array[n]
for n=0, n_elements(beyonduvot)-1    do bigmagarray[f,n_elements(earlymjd_array)+n_elements(uvotmjd_array)+n]=magall[vlines[beyonduvot[n]]]
for n=0, n_elements(latevmagarray)-1 do bigmagarray[f,n_elements(earlymjd_array)+n_elements(uvotmjd_array)+n_elements(beyonduvot)+n]=latevmagarray[n]


for n=0, n_elements(earlyv_array)-1  do bigmagerrarray[f,n]=earlyverr_array[n]
for n=0, n_elements(beyonduvot)-1    do bigmagerrarray[f,n_elements(earlymjd_array)+n_elements(uvotmjd_array)+n]=magerrall[vlines[beyonduvot[n]]]
for n=0, n_elements(latevmagarray)-1 do bigmagerrarray[f,n_elements(earlymjd_array)+n_elements(uvotmjd_array)+n_elements(beyonduvot)+n]=0.2

;;;

f=4
min=min(mjdall[blines])
max=max(mjdall[blines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(magall[blines[sort(mjdall[blines])]], mjdall[blines[sort(mjdall[blines])]], bigMJDarray[within[n]])
for n=0,n_elements(within)-1 do bigmagerrarray[f,within[n]]=interpol(magerrall[blines[sort(mjdall[blines])]], mjdall[blines[sort(mjdall[blines])]], bigMJDarray[within[n]])

;;; interpolate R,I to UVOT and V epochs


;f=5
;flines=vlines
;min=min(mjdall[flines])
;max=max(mjdall[flines])
;within=where(bigMJDarray lt max and bigMJDarray gt min)
;for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(magall[flines], mjdall[flines], bigMJDarray[within[n]])

f=6
min=min(mjdall[rlines])
max=max(mjdall[rlines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(magall[rlines[sort(mjdall[rlines])]], mjdall[rlines[sort(mjdall[rlines])]], bigMJDarray[within[n]])
for n=0,n_elements(within)-1 do bigmagerrarray[f,within[n]]=interpol(magerrall[rlines[sort(mjdall[rlines])]], mjdall[rlines[sort(mjdall[rlines])]], bigMJDarray[within[n]])

f=7
flines=ilines
min=min(mjdall[flines])
max=max(mjdall[flines])
within=where(bigMJDarray lt max and bigMJDarray gt min)
for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(magall[flines[sort(mjdall[flines])]], mjdall[flines[sort(mjdall[flines])]], bigMJDarray[within[n]])
for n=0,n_elements(within)-1 do bigmagerrarray[f,within[n]]=interpol(magerrall[flines], mjdall[flines], bigMJDarray[within[n]])


for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]



;;;;;;; now loop through all filters to fill in missing blanks in the interior region
for f=0,n_filters-1 do begin

;print, 'filling in interior region for ', f
;stop
	present=where(finite(bigmagarray[f,*]) eq 1,presentcount)
	min=min(bigmjdarray[present])
	max=max(bigmjdarray[present])
	notpresentwithin=where(bigMJDarray lt max and bigMJDarray gt min and finite(bigmagarray[f,*]) eq 0, notpresentcount)
	if notpresentcount ne 0 then for n=0,n_elements(notpresentwithin)-1 do bigmagarray[f,notpresentwithin[n]]=interpol(bigmagarray[f,present], bigmjdarray[present], bigMJDarray[notpresentwithin[n]])


endfor

;print, 'after loop'
;stop

;;; extrapolate or interpolate missing values based on the color

for f=0, n_filters-1 do begin

	color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )
	earlymissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 and bigmjdarray lt bigmjdarray[color[0]], earlymissingcount )
	latemissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0  and bigmjdarray gt bigmjdarray[color[0]], latemissingcount )

	;if missingcount ne 0 then bigmagarray[f,missing] = interpol( bigmagarray[f,color]-bigmagarray[vbandindex,color], bigmjdarray[color], bigmjdarray[missing] )+bigmagarray[vbandindex,missing]

	;;; this extrapolates based on the last color

	if latemissingcount ne 0 then bigmagarray[f,latemissing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[vbandindex, color[colorcount-1]]+ bigmagarray[vbandindex,latemissing]

;;; this extrapolates to early times based on the first color

	if earlymissingcount ne 0 then bigmagarray[f,earlymissing] = bigmagarray[f,color[0]]-bigmagarray[vbandindex,color[0]]+ bigmagarray[vbandindex,earlymissing]



	for n=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[n,*]
print, 'in loop with filter ', f
;stop
endfor


plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, yrange=[30,14]

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]
for f=0,5 do oplot, uvotmjd_array, uvotmag_array[f,*], psym=4

oplot, bigmjdarray, bigmagarray[vbandindex,*], thick=3

;oplot, bigmjdarray, bigmagarray[f,*], thick=3



;print, 'final stop'
;stop
end
