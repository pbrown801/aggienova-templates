pro testmakesed

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/kpno_r.txt','$SNSCRIPTS/filters/johnson_i.txt']
n_filters=n_elements(filters)


testspectrum='$SNSCRIPTS/SN2011fe_boloP000072.dat'
readcol, testspectrum, test_wave, test_flux,/silent
testmag_array=fltarr(n_filters)
for n=0, n_filters-1 do testmag_array[n]=vegaphot(testspectrum, filters[n])
mags=testmag_array

templatespectrum='$SNSCRIPTS/sn1a_hsiao_18.dat'


mangletemplate, mags, filters, templatespectrum, mangledspectrum
w2check=mangledspectrum

mags=mags[1:n_elements(mags)-1]

filters=['$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/kpno_r.txt','$SNSCRIPTS/filters/johnson_i.txt']
n_filters=n_elements(filters)

mangletemplate, mags, filters, templatespectrum, mangledspectrum
m2check=mangledspectrum

mags=testmag_array

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/kpno_r.txt','$SNSCRIPTS/filters/johnson_i.txt']
n_filters=n_elements(filters)

newtemplatespectrum=mangledspectrum



mangletemplate, mags, filters, newtemplatespectrum, newmangledspectrum
w2back=newmangledspectrum


cgplot,  w2check[0,*], w2check[1,*], /ylog, color='blue', xrange=[2000,4000]
cgoplot, w2check[0,*], m2check[1,*], color='red'
cgoplot, w2check[0,*], w2back[1,*], color='green'
oplot, test_wave, test_flux, thick=2

;; the above test shows that mangling the SED without the w2 filter 
;; and then remangling that filter doesn't result in anything much different 
;; then just mangling it with the w2 filter.
;; and for this Ia comparison, the resultant dip in uvm2 when the uvw2 filter is used 
;; does look visually better than when the uvw2 filter is ignored. 
;; the uvm2 photometry isn't affected much, as the mangling fixes that anyway, 
;; but the uvw2 filter appears to be able to allow one to match the higher uvw2 flux and uvm2 dip

pivotwavelengths=fltarr(n_filters)
for n=0, n_filters-1 do pivotwavelengths[n]=filterpivotwavelength(filters[n])

makesedfromphot, mags, filters, sed

plot, sed[0,*], sed[1,*]


;;;;;;;;;  now mangle a template by compared photometric SEDs


testspectrum='$SNSCRIPTS/SN2011fe_boloP000072.dat'
testmag_array=fltarr(n_filters)
for n=0, n_filters-1 do testmag_array[n]=vegaphot(testspectrum, filters[n])
mags=testmag_array
makesedfromphot, mags, filters, sed
testsed=sed

templatespectrum='$SNSCRIPTS/sn1a_hsiao_18.dat'
templatemag_array=fltarr(n_filters)
for n=0, n_filters-1 do templatemag_array[n]=vegaphot(templatespectrum, filters[n])
makesedfromphot, templatemag_array, filters, sed

templatesed=sed

ratio=testsed[1,*]/templatesed[1,*]
plot, ratio

readcol,templatespectrum, template_wave, template_flux, /silent

templatescaling=interpol(ratio,testsed[0,*],template_wave)

scaledtemplate_flux=template_flux*templatescaling
;   
;  this was to append ends of templates scaled to the end, but it already extrapolating witha constant out to the end
;scaledtemplate_flux[ where(template_wave lt pivotwavelengths[0]) ]= ratio[0]*template_flux[ where(template_wave lt pivotwavelengths[0]) ]

;scaledtemplate_flux[ where(template_wave gt pivotwavelengths[n_filters-1]) ]= ratio[n_filters-1]*template_flux[ where(template_wave gt pivotwavelengths[n_filters-1]) ]


readcol,testspectrum, test_wave, test_flux, /silent

cgplot, test_wave, test_flux, color='blue'
oplot,  template_wave, scaledtemplate_flux, color='red'

plot, template_wave,templatescaling

mangledtemplatespectrum=[transpose(template_wave),transpose(scaledtemplate_flux)]

mangledtemplatemag_array=fltarr(n_filters)
for n=0, n_filters-1 do mangledtemplatemag_array[n]=vegaphot(mangledtemplatespectrum, filters[n])

;;;;;;;;;;;;;;;;
;;;; compute photometry from mangled template spectrum and compare to input mags
;;;; iterate until all filters agree to within 0.02 mag
goodfilters=0
mangled_mag_array=fltarr(n_filters)

iteration=0

while goodfilters lt n_filters do begin
	print, 'iteration ', iteration

	for n=0, n_filters-1 do mangled_mag_array[n]=vegaphot(mangledtemplatespectrum, filters[n])

	deltamag=mags-mangled_mag_array
	goodfilters=n_elements(where(abs(deltamag) lt 0.02) )
	ratios=10.0^(-0.4*deltamag)
	ratios=[ratios[0],ratios,ratios[n_filters-1] ]
	templatescaling=interpol(ratios,testsed[0,*],template_wave)

	mangledtemplatespectrum[1,*]=mangledtemplatespectrum[1,*]*templatescaling

	;;;;;;;;;;

	iteration = iteration +1
	
endwhile

cgplot, test_wave, test_flux, color='blue'
oplot,  mangledtemplatespectrum[0,*], mangledtemplatespectrum[1,*], color='red'


stop
end
