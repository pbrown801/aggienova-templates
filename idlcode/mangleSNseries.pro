pro mangleSNseries, SNname, z, referenceepoch, EBVmw, EBVhost, bigmjdarray, bigmagarray, bigmagerrarray, filterarray, templatespectrumfile


ebvmw=ebvmw[0]
ebvhost=ebvhost[0]

restore, filename=SNname+'_filtermags.sav'

lum_dist=lumdist(z)

nepochs=n_elements(bigmjdarray)

; open data file for writing
openw,lun2, '$SNFOLDER/localtemplates/ANT-'+SNname+'.20A.sed.restframe.dat', /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UVOT photometry is fit to a single template'
printf, lun2, '# ', templatespectrumfile

; open data file for writing
openw,lun1, '$SNFOLDER/localtemplates/ANT-'+SNname+'.full.sed.restframe.dat', /get_lun

printf, lun1, '# based on '+SNname
printf, lun1, '# The UVOT photometry is fit to a single template'
printf, lun1, '# ', templatespectrumfile

templatewaverange=fltarr(2448)
templatefluxrange=fltarr(2448)
for i=0,2447 do templatewaverange[i]=1020.0+20.0*i
;print, templatewaverange

;; start with zero flux array
	for t=0,n_elements(templatewaverange)-1 do printf, lun1, -100.0, templatewaverange[t],  0.0
	for t=0,1199 do printf, lun2, -100.0, templatewaverange[t],  0.0


	mangledspectra_array=fltarr(n_elements(templatewaverange),nepochs)

	;;;;;;;;; pick the spectroscopic template

	readcol, templatespectrumfile, sp_wave,sp_flux,/silent

	;;; rebin to common wavelength range

;;;; if where gives -1 then the early data is extrapolated with the IR points

	for e=0,n_elements(templatewaverange)-1 do templatefluxrange[e]=mean(sp_flux[where(sp_wave gt templatewaverange[e]-10.0 and sp_wave lt templatewaverange[e]+10.0 )])


	templatefluxrange[where(templatewaverange lt sp_wave[0])]=sp_flux[0]


	templatespectrum=[transpose(templatewaverange),transpose(templatefluxrange)]



for n=0,nepochs-1 do begin

	phase=bigmjdarray[n]-referenceepoch

	print, 'phase ', phase


	;; apply reddening to the template
;	pro fm_unred, wave, flux, ebv, funred, R_V = R_V, gamma = gamma, x0 = x0, $
;              c1 = c1, c2 = c2, c3 = c3, c4 = c4,avglmc=avglmc, lmc2 = lmc2, $
;              ExtCurve=ExtCurve


	fm_unred, templatespectrum[0,*], templatespectrum[1,*], -ebvhost, fluxhostred

	;shift into the observer frame and then correct for mw reddening
	fm_unred, templatespectrum[0,*]*(1.0+z), fluxhostred, -ebvmw, fluxred

	shiftedspectrum=templatespectrum
	shiftedspectrum[0,*]=templatespectrum[0,*]*(1.0+z[0])
	shiftedspectrum[1,*]=fluxred/(1.0+z[0])


	weightedmangletemplateerr, bigmagarray[*,n], bigmagerrarray[*,n], filterarray, shiftedspectrum, mangledspectrum
;	plot, mangledspectrum[0,*], mangledspectrum[1,*], charsize=1
;	mangletemplateerr, bigmagarray[*,n], bigmagerrarray[*,n], filterarray, shiftedspectrum, mangledspectrum


;	oplot, mangledspectrum[0,*], mangledspectrum[1,*]
	mangledspectra_array[*,n]=mangledspectrum[1,*]

;;; this print diagnostic removed since not all supernovae will have the 6 UVOT filters
;	print, 'big mag array', bigmagarray[0:5,n]

;	pjb_uvotspec_all, mangledspectrum,  mag_array=mag_array
;	print, 'mangled mags ', mag_array[0:5]
;	if total(bigmagarray[0:5,n]-mag_array[0:5]) gt 0.2 then stop

;  now unredden the mangled spectrum
	fm_unred, mangledspectrum[0,*], mangledspectrum[1,*], ebvhost, spectrumdehostred
	fm_unred, mangledspectrum[0,*]/(1.0+z), spectrumdehostred, ebvmw, spectrumdered


;;; this was used to generate the aggienova templates in 2017   
;;;  distancefactor=(1.0+z)*((lum_dist*10.0^6)/10.0)^2.0
distancefactor=((lum_dist*10.0^6)/10.0)^2.0

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



save, filename='$SNFOLDER/localtemplates/'+SNname+'_bolospec.sav', templatewaverange, mangledspectra_array, bigmjdarray, bigmagarray, templatespectrum

;print, 'final stop'

end
