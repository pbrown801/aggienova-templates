pro makeweightedsedfromphot, mags, magerrs, filters, sed

;stop
if n_elements(mags) ne n_elements(filters) then print, ' Each magnitude needs a filter path and vice versa. '
if n_elements(mags) ne n_elements(filters) then stop

;filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/kpno_r.txt','$SNSCRIPTS/filters/johnson_i.txt']
n_filters=n_elements(filters)

;testspectrum='$SNSCRIPTS/SN2011fe_boloP000072.dat'
;testmag_array=fltarr(n_filters)
;for n=0, n_filters-1 do testmag_array[n]=vegaphot(testspectrum, filters[n])
;mags=testmag_array
;magerrs=mags*0.0+0.1

vegazeropoint_array=make_array(n_filters, value=!Values.F_NAN)
counts_array=make_array(n_filters, value=!Values.F_NAN)

for f=0, n_filters-1 do begin
	vegazeropointout=vegazeropoint(filters[f])
	vegazeropoint_array[f]=vegazeropointout
endfor


obs_counts_array=10.0^((vegazeropoint_array-mags)/2.5)

filterwavelow_array=make_array(n_filters, value=!Values.F_NAN)
filterwavehigh_array=make_array(n_filters, value=!Values.F_NAN)
filterpivotwave_array=make_array(n_filters, value=!Values.F_NAN)

for n=0, n_filters-1 do begin 

	filterpivotwave_array[n]=filterpivotwavelength(filters[n])

	readcol, filters[n], filterlambda, filtertransmission, /silent
	filterwavelow_array[n]=min(filterlambda[where(filtertransmission ne 0.0 )])
	filterwavehigh_array[n]=  max(filterlambda[where(filtertransmission ne 0.0 )])

endfor

sedlow =min(filterwavelow_array)
sedhigh=max(filterwavehigh_array)

sedwaverange=make_array( 1.0+floor((sedhigh-sedlow)/10.0),value=!Values.F_NAN)
for n=0, n_elements(sedwaverange)-1 do sedwaverange[n]=floor(sedlow)+10.0*n


;;;;;;;;;;;;;;;;;;;;;;;;;;
filtertransmission_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)
filternormtransmission_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)
filterweights_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)
filtertotalweights_array=make_array(n_elements(sedwaverange), value=!Values.F_NAN)
filterflux_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)
filterweightedflux_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)
weightedflux_array=make_array(n_elements(sedwaverange), value=!Values.F_NAN)

for n=0, n_filters-1 do begin 

	readcol, filters[n], filterlambda, filtertransmission, /silent
	filtertransmission_array[n,*]=interpol(filtertransmission, filterlambda, sedwaverange)

; fix any negatives
negatives=where(filtertransmission_array[n,*] lt 0.0, negcount)
if negcount gt 0 then	filtertransmission_array[n,negatives]=0.0
	filternormtransmission_array[n,*]=filtertransmission_array[n,*]/total(filtertransmission_array[n,*],/nan)
	filterweights_array[n,*]=filtertransmission_array[n,*]/total(filtertransmission_array[n,*],/nan)
	filterflux_array[n,*]=mag2vegaflux(mags[n],filters[n])
endfor

roughsed=interpol(filterflux_array[*,5], filterpivotwave_array,sedwaverange)

for n=0, n_elements(sedwaverange)-1 do filtertotalweights_array[n]=total(filterweights_array[*,n],/nan)

filtertotalweights_array[where(filtertotalweights_array lt 0.002)]=!Values.F_NAN

for n=0, n_elements(sedwaverange)-1 do for f=0, n_filters-1 do filterweightedflux_array[f,n]=filterflux_array[f,n]*filterweights_array[f,n]/filtertotalweights_array[n]

for n=0, n_elements(sedwaverange)-1 do  weightedflux_array[n]=total(filterweightedflux_array[*,n],/nan)

missing=where( weightedflux_array eq 0 or   finite(weightedflux_array) eq 0 , missingcount) 
good   =where( weightedflux_array ne 0 and  finite(weightedflux_array) eq 1 , goodcount) 
weightedflux_array[missing] = interpol(weightedflux_array[good], sedwaverange[good], sedwaverange[missing])


sed_wave_array=sedwaverange
sed_flux_array=weightedflux_array

sed_flux_array[where(sed_wave_array lt min(filterpivotwave_array))]=mean(sed_flux_array[where(abs(sed_wave_array - min(filterpivotwave_array)) lt 12)])  
sed_flux_array[where(sed_wave_array gt max(filterpivotwave_array))]=mean(sed_flux_array[where(abs(sed_wave_array - max(filterpivotwave_array)) lt 12)])  


;; if the filter curve happens to use 0 Angstroms as its starting point, 
;; set the flux there to zero to avoid infinite energy

if sed_wave_array[0] eq 0 then sed_flux_array[0]=0.0
;;;;;;;;;;;;;;;;;;;;
;;; compute count rate to flux conversion for each filter
	
filterfluxconversions_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)

for f=0, n_filters-1 do filterfluxconversions_array[f,*]=roughsed/obs_counts_array[f]	

for f=0, n_filters-1 do  filterflux_array[f,*]=filterfluxconversions_array[f,*]*obs_counts_array[f]

for n=0, n_elements(sedwaverange)-1 do for f=0, n_filters-1 do filterweightedflux_array[f,n]=filterflux_array[f,n]*filterweights_array[f,n]/filtertotalweights_array[n]
for n=0, n_elements(sedwaverange)-1 do  weightedflux_array[n]=total(filterweightedflux_array[*,n],/nan)

missing=where( weightedflux_array eq 0 or  finite(weightedflux_array) eq 0 ,missingcount) 
good=where( weightedflux_array ne 0 and  finite(weightedflux_array) eq 1 , goodcount) 
weightedflux_array[missing]=interpol(weightedflux_array[good], sedwaverange[good], sedwaverange[missing])
sed_flux_array=weightedflux_array


;;;;;;;;;; test the SED maker

;;; plot against the testspectrum

;sniimodelphases=[1.5, 2.5, 7.5, 9.5, 14.5, 15.5, 20.6,  27.6, 32.6, 41.6, 56.6, 72.5]

;sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']

;testspectrum=sniimodelspecs[8]


;readcol, testspectrum, sp_wave, sp_flux, /silent
;plot, sp_wave, sp_flux, xrange=[1000,10000], /ylog
;oplot, sed_wave_array, sed_flux_array, psym=-4, symsize=2, thick=2


;;;; compute photometry from sed and compare to input mags
;;;; iterate until all filters agree to within 0.02 mag
goodfilters=0
sed_mag_array=fltarr(n_filters)

iteration=0

;;;;;;;;;;;;;;;;;;;


while goodfilters lt n_filters and iteration lt 10 do begin
;	print, 'iteration ', iteration

	for n=0, n_filters-1 do sed_mag_array[n]=vegaphot([transpose(sed_wave_array), transpose(sed_flux_array)], filters[n])

	deltamag=mags-sed_mag_array

	sed_counts_array=10.0^((vegazeropoint_array-sed_mag_array)/2.5)

	goodfilters=n_elements(where(abs(deltamag) lt magerrs) )

	ratios=10.0^(-0.4*deltamag)

;	print, deltamag

;;;;;;;;;;;;;;;;;;;;
;;; compute count rate to flux conversion for each filter
	

filterfluxconversions_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)

for f=0, n_filters-1 do filterfluxconversions_array[f,*]=sed_flux_array/sed_counts_array[f]	

for f=0, n_filters-1 do  filterflux_array[f,*]=filterfluxconversions_array[f,*]*obs_counts_array[f]


 for n=0, n_elements(sedwaverange)-1 do for f=0, n_filters-1 do filterweightedflux_array[f,n]=filterflux_array[f,n]*filterweights_array[f,n]/filtertotalweights_array[n]
  for n=0, n_elements(sedwaverange)-1 do  weightedflux_array[n]=total(filterweightedflux_array[*,n],/nan)

missing=where( weightedflux_array eq 0 or  finite(weightedflux_array) eq 0 ,missingcount) 
good=where( weightedflux_array ne 0 and  finite(weightedflux_array) eq 1 , goodcount) 
weightedflux_array[missing]=interpol(weightedflux_array[good], sedwaverange[good], sedwaverange[missing])

;;;;;;;;;;;;;;;;;;;;
	;;;;;;;;;;

	sed_flux_array=weightedflux_array

for n=0,n_elements(sed_flux_array) - 1 do sed_flux_array[n]=mean(sed_flux_array[where(abs(sed_wave_array - sed_wave_array[n]) lt 21)])  


;	oplot, sed_wave_array, sed_flux_array, psym=-4, symsize=2, thick=2

	iteration = iteration +1
	

endwhile

;oplot, sed_wave_array, sed_flux_array, psym=-3, symsize=3, thick=2

sed=[transpose(sed_wave_array), transpose(sed_flux_array)]

;stop
end