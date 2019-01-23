pro SN2018oh_sed

SNname='SN2018oh'

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
uvotmagerr_array=dt.magerr_array
uvotmjd_array=dt.time_array

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt']


;for e=3,n_elements(uvotmjd_array)-1 do begin
for e=6,6 do begin

;makesedfromphot, uvotmag_array[where(finite(uvotmag_array[*,e]) eq 1),e], filters[where(finite(uvotmag_array[*,e]) eq 1)], sed

print, ' '
;print, uvotmjd_array[e]
;print, sed




weightedmangletemplateerr, uvotmag_array[where(finite(uvotmag_array[*,e]) eq 1),e], uvotmagerr_array[where(finite(uvotmag_array[*,e]) eq 1),e], filters[where(finite(uvotmag_array[*,e]) eq 1)], '/Users/pbrown/Desktop/Dropbox/SN/snscripts//SN2011fe_boloP000072.dat', mangledspectrum


pjb_uvotspec_all, mangledspectrum, mag_array=mag_array, lambda=lambda, fluxdensityfactors=fluxdensityfactors, filtereffwavelength=filtereffwavelength

plot, mangledspectrum[0,*], mangledspectrum[1,*], xrange=[1600,6000], /ylog
oplot, filtereffwavelength, dt.counts_array[0:5,e]*fluxdensityfactors[0:5], psym=4 

print, ' '
print, uvotmjd_array[e]
print, filtereffwavelength[0:5], dt.counts_array[0:5,e]*fluxdensityfactors[0:5]


print, uvotmag_array[where(finite(uvotmag_array[*,e]) eq 1),e]
print, mag_array[0:5]

pjb_uvotspec_all, [transpose(lambda), transpose(interpol(dt.counts_array[0:5,e]*fluxdensityfactors[0:5],filtereffwavelength[0:5], lambda))], mag_array=mag_array, lambda=lambda, fluxdensityfactors=fluxdensityfactors, filtereffwavelength=filtereffwavelength

print, mag_array

endfor



stop
end
