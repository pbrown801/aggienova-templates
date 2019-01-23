pro mangleSNIIP, SNname, z, referenceepoch, bigmjdarray, bigmagarray, filterarray

; .run pjb_phot_array_B141
;; for testing
;SNname='SN2008in'
;z=0.005

;referenceepoch=54828.0

lum_dist=lumdist(z)
distancefactor=(1.0+z)*(lum_dist/10.0)^2.0

nepochs=n_elements(bigmjdarray)


; open data file for writing
openw,lun2, 'ANT-'+SNname+'.sed.restframe.dat', /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UVOT photometry is fit by a mangled template of SN2016ccj '
printf, lun2, '# using HST and NOT spectra and a blackbody extension. '

sniimodelphases=[1.5, 2.5, 7.5, 9.5, 14.5, 15.5, 20.6,  27.6, 32.6, 41.6, 56.6, 72.5]

sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']


for n=0,nepochs-1 do begin

	phase=bigmjdarray[n]-referenceepoch

	;;;;;;;;; pick the spectroscopic template

	closest=where(abs(phase-sniimodelphases) eq min(abs(phase-sniimodelphases)) )

	templatespectrumfile=sniimodelspecs[closest]

	readcol, templatespectrumfile, sp_wave,sp_flux,/silent
	templatespectrum=[transpose(sp_wave),transpose(sp_flux)]


	;;; put it in the observer frame
	templatespectrum[0,*]=templatespectrum[0,*]*(1.0+z)
	mangledspectra_array=fltarr(n_elements(templatespectrum[1,*]),nepochs)

	print, bigmagarray[*,n]
	print, filterarray
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

end
