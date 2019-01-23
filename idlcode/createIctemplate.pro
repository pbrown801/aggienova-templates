pro createlctemplate



h = 1D*6.626E-27
c = 1D*2.998E18
hc = 1D*1.986E-8
e = 1D*2.71828
k = 1D*1.38E-16

SNname='SN1994I'
z=0.001544
;;;;;;;;;;; create template spectrum

templatefilename=SNname+'_peaktemplatespectrum.dat'

UVspectrum='$SNSCRIPTS/SN1994I_UV.dat'

readcol, UVspectrum, uv_wave, uv_flux

optspectrum='sn1994i-19940420-final.flm'

optspectrum='sn1994i-19940418-final-red.flm'


readcol, optspectrum, opt_wave, opt_flux

cgplot, uv_wave, uv_flux, color='blue', xrange=[1500,10000], /ylog

;; already deredshifted
cgplot, uv_wave, uv_flux, color='blue', xrange=[1500,30000]
;cgoplot, opt_wave/(1.0+z), opt_flux*0.4*10.0^(-15), color='red'
cgoplot, opt_wave/(1.0+z), opt_flux*1.5*10.0^(-15), color='red'

;; set up wavelength range for output
range=35000-900
fullwave=fltarr(range/10)
for f=0,n_elements(fullwave)-1 do fullwave[f]=900.0+f*10.0


T=8000.0
bbspec=1L*2.0*h*c^2.0/((fullwave)^5.0*(e^(h*c/((fullwave)*k*T))-1.0))

factor=mean(bbspec[where(fullwave gt 10000.0 and fullwave lt 10200.0)]) / mean(1.5*10.0^(-15.0)*opt_flux[where(opt_wave/(1.0+z) gt 10000.0 and opt_wave/(1.0+z) lt 10200.0)])

cgoplot, fullwave, bbspec/factor, color='maroon'

uvfactor=mean(bbspec[where(fullwave gt 1900.0 and fullwave lt 2100.0)]) / mean(uv_flux[where(uv_wave gt 1900.0 and uv_wave lt 2100.0)])

cgoplot, fullwave, bbspec/uvfactor, color='violet'

bigwave=[ fullwave[where(fullwave lt 2000.0)], uv_wave[where(uv_wave gt 2000.0 and uv_wave lt 7000.0)]/(1.0+z), opt_wave[where(opt_wave/(1.0+z) gt 7000.0 and opt_wave/(1.0+z) lt 10000.0)]/(1.0+z), fullwave[where(fullwave gt 10000.0)] ]


bigflux=[ bbspec[where(fullwave lt 2000.0)]/uvfactor, uv_flux[where(uv_wave gt 2000.0 and uv_wave/(1.0+z) lt 7000.0)]/(1.0+z), 1.5*10.0^(-15)*opt_flux[where(opt_wave/(1.0+z) gt 7000.0 and opt_wave/(1.0+z) lt 10000.0)]/(1.0+z), bbspec[where(fullwave gt 10000.0)]/factor ]

plot, bigwave, bigflux, xrange=[1000,10000]

plot, bigwave, bigflux, xrange=[1000,30000], /ylog

fullflux=fullwave

for n=0,n_elements(fullflux)-1 do fullflux[n]=mean(bigflux[where(  abs(bigwave-fullwave[n]) le 10.0)  ])

templatespectrum=[ transpose(fullwave), transpose(fullflux) ]


openw,lun2, templatefilename, /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UV spectrum is from HST (Millard et al. 1999 )
printf, lun2, '# The optical spectrum is from Filippenko et al. (1995'

for n=0,n_elements(fullflux)-1 do  printf, lun2, templatespectrum[0,n], templatespectrum[1,n]


; close spectrum file
close, lun2
free_lun, lun2



;;;  fdump 2003957030_o48z50010_sx1.fits columns="wavelength,flux,error,dq" outfile=SN1998S_opt_19980316_1.dat rows=1 prhead=no showcol=no showunit=no showrow=no
;;fdump 2003957033_o48z50040_x1d.fits columns="wavelength,flux,error,dq" outfile=SN1998S_nuv_19980316_1.dat rows=1 prhead=no showcol=no showunit=no showrow=no
;;fdump 2003957032_o48z50030_x1d.fits columns="wavelength,flux,error,dq" outfile=SN1998S_fuv_19980316_1.dat rows=1 prhead=no showcol=no showunit=no showrow=no


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


h = 1D*6.626E-27
c = 1D*2.998E18
hc = 1D*1.986E-8
e = 1D*2.71828
k = 1D*1.38E-16



SNname='SN1998S'
z=0.002987
;;;;;;;;;;; create template spectrum

templatefilename=SNname+'_peaktemplatespectrum.dat'

UVspectrum='SN1998S_fuv_19980316_1.dat'

readcol, UVspectrum, fuv_wave, fuv_flux

fuv_wave=fuv_wave/(1.0+z)

optspectrum='1998S_19980316_3395_9592_00.dat'

readcol, optspectrum, opt_wave, opt_flux

opt_wave=opt_wave/(1.0+z)

nuvspectrum='SN1998S_nuv_19980316_1.dat'

readcol, nuvspectrum, nuv_wave, nuv_flux

nuv_wave=nuv_wave/(1.0+z)


optspectrum='SN1998S_opt_19980316_1.dat'

readcol, optspectrum, opt_wave, opt_flux

cgplot, uv_wave, uv_flux, color='blue', xrange=[1000,2000], /ylog

;; already deredshifted
cgplot, uv_wave, uv_flux, color='blue', xrange=[1000,10000]
;cgoplot, opt_wave, opt_flux, color='red'
cgoplot, opt_wave, opt_flux, color='red'

;; set up wavelength range for output
range=35000-900
fullwave=fltarr(range/10)
for f=0,n_elements(fullwave)-1 do fullwave[f]=900.0+f*10.0


T=12000.0
bbspec=1L*2.0*h*c^2.0/((fullwave)^5.0*(e^(h*c/((fullwave)*k*T))-1.0))

factor=mean(bbspec[where(fullwave gt 9000.0 and fullwave lt 9020.0)]) / mean(opt_flux[where(opt_wave gt 9000.0 and opt_wave lt 9020.0)])

cgoplot, fullwave, bbspec/factor, color='maroon'

fuvfactor=mean(bbspec[where(fullwave gt 1150.0 and fullwave lt 1160.0)]) / mean(fuv_flux[where(fuv_wave gt 1150.0 and fuv_wave lt 1160.0)])

nuvfactor=mean(bbspec[where(fullwave gt 3000.0 and fullwave lt 3100.0)]) / mean(nuv_flux[where(nuv_wave gt 3000.0 and nuv_wave lt 3100.0)])


cgoplot, fullwave, bbspec/fuvfactor, color='violet'
cgoplot, fullwave, bbspec/nuvfactor, color='violet'

bigwave=[ fullwave[where(fullwave lt 1140.0)], fuv_wave[where(fuv_wave gt 1140.0 and fuv_wave lt 1750.0)], nuv_wave[where(nuv_wave gt 1750.0 and nuv_wave lt 3100.0)], fullwave[where(fullwave gt 3100.0 and fullwave lt 4000.0)], opt_wave[where(opt_wave gt 4000.0 and opt_wave lt 9000.0)], fullwave[where(fullwave gt 9000.0)] ]


bigflux=[ bbspec[where(fullwave lt 1140.0)]/nuvfactor, fuv_flux[where(fuv_wave gt 1140.0 and fuv_wave lt 1750.0)], nuv_flux[where(nuv_wave gt 1750.0 and nuv_wave lt 3100.0)], bbspec[where(fullwave gt 3100.0 and fullwave lt 4000.0)]/nuvfactor, opt_flux[where(opt_wave gt 4000.0 and opt_wave lt 9000.0)], bbspec[where(fullwave gt 9000.0)]/factor ]

plot, bigwave, bigflux, xrange=[1000,10000]

plot, bigwave, bigflux, xrange=[1000,30000], /ylog

fullflux=fullwave

for n=0,n_elements(fullflux)-1 do fullflux[n]=mean(bigflux[where(  abs(bigwave-fullwave[n]) le 10.0)  ])

templatespectrum=[ transpose(fullwave), transpose(fullflux) ]


openw,lun2, templatefilename, /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UV spectra are from HST (Frannson et al. 2005) '
printf, lun2, '# The optical spectrum is from Fassia et al. (2000)'

for n=0,n_elements(fullflux)-1 do  printf, lun2, templatespectrum[0,n], templatespectrum[1,n]


; close spectrum file
close, lun2
free_lun, lun2






print, 'final stop'
stop
end