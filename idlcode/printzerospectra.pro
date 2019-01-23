pro printzerospectra


;  read in wavelengthrange
samplespec='sniimodels/tst_n20_5_B.fl'
readcol, samplespec, sp_wave,sp_flux,/silent


; open data file for writing
openw,lun2, 'ANT-zerofluxepoch-100.sed.restframe.dat', /get_lun

printf, lun2, '# just prints out a zero flux spectrum for a pre-explosion epoch '

phase = -100
for t=0,n_elements(sp_wave)-1 do printf, lun2, phase, sp_wave[t], 0

; close spectrum file
close, lun2
free_lun, lun2




openw,lun2, 'ANT-zerofluxepoch+1000.sed.restframe.dat', /get_lun

printf, lun2, '# just prints out a zero flux spectrum for a pre-explosion epoch '

phase = 1000
for t=0,n_elements(sp_wave)-1 do printf, lun2, phase, sp_wave[t], 0

; close spectrum file
close, lun2
free_lun, lun2


stop
end