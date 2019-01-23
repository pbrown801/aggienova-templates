
;;;;;;;;
pro warpsed, spectrum, warpedspectrum, uvotmags=uvotmags, uvotmagerrs=uvotmagerrs, uvotcounts=uvotcounts, counterrs=counterrs, lambda=lambda

; 92a
; uvotcounts=[4.54193   ,   1.81368  ,17.0897, 152.233 , 322.275 , 127.479 ]

;uvotcounts=[ 12591.0   ,   8634.79   ,   51687.1   ,   367000.  ,    699111.  ,    484310.  ]  

;spectrum='sn1992A-19920124-iue-ctio.flm'
;spectrum='5000.flm'
;spectrum='vega.flm'

;spectrum='10000.flm'
;warpsed, uvotcounts=uvotcounts, spectrum, warpedspectrum

;;take input magnitudes or count rates and warp the input spectrum to match
;; the warping is done by making both into a crude sed, and fitting a polynomial to the ratios

zeropoints=[17.38,16.85,17.44,18.34,19.11,17.89]
if keyword_set(uvotmags) then uvotcounts=10.0^((zeropoints-uvotmags)/2.5)
if keyword_set(uvotmagerrs) then uvotcounterrs=uvotmagerrs*1.086*uvotcounts
IF KEYWORD_SET(counterrs) THEN errorflag=1 else counterrs=uvotcounts*0.1

if n_elements(counterrs) eq 1 then counterrs=[counterrs,counterrs,counterrs,counterrs,counterrs,counterrs]

gridsed, uvotcounts, bestsed=bestsed


uvotsed=bestsed

vegaeffwave=[2030,2230,2590,3500,4330,5400,1950,2500]

sedwave=[1600,vegaeffwave[1:4],6000,8000]

;plot, sedwave, uvotsed
;;;;;;;;;;;;;;;;;


; check to see if it is a string (ie a filename) or an array
s=size(spectrum)
if (s[1] eq 7) then begin
	readcol,spectrum,sp_wave,sp_flux,/silent
endif else begin
	sp_wave=spectrum[0,*]
	sp_flux=spectrum[1,*]
endelse


h = 1D*6.62606957E-27
c = 1D*2.99792458E18 ; in angstroms per second
hc = 1D*1.986E-8
hc = h*c
e = 1D*2.71828
k = 1D*1.38E-16

;read in filter curves
filtercurves=["$SNSCRIPTS/UVW2_2010.txt","$SNSCRIPTS/UVM2_2010.txt","$SNSCRIPTS/UVW1_2010.txt","$SNSCRIPTS/U_UVOT.txt","$SNSCRIPTS/B_UVOT.txt","$SNSCRIPTS/V_UVOT.txt"]
readcol,"$SNSCRIPTS/V_UVOT.txt",lambda,V_EA,/silent
filter_array=fltarr(n_elements(filtercurves),n_elements(lambda) )

for f=0,n_elements(filtercurves)-1 do begin
	readcol,filtercurves[f],filter_wave,filter_ea,/silent
	filter_array[f,*]=filter_ea
endfor

specflux_lambda=interpol(sp_flux, sp_wave, lambda)

;oplot, lambda, specflux_lambda*uvotsed[5]/specflux_lambda[600]


warps=make_array(n_elements(lambda),/FLOAT,VALUE=1.0) 
totalwarp=make_array(n_elements(lambda),/FLOAT,VALUE=1.0) 
speccounts=make_array(6,/FLOAT,VALUE=!values.f_nan) 
for f=0,5 do speccounts[f]=tsum(lambda,filter_array[f,*]*specflux_lambda*lambda/hc)


chisq=total(((uvotcounts-speccounts)/counterrs)^2.0)

iteration=1
while (chisq gt 1 and iteration lt 5) or iteration lt 2 do begin


;;;;; the first SED could be read in from a sav file

	gridsed, speccounts, bestsed=bestsed

	specsed=bestsed

;	oplot, sedwave, specsed
	specratio=uvotsed/specsed

	warpfunction1=spline(sedwave, specratio, lambda, 0.10)

	coeff3=poly_fit(sedwave, specratio, 3)
	warpfunction2=lambda^3*coeff3[3]+lambda^2*coeff3[2]+lambda*coeff3[1]+coeff3[0]

	warpfunction3=interpol(specratio, sedwave, lambda)
	warps=[  [warps], [warpfunction3] ]
	totalwarp=totalwarp*warpfunction3

	newspec=totalwarp*specflux_lambda


	for f=0,5 do speccounts[f]=tsum(lambda,filter_array[f,*]*newspec*lambda/hc)


	chisq=total( (   (uvotcounts-speccounts)/counterrs)^2.0)

	print, chisq

;oplot, lambda, newspec

iteration=iteration+1

endwhile

warpedspectrum=newspec

;plot, lambda, totalwarp
print, uvotcounts
print, speccounts
end
