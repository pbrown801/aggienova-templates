pro weightedmangletemplateerr, mags, magerrs, filters, templatespectrum, mangledspectrum

;stop
n_filters=n_elements(filters)
pivotwavelengths=fltarr(n_filters)
for n=0, n_filters-1 do pivotwavelengths[n]=filterpivotwavelength(filters[n])
filterpivotwave_array=pivotwavelengths
;;;;;;;;


makeweightedsedfromphot, mags, magerrs, filters, sed

photsed=sed

;plot, sed[0,*], sed[1,*]


;;;;;;;;;  mangle a template by compared photometric SEDs
templatemag_array=fltarr(n_filters)
for n=0, n_filters-1 do templatemag_array[n]=vegaphot(templatespectrum, filters[n])
makeweightedsedfromphot, templatemag_array, 0.1, filters, sed

templatesed=sed

ratio=photsed[1,*]/templatesed[1,*]
;plot, ratio

;;;;;;;;;


; check to see if it is a string (ie a filename) or an array
s=size(templatespectrum)
if (s[1] eq 7) then begin
	readcol, templatespectrum, template_wave, template_flux,/silent
endif else begin
	template_wave=transpose(templatespectrum[0,*])
	template_flux=transpose(templatespectrum[1,*])
endelse



;;;;;;;;;
sedwaverange=template_wave

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
	filtertransmission_array[n,where(filtertransmission_array[n,*] lt 0.0)]=0.0
	filternormtransmission_array[n,*]=filtertransmission_array[n,*]/total(filtertransmission_array[n,*],/nan)
	filterweights_array[n,*]=filtertransmission_array[n,*]/total(filtertransmission_array[n,*],/nan)
	filterflux_array[n,*]=mag2vegaflux(mags[n],filters[n])
endfor

for n=0, n_elements(sedwaverange)-1 do filtertotalweights_array[n]=total(filterweights_array[*,n],/nan)

filtertotalweights_array[where(filtertotalweights_array lt 0.002)]=!Values.F_NAN

for n=0, n_elements(sedwaverange)-1 do for f=0, n_filters-1 do filterweightedflux_array[f,n]=filterflux_array[f,n]*filterweights_array[f,n]/filtertotalweights_array[n]


;;;;;;;;


;;;;;;;;;


;readcol,templatespectrum, template_wave, template_flux, /silent

templatescaling=interpol(ratio,photsed[0,*],template_wave)

;  this was to append ends of templates scaled to the end, but it already extrapolates with a constant out to the end
; well maybe it doesn't

minindex=where( abs(template_wave-min(pivotwavelengths)) eq min(abs(template_wave-min(pivotwavelengths))))

maxindex=where( abs(template_wave-max(pivotwavelengths)) eq min(abs(template_wave-max(pivotwavelengths))))

templatescaling[where(template_wave lt min(pivotwavelengths) )]= templatescaling[minindex]
templatescaling[where(template_wave gt max(pivotwavelengths) )]= templatescaling[maxindex]


scaledtemplate_flux=template_flux*templatescaling
;   

mangledtemplatespectrum=[transpose(template_wave),transpose(scaledtemplate_flux)]
;mangledtemplatespectrum=[template_wave,scaledtemplate_flux]

mangledtemplatemag_array=fltarr(n_filters)
for n=0, n_filters-1 do mangledtemplatemag_array[n]=vegaphot(mangledtemplatespectrum, filters[n])

;;;;;;;;;;;;;;;;
;;;; compute photometry from mangled template spectrum and compare to input mags
;;;; iterate until all filters agree to within the errors
goodfilters=0
mangled_mag_array=fltarr(n_filters)

iteration=0


;; do at least 2 iterations and quit when matching to within the errors 
;; or just give up after ten iterations

while (goodfilters lt n_filters and iteration lt 10)  or iteration lt 2 do begin
	print, 'iteration ', iteration

	for n=0, n_filters-1 do mangled_mag_array[n] = vegaphot(mangledtemplatespectrum, filters[n])

	deltamag=mags-mangled_mag_array
	goodfilters=n_elements(where(abs(deltamag) lt magerrs) )


;;;;;;;;

	ratios=10.0^(-0.4*deltamag)
;	ratios=[ratios[0],ratios,ratios[n_filters-1] ]
	print, ratios
;	templatescaling=interpol(ratios,photsed[0,*],template_wave)

;stop
;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;
;;; compute count rate to flux conversion for each filter
	

filterweightedratio_array=make_array(n_filters, n_elements(sedwaverange), value=!Values.F_NAN)
weightedratio_array=make_array(n_elements(sedwaverange), value=!Values.F_NAN)


 for n=0, n_elements(sedwaverange)-1 do for f=0, n_filters-1 do filterweightedratio_array[f,n]=ratios[f]*filterweights_array[f,n]/filtertotalweights_array[n]
  for n=0, n_elements(sedwaverange)-1 do  weightedratio_array[n]=total(filterweightedratio_array[*,n],/nan)

missing=where( weightedratio_array eq 0 or  finite(weightedratio_array) eq 0 ,missingcount) 
good=where( weightedratio_array ne 0 and  finite(weightedratio_array) eq 1 , goodcount) 
weightedratio_array[missing]=interpol(weightedratio_array[good], sedwaverange[good], sedwaverange[missing])


weightedratio_array[where(sedwaverange lt min(filterpivotwave_array))]=mean(weightedratio_array[where(abs(sedwaverange - min(filterpivotwave_array)) lt 12)])  
weightedratio_array[where(sedwaverange gt max(filterpivotwave_array))]=mean(weightedratio_array[where(abs(sedwaverange - max(filterpivotwave_array)) lt 12)])  

templatescaling=weightedratio_array

; apply some smoothing
for n=0,n_elements(templatescaling) - 1 do templatescaling[n]=mean(templatescaling[where(abs(sedwaverange - sedwaverange[n]) lt 21)])  


;;;;;;;;;;;;;;;;;;;;





;;;;;;;;;;;;;;;
	mangledtemplatespectrum[1,*]=mangledtemplatespectrum[1,*]*templatescaling

	;;;;;;;;;;

	iteration = iteration +1
	
endwhile

mangledspectrum=mangledtemplatespectrum

print, 'deltamag ', deltamag
;stop
;print, 'final stop'
end