pro checkgmags

SNnames=['SN2007pk','SN2007od','SN2008in','SN2013by','SN2006at','SN2007pk','SN2012aw','SN2006aj']

	peak_g_mags_array=fltarr(n_elements(SNnames))
	peak_g_epoch_array=intarr(n_elements(SNnames))


for n=0, n_elements(SNnames)-1 do begin

	SNname=SNnames[n]

	templatefile='$SNFOLDER/localtemplates/ANT-'+SNname+'.20A.sed.restframe.dat'

;	templatefile='$SNFOLDER/localtemplates/ANT-'+SNname+'.full.sed.restframe.dat'


	readcol, templatefile, restphase, lambda_rest, f_lambda, /silent

	epochlist= restphase[UNIQ(restphase, SORT(restphase))]

	n_epochs=n_elements(epochlist)

	template_g_mag_array=fltarr(n_epochs-2)

	for e=1, n_epochs-2 do begin
;for e=1, 50 do begin

	spectrumwaverest=lambda_rest[where(restphase eq epochlist[e])]

	spectrumflux=f_lambda[where(restphase eq epochlist[e])] ;/distancefactor

	originalspectrum=[transpose(spectrumwaverest),transpose(spectrumflux)]

	template_g_mag_array[e-1]=abphot(originalspectrum, '/Users/pbrown/Desktop/Dropbox/SN/aggienova/code/Aggienova/filters/LSST_g.dat')

endfor


	peak_g_mags_array[n]=min(template_g_mag_array,location,/nan)
	peak_g_epoch_array[n]=location+1



if n eq 0 then plot, epochlist, template_g_mag_array[1:n_epochs-3], yrange=[-10,-20], xrange=[0,100], charsize=2, xtitle='Epoch [days]', ytitle='Templage g mags'

stop

oplot, epochlist, template_g_mag_array[1:n_epochs-3]



endfor

stop

for n=0, n_elements(SNnames)-1 do begin

	SNname=SNnames[n]

;	templatefile='$SNFOLDER/localtemplates/ANT-'+SNname+'.20A.sed.restframe.dat'

	templatefile='$SNFOLDER/localtemplates/ANT-'+SNname+'.full.sed.restframe.dat'


	readcol, templatefile, restphase, lambda_rest, f_lambda, /silent

	epochlist= restphase[UNIQ(restphase, SORT(restphase))]

	spectrumwaverest=lambda_rest[where(restphase eq epochlist[peak_g_epoch_array[n]])]

	spectrumflux=f_lambda[where(restphase eq epochlist[e])] ;/distancefactor


if n eq 0 then plot, spectrumwaverest, -2.5*alog10(spectrumflux*3.34*10.0^4.0*spectrumwaverest^2.0/3631.0), yrange=[-10,-20], xrange=[1000,10000], charsize=2



oplot, spectrumwaverest, -2.5*alog10(spectrumflux*3.34*10.0^4.0*spectrumwaverest^2.0/3631.0)


endfor


;;;;;;;;;;;;;





print, 'final stop'
stop
end