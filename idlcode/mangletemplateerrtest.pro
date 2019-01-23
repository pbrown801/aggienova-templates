pro mangletemplateerrtest, mags, magerrs, filters, templatespectrum, mangledspectrum

mags=[19.5973, 19.9387, 18.4246, 18.5519, 16.8320, 15.6710]

magerrs=[ 0.200000, 0.200000, 0.200000, 0.200000 , 0.0690000, 0.0640000]

filters=['$SNSCRIPTS/filters/UVW2_B11.txt', '$SNSCRIPTS/filters/UVM2_B11.txt', '$SNSCRIPTS/filters/UVW1_B11.txt', '$SNSCRIPTS/filters/U_P08.txt', '$SNSCRIPTS/filters/B_P08.txt', '$SNSCRIPTS/filters/V_P08.txt', '$SNSCRIPTS/filters/r_passband_period_one_and_two.txt', '$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']
filters=['$SNSCRIPTS/filters/UVW2_B11.txt', '$SNSCRIPTS/filters/UVM2_B11.txt', '$SNSCRIPTS/filters/UVW1_B11.txt', '$SNSCRIPTS/filters/U_P08.txt', '$SNSCRIPTS/filters/B_P08.txt', '$SNSCRIPTS/filters/V_P08.txt']


sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']

templatespectrum=sniimodelspecs[10]

;stop
n_filters=n_elements(filters)
pivotwavelengths=fltarr(n_filters)
for n=0, n_filters-1 do pivotwavelengths[n]=filterpivotwavelength(filters[n])

makeweightedsedfromphot, mags, magerrs, filters, sed

photsed=sed

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

templatescaling=interpol(ratio,photsed[0,*],template_wave)

scaledtemplate_flux=template_flux*templatescaling
;   

mangledtemplatespectrum=[transpose(template_wave),transpose(scaledtemplate_flux)]

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

	for n=0, n_filters-1 do mangled_mag_array[n]=vegaphot(mangledtemplatespectrum, filters[n])

	makeweightedsedfromphot, mangled_mag_array, 0.1, filters, sed

	mangledsed=sed

	ratios=photsed[1,*]/mangledsed[1,*]
	print, ratios
	templatescaling=interpol(ratios,photsed[0,*],template_wave)

	mangledtemplatespectrum[1,*]=mangledtemplatespectrum[1,*]*templatescaling

	;;;;;;;;;;

	iteration = iteration +1
	
endwhile

mangledspectrum=mangledtemplatespectrum

stop
print, 'final stop'
end