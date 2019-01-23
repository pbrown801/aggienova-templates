pro mangletemplateerr, mags, magerrs, filters, templatespectrum, mangledspectrum

;stop
n_filters=n_elements(filters)
pivotwavelengths=fltarr(n_filters)
for n=0, n_filters-1 do pivotwavelengths[n]=filterpivotwavelength(filters[n])


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

while goodfilters lt n_filters and iteration lt 10  and iteration gt 2 do begin
	print, 'iteration ', iteration

	for n=0, n_filters-1 do mangled_mag_array[n] = vegaphot(mangledtemplatespectrum, filters[n])

	deltamag=mags-mangled_mag_array
	goodfilters=n_elements(where(abs(deltamag) lt magerrs) )
	ratios=10.0^(-0.4*deltamag)
	ratios=[ratios[0],ratios,ratios[n_filters-1] ]
	print, ratios
	templatescaling=interpol(ratios,photsed[0,*],template_wave)

	mangledtemplatespectrum[1,*]=mangledtemplatespectrum[1,*]*templatescaling

	;;;;;;;;;;

	iteration = iteration +1
	
endwhile

mangledspectrum=mangledtemplatespectrum

;stop
;print, 'final stop'
end