pro create06ajbigmagarray, SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray, bigmjdarray, bigmagarray, bigmagerrarray, explosiondate, explosiondateerr

restore, filename=SNname+'_filtermags.sav'

filters=filterarray
n_filters=n_elements(filters)
referenceepoch=explosiondate


;; make late array
;;; Quimby et al. decay rate from IIP
;;; 0.0098 mag day-1 decline expected from the decay of 56Co into 56Fe 

; extend by 400 days so that light curve drops by  4 magnitudes 
latemjdarray=fltarr(40)
for f=0,39 do latemjdarray[f]= f*10.0+max(filtermjdarray[vbandindex,*])

;; late slopes from Misra et al. 2011
;; http://adsabs.harvard.edu/abs/2011AIPC.1358..299M

latebmagarray=fltarr(40)
for f=0,39 do latebmagarray[f]=f*10.0*0.0110+filtermagarray[vbandindex-1,where(filtermjdarray[vbandindex-1,*] eq max(filtermjdarray[vbandindex-1,*]))]
latevmagarray=fltarr(40)
for f=0,39 do latevmagarray[f]=f*10.0*0.0181+filtermagarray[vbandindex,where(filtermjdarray[vbandindex,*] eq max(filtermjdarray[vbandindex,*]))]
latermagarray=fltarr(40)
for f=0,39 do latermagarray[f]=f*10.0*0.0160+filtermagarray[vbandindex+1,where(filtermjdarray[vbandindex+1,*] eq max(filtermjdarray[vbandindex+1,*]))]
lateimagarray=fltarr(40)
for f=0,39 do lateimagarray[f]=f*10.0*0.0164+filtermagarray[vbandindex+2,where(filtermjdarray[vbandindex+2,*] eq max(filtermjdarray[vbandindex+2,*]))]
latevmagerrarray=fltarr(40)
for f=0,39 do latevmagerrarray[f]=0.2

;  earlymjd was included in filter mags

goodv=where(finite(filtermagarray[vbandindex,*]) eq 1)
bigMJDarray=[transpose(filtermjdarray[vbandindex,goodv]), latemjdarray ]
n_epochs=n_elements(bigMJDarray)

bigmagarray=make_array(n_filters,n_epochs,value=!Values.F_NAN)
bigmagerrarray=make_array(n_filters,n_epochs,value=!Values.F_NAN)

;  first put in V data

bigmagarray[vbandindex,*]=[transpose(filtermagarray[vbandindex,goodv]), latevmagarray]
bigmagerrarray[vbandindex,*]=[transpose(filtermagerrarray[vbandindex,goodv]), latevmagerrarray]

start=n_elements(goodv)-1
;for f=0,39 do bigmagarray[vbandindex-1,start+f]=latebmagarray[f]
;for f=0,39 do bigmagerrarray[vbandindex-1,start+f]=latevmagerrarray[f]

;for f=0,39 do bigmagarray[vbandindex+1,start+f]=latermagarray[f]
;for f=0,39 do bigmagerrarray[vbandindex+1,start+f]=latevmagerrarray[f]

;for f=0,39 do bigmagarray[vbandindex+2,start+f]=lateimagarray[f]
;for f=0,39 do bigmagerrarray[vbandindex+2,start+f]=latevmagerrarray[f]


;;;;;;;;;;;;;;
plot, bigmjdarray, bigmagarray[vbandindex,*], psym=-3, thick=3, symsize=2, yrange=[30,14]

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]

;;;

for f=0, n_filters-1 do begin

	min=min(filtermjdarray[f,*])
	max=max(filtermjdarray[f,*])
	within=where(bigMJDarray lt max and bigMJDarray gt min)
	present=where(finite(filtermagarray[f,*]) eq 1,npresent)
	for n=0,n_elements(within)-1 do bigmagarray[f,within[n]]=interpol(filtermagarray[f,present], filtermjdarray[f,present], bigMJDarray[within[n]])
	for n=0,n_elements(within)-1 do bigmagerrarray[f,within[n]]=interpol(filtermagerrarray[f,present], filtermjdarray[f,present], bigMJDarray[within[n]])

endfor

for f=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[f,*]

;; I think this part is covered

;;;;;;; now loop through all filters to fill in missing blanks in the interior region
for f=0,n_filters-1 do begin

;print, 'filling in interior region for ', f
;stop
	present=where(finite(bigmagarray[f,*]) eq 1,presentcount)
	min=min(bigmjdarray[present])
	max=max(bigmjdarray[present])
	notpresentwithin=where(bigMJDarray lt max and bigMJDarray gt min and finite(bigmagarray[f,*]) eq 0, notpresentcount)
	if notpresentcount ne 0 then for n=0,n_elements(notpresentwithin)-1 do bigmagarray[f,notpresentwithin[n]]=interpol(bigmagarray[f,present], bigmjdarray[present], bigMJDarray[notpresentwithin[n]])
	if notpresentcount ne 0 then for n=0,n_elements(notpresentwithin)-1 do bigmagerrarray[f,notpresentwithin[n]]=interpol(bigmagerrarray[f,present], bigmjdarray[present], bigMJDarray[notpresentwithin[n]])

endfor

;print, 'after loop'
;stop

;;; extrapolate or interpolate missing values based on the color
;;; starting with UV filters matched to uvw1

if w1bandindex eq 2 then begin
for f=0, 1 do begin

	color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )
	earlymissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 and bigmjdarray lt bigmjdarray[color[0]], earlymissingcount )
	latemissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0  and bigmjdarray gt bigmjdarray[color[0]], latemissingcount )

	;;; this extrapolates based on the last color

	if latemissingcount ne 0 then bigmagarray[f,latemissing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[w1bandindex, color[colorcount-1]]+ bigmagarray[w1bandindex,latemissing]
	if latemissingcount ne 0 then bigmagerrarray[f,latemissing] = 0.2

;;; this extrapolates to early times based on the first color

	if earlymissingcount ne 0 then bigmagarray[f,earlymissing] = bigmagarray[f,color[0]]-bigmagarray[w1bandindex,color[0]]+ bigmagarray[w1bandindex,earlymissing]
	if earlymissingcount ne 0 then bigmagerrarray[f,earlymissing] = 0.2

;stop
endfor
endif

;;; then matching all filters to v based on color
for f=0, n_filters-1 do begin

	color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )
	earlymissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 and bigmjdarray lt bigmjdarray[color[0]], earlymissingcount )
	latemissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0  and bigmjdarray gt bigmjdarray[color[0]], latemissingcount )

	;if missingcount ne 0 then bigmagarray[f,missing] = interpol( bigmagarray[f,color]-bigmagarray[vbandindex,color], bigmjdarray[color], bigmjdarray[missing] )+bigmagarray[vbandindex,missing]

	;;; this extrapolates based on the last color

	if latemissingcount ne 0 then bigmagarray[f,latemissing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[vbandindex, color[colorcount-1]]+ bigmagarray[vbandindex,latemissing]
	if latemissingcount ne 0 then bigmagerrarray[f,latemissing] = 0.2

;;; this extrapolates to early times based on the first color

	if earlymissingcount ne 0 then bigmagarray[f,earlymissing] = bigmagarray[f,color[0]]-bigmagarray[vbandindex,color[0]]+ bigmagarray[vbandindex,earlymissing]
	if earlymissingcount ne 0 then bigmagerrarray[f,earlymissing] = 0.2



	for n=0,n_filters-1 do oplot, bigmjdarray, bigmagarray[n,*]
print, 'in loop with filter ', f
;stop
endfor


plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, xrange=[53780,53920], yrange=[25,15], charsize=2

for f=0,n_filters-1 do cgoplot, bigmjdarray, bigmagarray[f,*], color='white'
for f=0,n_elements(filterarray)-1 do 	cgoplot, filtermjdarray[f,*], filtermagarray[f,*], psym=4, color='blue'


save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray, bigmjdarray, bigmagarray, bigmagerrarray, explosiondate, explosiondateerr, vbandindex, w1bandindex


;print, 'final stop'
stop
end
