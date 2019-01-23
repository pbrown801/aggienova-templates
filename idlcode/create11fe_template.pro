pro create11fe_template

SNname='SN2011fe'
z=0.000804

UVspectrum='/Users/pbrown/Desktop/Dropbox/SN/snscripts/SN2011fe_peakplusthree_longestcoverage.dat'


h = 1D*6.626E-27
c = 1D*2.998E18
hc = 1D*1.986E-8
e = 1D*2.71828
k = 1D*1.38E-16

;;;;;;;;;;; create template spectrum

templatefilename=SNname+'_peaktemplatespectrum.dat'

readcol, UVspectrum, uv_wave, uv_flux


present=where(finite(uv_flux) eq 1)
notpresentwithin=where(finite(uv_flux) eq 0)
for n=0,n_elements(notpresentwithin)-1 do uv_flux[notpresentwithin[n]]=interpol(uv_flux[present], uv_wave[present], uv_wave[notpresentwithin[n]])




cgplot, uv_wave/(1.0+z), uv_flux, color='blue', xrange=[1500,10000]

;; set up wavelength range for output
templatewaverange=fltarr(3448)
templatefluxrange=fltarr(3448)
for i=0,3447 do templatewaverange[i]=1020.0+20.0*i
fullwave=templatewaverange

;range=35000-1020
;fullwave=fltarr(range/10)
;for f=0,n_elements(fullwave)-1 do fullwave[f]=900.0+f*20.0


T=14000.0
bbspec=1L*2.0*h*c^2.0/((fullwave)^5.0*(e^(h*c/((fullwave)*k*T))-1.0))

factor=mean(bbspec[where(fullwave gt 24000.0 and fullwave lt 25000.0)]) / mean(1.0*uv_flux[where(uv_wave/(1.0+z) gt 24000.0 and uv_wave/(1.0+z) lt 25000.0)])

cgoplot, fullwave, bbspec/factor, color='maroon'

uvfactor=mean(bbspec[where(fullwave gt 1150.0 and fullwave lt 1350.0)]) / mean(uv_flux[where(uv_wave/(1.0+z) gt 1150.0 and uv_wave/(1.0+z) lt 1350.0)])

cgoplot, fullwave, bbspec/uvfactor, color='violet'

bigwave=[ fullwave[where(fullwave lt 1300.0)], uv_wave[where(uv_wave/(1.0+z) gt 1300.0 and uv_wave/(1.0+z) lt 24500.0)]/(1.0+z), fullwave[where(fullwave gt 24500.0)] ]


bigflux=[ bbspec[where(fullwave lt 1300.0)]/uvfactor, uv_flux[where(uv_wave/(1.0+z) gt 1300.0 and uv_wave/(1.0+z) lt 24500.0)]/(1.0+z), bbspec[where(fullwave gt 24500.0)]/factor ]

plot, bigwave, bigflux, xrange=[1000,30000]

fullflux=fullwave

for n=0,n_elements(fullflux)-1 do fullflux[n]=mean(bigflux[where(  abs(bigwave-fullwave[n]) le 10.0)  ])

templatespectrum=[ transpose(fullwave), transpose(fullflux) ]

stop
openw,lun2, templatefilename, /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UV and optical spectra are from HST  with a blackbody extension. '


for n=0,n_elements(fullflux)-1 do begin
	printf, lun2, templatespectrum[0,n], templatespectrum[1,n]
endfor


; close spectrum file
close, lun2
free_lun, lun2





print, 'final stop'
stop
end