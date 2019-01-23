pro filterfluxconversions, filter_array, spectrum, filterfluxconversions_array

n_filters=n_elements(filter_array)
filterfluxconversions_array=make_array(n_filters, value=!Values.F_NAN)

; check to see if it is a string (ie a filename) or an array
s=size(spectrum)
if (s[1] eq 7) then begin
	readcol,spectrum,sp_wave,sp_flux,/silent
endif else begin
	sp_wave=spectrum[0,*]
	sp_flux=spectrum[1,*]
endelse


vegazeropoint_array=make_array(n_filters, value=!Values.F_NAN)
counts_array=make_array(n_filters, value=!Values.F_NAN)
magss_array=make_array(n_filters, value=!Values.F_NAN)

for f=0, n_filters-1 do begin
	vegazeropointout=vegazeropoint(filter_array[f])
	vegazeropoint_array[f]=vegazeropointout
	mags_array[f]=vegaphot(spectrum,filter_array[n]
endfor


counts_array=10.0^((vegazeropoint_array-mags_array)/2.5)

for f=0, n_filters-1 do filterfluxconversions_array[f]=roughsed/obs_counts_array[f]	


end