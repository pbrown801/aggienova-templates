pro makesedfromphot, mags, filters, sed

;stop
if n_elements(mags) ne n_elements(filters) then print, ' Each magnitude needs a filter path and vice versa. '
if n_elements(mags) ne n_elements(filters) then stop


;;;;;;;;;;;;;;;;;;;;;;;;;; these will be the inputs
;mags=[0.0,0,0,0,0,0,0,0]
;magerrs=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]

;filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/kpno_r.txt','$SNSCRIPTS/filters/johnson_i.txt']

n_filters=n_elements(filters)


;testspectrum='$SNSCRIPTS/SN2011fe_boloP000072.dat'
;testmag_array=fltarr(n_filters)
;for n=0, n_filters-1 do testmag_array[n]=vegaphot(testspectrum, filters[n])
;mags=testmag_array

;;;;;;;;;;;;;;;;;;;;;;;;;;


magsed_flux=fltarr(n_filters)
magsed_wave=fltarr(n_filters)

; create SED from the magnitudes based on the Vega spectrum

for n=0, n_filters-1 do magsed_wave[n]=filterpivotwavelength(filters[n])
for n=0, n_filters-1 do magsed_flux[n]=mag2vegaflux(mags[n],filters[n])

;; rearrange just in case they are not in order

mags=mags[sort(magsed_wave)]
filters=filters[sort(magsed_wave)]

magsed_flux=magsed_flux[sort(magsed_wave)]
magsed_wave=magsed_wave[sort(magsed_wave)]

;;;;;;;;; find the endpoints of the filter curves to which to extrapolate the spectrum 

readcol, filters[0], filterlambda, filtertransmission,/silent
specbegin=min(filterlambda)

readcol, filters[n_filters-1], filterlambda, filtertransmission,/silent
specend=max(filterlambda)

sed_flux_array=transpose([magsed_flux[0], magsed_flux, magsed_flux[n_filters-1]])
sed_wave_array=transpose([specbegin,magsed_wave,specend])

;; if the filter curve happens to use 0 Angstroms as its starting point, 
;; set the flux there to zero to avoid infinite energy

if specbegin eq 0 then sed_flux_array[0]=0.0

;;;;;;;;;; test the SED maker

;;; plot against the testspectrum

;readcol, testspectrum, sp_wave, sp_flux, /silent
;plot, sp_wave, sp_flux, xrange=[1000,10000]
;oplot, sed_wave_array, sed_flux_array, psym=-4, symsize=2, thick=2


;;;; compute photometry from sed and compare to input mags
;;;; iterate until all filters agree to within 0.02 mag
goodfilters=0
sed_mag_array=fltarr(n_filters)

iteration=0

;;;;;;;;;;;;;;;;;;;


while goodfilters lt n_filters and iteration lt 10 do begin
;	print, 'iteration ', iteration

	for n=0, n_filters-1 do sed_mag_array[n]=vegaphot([sed_wave_array, sed_flux_array], filters[n])

	deltamag=mags-sed_mag_array
	goodfilters=n_elements(where(abs(deltamag) lt 0.02) )
	ratios=10.0^(-0.4*deltamag)

	if iteration lt 5 then ratios[where(filters eq '$SNSCRIPTS/filters/UVW2_B11.txt')]=(ratios[where(filters eq '$SNSCRIPTS/filters/UVW2_B11.txt')]+ratios[where(filters eq '$SNSCRIPTS/filters/UVM2_B11.txt')])/2.0

	if iteration lt 5 then ratios[where(filters eq '$SNSCRIPTS/filters/UVW1_B11.txt')]=(ratios[where(filters eq '$SNSCRIPTS/filters/UVW1_B11.txt')]+ratios[where(filters eq '$SNSCRIPTS/filters/UVM2_B11.txt')]+ratios[where(filters eq '$SNSCRIPTS/filters/U_P08.txt')])/3.0



	print, deltamag

	;;;;;;;;;;

	sed_flux_array=sed_flux_array[1:n_filters]*ratios
	sed_flux_array=transpose([sed_flux_array[0], sed_flux_array, sed_flux_array[n_filters-1]])

	iteration = iteration +1
	
endwhile

;oplot, sed_wave_array, sed_flux_array, psym=-3, symsize=3, thick=2

sed=[sed_wave_array, sed_flux_array]


end

