pro mangleSNIIPred, SNname, z, referenceepoch, EBVmw, EBVhost, bigmjdarray, bigmagarray, bigmagerrarray, filterarray

restore, filename=SNname+'_filtermags.sav'

; .run pjb_phot_array_B141
;; for testing
;SNname='SN2008in'
;z=0.005

;referenceepoch=54828.0

lum_dist=lumdist(z)

nepochs=n_elements(bigmjdarray)




; open data file for writing
openw,lun2, '$SNFOLDER/localtemplates/ANT-'+SNname+'.20A.sed.restframe.dat', /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UVOT photometry is fit to the closest epoch '
printf, lun2, '# theoretical IIP spectrum from Dessart et al. 2008 '


; open data file for writing
openw,lun1, '$SNFOLDER/localtemplates/ANT-'+SNname+'.full.sed.restframe.dat', /get_lun

printf, lun1, '# based on '+SNname
printf, lun1, '# The UVOT photometry is fit to the closest epoch '
printf, lun1, '# theoretical IIP spectrum from Dessart et al. 2008 '

sniimodelphases=[1.5, 2.5, 7.5, 9.5, 14.5, 15.5, 20.6,  27.6, 32.6, 41.6, 56.6, 72.5]

sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']

templatewaverange=fltarr(2448)
templatefluxrange=fltarr(2448)
for i=0,2447 do templatewaverange[i]=1020.0+20.0*i
;print, templatewaverange

;; start with zero flux array
	for t=0,n_elements(templatewaverange)-1 do printf, lun1, -100.0, templatewaverange[t],  0.0
	for t=0,1199 do printf, lun2, -100.0, templatewaverange[t],  0.0


	mangledspectra_array=fltarr(n_elements(templatewaverange),nepochs)


for n=0,nepochs-1 do begin

	phase=bigmjdarray[n]-referenceepoch

	print, 'phase ', phase

	;;;;;;;;; pick the spectroscopic template

	closest=where(abs(phase-sniimodelphases) eq min(abs(phase-sniimodelphases)) )

	templatespectrumfile=sniimodelspecs[closest[0]]

	readcol, templatespectrumfile[0], sp_wave,sp_flux,/silent

	;;; rebin to common wavelength range
	for e=0,n_elements(templatewaverange)-1 do templatefluxrange[e]=mean(sp_flux[where(sp_wave gt templatewaverange[e]-10.0 and sp_wave lt templatewaverange[e]+10.0 )])


	templatespectrum=[transpose(templatewaverange),transpose(templatefluxrange)]

	;; apply reddening to the template
;	pro fm_unred, wave, flux, ebv, funred, R_V = R_V, gamma = gamma, x0 = x0, $
;              c1 = c1, c2 = c2, c3 = c3, c4 = c4,avglmc=avglmc, lmc2 = lmc2, $
;              ExtCurve=ExtCurve


	fm_unred, templatespectrum[0,*], templatespectrum[1,*], -ebvhost, fluxhostred

	;shift into the observer frame and then correct for mw reddening
	fm_unred, templatespectrum[0,*]*(1.0+z), fluxhostred, -ebvmw, fluxred

	shiftedspectrum=templatespectrum
	shiftedspectrum[0,*]=templatespectrum[0,*]*(1.0+z)
	shiftedspectrum[1,*]=fluxred


	weightedmangletemplateerr, bigmagarray[*,n], bigmagerrarray[*,n], filterarray, shiftedspectrum, mangledspectrum
;	plot, mangledspectrum[0,*], mangledspectrum[1,*], charsize=1
;	mangletemplateerr, bigmagarray[*,n], bigmagerrarray[*,n], filterarray, shiftedspectrum, mangledspectrum


;	oplot, mangledspectrum[0,*], mangledspectrum[1,*]
	mangledspectra_array[*,n]=mangledspectrum[1,*]


	print, 'big mag array', bigmagarray[0:5,n]

	pjb_uvotspec_all, mangledspectrum,  mag_array=mag_array
	print, 'mangled mags ', mag_array[0:5]
;	if total(bigmagarray[0:5,n]-mag_array[0:5]) gt 0.2 then stop

;  now unredden the mangled spectrum
	fm_unred, mangledspectrum[0,*], mangledspectrum[1,*], ebvhost, spectrumdehostred
	fm_unred, mangledspectrum[0,*]/(1.0+z), spectrumdehostred, ebvmw, spectrumdered


distancefactor=(1.0+z)*((lum_dist*10.0^6)/10.0)^2.0

	outputspectrum=mangledspectrum
	outputspectrum[0,*]=mangledspectrum[0,*]/(1.0+z)
	outputspectrum[1,*]=distancefactor*spectrumdered

mangledspectra_array[*,n]=distancefactor*spectrumdered


plot, outputspectrum[0,*], outputspectrum[1,*], charsize=2

	for t=0,n_elements(outputspectrum[0,*])-1 do printf, lun1, phase/(1.0+z), outputspectrum[0,t],  outputspectrum[1,t]
	for t=0,1199 do printf, lun2, phase/(1.0+z), outputspectrum[0,t],  outputspectrum[1,t]

;pjb_uvotspec_all, templatespectrum,  mag_array=mag_array
;print, 'template mags ', mag_array

;pjb_uvotspec_all, shiftedspectrum,  mag_array=mag_array
;print, 'shifted mags ', mag_array

;print, bigmagarray[0:5,n]

;pjb_uvotspec_all, mangledspectrum,  mag_array=mag_array
;print, 'mangled mags ', mag_array[0:5]

;pjb_uvotspec_all, outputspectrum,  mag_array=mag_array
;print, 'output mags ', mag_array[0:5]

;if phase gt 10.0 then stop

endfor

for t=0,n_elements(templatewaverange)-1 do printf, lun1, 10000.0, templatewaverange[t],  0.0
for t=0,1199 do printf, lun2, 10000.0, templatewaverange[t],  0.0



; close spectrum file
close, lun2
free_lun, lun2

save, filename='$SNFOLDER/localtemplates/'+SNname+'_bolospec.sav', mangledspectra_array, bigmjdarray, bigmagarray, templatespectrum

;print, 'final stop'

end
