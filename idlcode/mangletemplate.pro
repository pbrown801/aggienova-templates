pro mangletemplate, mags, filters, templatespectrum, mangledspectrum

;stop
n_filters=n_elements(filters)
pivotwavelengths=fltarr(n_filters)
for n=0, n_filters-1 do pivotwavelengths[n]=filterpivotwavelength(filters[n])

makesedfromphot, mags, filters, sed

photsed=sed

;plot, sed[0,*], sed[1,*]


;;;;;;;;;  mangle a template by compared photometric SEDs
templatemag_array=fltarr(n_filters)
for n=0, n_filters-1 do templatemag_array[n]=vegaphot(templatespectrum, filters[n])
makesedfromphot, templatemag_array, filters, sed

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

scaledtemplate_flux=template_flux*templatescaling
;   
;  this was to append ends of templates scaled to the end, but it already extrapolates with a constant out to the end
;scaledtemplate_flux[ where(template_wave lt pivotwavelengths[0]) ]= ratio[0]*template_flux[ where(template_wave lt pivotwavelengths[0]) ]

;scaledtemplate_flux[ where(template_wave gt pivotwavelengths[n_filters-1]) ]= ratio[n_filters-1]*template_flux[ where(template_wave gt pivotwavelengths[n_filters-1]) ]



mangledtemplatespectrum=[transpose(template_wave),transpose(scaledtemplate_flux)]
;mangledtemplatespectrum=[template_wave,scaledtemplate_flux]

mangledtemplatemag_array=fltarr(n_filters)
for n=0, n_filters-1 do mangledtemplatemag_array[n]=vegaphot(mangledtemplatespectrum, filters[n])

;;;;;;;;;;;;;;;;
;;;; compute photometry from mangled template spectrum and compare to input mags
;;;; iterate until all filters agree to within 0.02 mag
goodfilters=0
mangled_mag_array=fltarr(n_filters)

iteration=0


;; match to within 0.02 mag or just give up after ten iterations

while goodfilters lt n_filters and iteration lt 10 do begin
	print, 'iteration ', iteration

	for n=0, n_filters-1 do mangled_mag_array[n]=vegaphot(mangledtemplatespectrum, filters[n])

	deltamag=mags-mangled_mag_array
	goodfilters=n_elements(where(abs(deltamag) lt 0.02) )
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