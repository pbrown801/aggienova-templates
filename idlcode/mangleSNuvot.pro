pro mangleSNuvot, SNname, z, referenceepoch, templatespectrumfile

lum_dist=lumdist(z)
distancefactor=(1.0+z)*(lum_dist/10.0)^2.0

;;;;;;;;; make the spectroscopic template

; check to see if it is a string (ie a filename) or an array
s=size(templatespectrumfile)
if (s[1] eq 7) then begin
	readcol, templatespectrumfile, sp_wave,sp_flux,/silent
	templatespectrum=[transpose(sp_wave),transpose(sp_flux)]
endif else begin
	templatespectrum=templatespectrumfile
endelse


;;; put it in the observer frame
templatespectrum[0,*]=templatespectrum[0,*]*(1.0+z)

;;;;;;;;;; now read in photometry data

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt


nfiltersinepoch=intarr(n_elements(dt.time_array))
filtercheck=intarr(n_elements(dt.time_array),6)
for n=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[n,f]=finite(dt.mag_array[f,n])
for n=0,n_elements(dt.time_array)-1 do nfiltersinepoch[n]=total(filtercheck[n,*]) 
all6=where(nfiltersinepoch eq 6)


bigmjdarray=dt.time_array[all6]
bigmagarray=dt.mag_array[*,all6]

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt']
n_filters=n_elements(filters)

filterarray=filters

plot, bigmjdarray, bigmagarray[5,*], psym=3, yrange=[22,15]



for f=0,5 do oplot, bigmjdarray, bigmagarray[f,*]



nepochs=n_elements(bigmjdarray)

mangledspectra_array=fltarr(n_elements(templatespectrum[1,*]),nepochs)

; open data file for writing
openw,lun2, 'ANT-'+SNname+'.sed.restframe.dat', /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UVOT photometry is fit by a mangled template'


for n=0,nepochs-1 do begin

;print, 'does LSQ make it this far?  5 ', n


	phase=bigmjdarray[n]-referenceepoch
;print, bigmagarray[*,n]
;print, filterarray
plot, templatespectrum[0,*], templatespectrum[1,*]

	mangletemplate, bigmagarray[*,n], filterarray, templatespectrum, mangledspectrum
plot, mangledspectrum[0,*], mangledspectrum[1,*]
	mangledspectra_array[*,n]=mangledspectrum[1,*]
	for t=0,n_elements(mangledspectrum[0,*])-1 do printf, lun2, phase/(1.0+z), mangledspectrum[0,t]/(1.0+z),  distancefactor*mangledspectrum[1,t]


endfor


; close spectrum file
close, lun2
free_lun, lun2

save, filename=SNname+'_bolospec.sav', mangledspectra_array, bigmjdarray, bigmagarray, templatespectrum

print, 'final stop'
stop
end
