pro callbbabsgrid

h = 1D*6.626E-27
c = 1D*2.998E18
hc = 1D*1.986E-8
e = 1D*2.71828
k = 1D*1.38E-16

;;Read in the filter Effective Area
readcol,"$SNSCRIPTS/V_UVOT.txt", lambda,V_EA,/silent
readcol,"$SNSCRIPTS/B_UVOT.txt", lambda,B_EA,/silent
readcol,"$SNSCRIPTS/U_UVOT.txt", lambda,U_EA,/silent
readcol,"$SNSCRIPTS/UVW1_2010.txt",   lambda,W1_EA,/silent
readcol,"$SNSCRIPTS/UVM2_2010.txt",   lambda,M2_EA,/silent
readcol,"$SNSCRIPTS/UVW2_2010.txt",   lambda,W2_EA,/silent

n_bbs=25
n_abs=31
n_filters=6
n_ebv=11

z=0.1
SNname='Gaia16apd'

referenceepoch=57505.3
lum_dist=lumdist(z)

pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat',   dt=dt

nfiltersinepoch=intarr(n_elements(dt.time_array))
filtercheck=intarr(n_elements(dt.time_array),6)
for n=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[n,f]=finite(dt.mag_array[f,n])
for n=0,n_elements(dt.time_array)-1 do nfiltersinepoch[n]=total(filtercheck[n,*]) 
all6=where(nfiltersinepoch eq 6)

earlymjds=[57510.0,57515.0,57520.0,57525.0]
;earlyvmags=[20.0]

n_earlymjds=n_elements(earlymjds)

earlymags=fltarr(6,n_earlymjds)
earlymagerrs=earlymags*0.0+0.1

;for e=0,n_earlymjds-1 do earlyvmags[e]=interpol([20.0,dt.mag_array[5,all6[0]]],[57510.0,dt.time_array[all6[0]]], earlymjds)
earlyvmags=interpol([20.0,dt.mag_array[5,all6[0]]],[57510.0,dt.time_array[all6[0]]], earlymjds)

;; extrapolate other filters assuming a constant color
for f=0,5 do earlymags[f,*]=earlyvmags+dt.mag_array[f,all6[0]]-dt.mag_array[5,all6[0]]
;;;;;;;

latemjds=[57600.0,57605,57610,57615,57620,57625,57630,57635,57640,57645,57650,57655,57660,57665,57670,57675,57680,57685,57690,57695,57700]
;earlyvmags=[20.0]

n_latemjds=n_elements(latemjds)

latemags=fltarr(6,n_latemjds)
latemagerrs=latemags*0.0+0.1

;for e=0,n_earlymjds-1 do earlyvmags[e]=interpol([20.0,dt.mag_array[5,all6[0]]],[57510.0,dt.time_array[all6[0]]], earlymjds)
latevmags=interpol([dt.mag_array[5,all6[n_elements(all6)-1]],20],[dt.time_array[all6[n_elements(all6)-1]],57690], latemjds)

;; extrapolate other filters assuming a constant color
for f=0,5 do latemags[f,*]=latevmags+dt.mag_array[f,all6[n_elements(all6)-1]]-dt.mag_array[5,all6[n_elements(all6)-1]]


; combine mag arrays

allmag_array   =[[earlymags],   [dt.mag_array[*,all6]],   [latemags]]
allmagerr_array=[[earlymagerrs],[dt.magerr_array[*,all6]],[latemagerrs]]
allmjds        =[earlymjds,      dt.time_array[all6],      latemjds]
totalepochs=n_elements(allmag_array[0,*])

;;; here comes the looping

allmodelmag_array =fltarr(6,totalepochs)
alltemps_array    =fltarr(totalepochs)
allabs_array      =fltarr(totalepochs)
allebv_array      =fltarr(totalepochs)
allchi_array      =fltarr(totalepochs)

; open data file for writing
openw,lun2, 'ANT-'+SNname+'.sed.restframe.dat', /get_lun

printf, lun2, '# based on '+SNname
printf, lun2, '# The UVOT photometry is fit to a blackbody '
printf, lun2, '# modified by an absorption spectrum based on Gaia16apd'

;; set up wavelength range for output
range=35000-900
fullwave=fltarr(range/10)
for f=0,n_elements(fullwave)-1 do fullwave[f]=900.0+f*10.0

readcol,"gaia16apd_absorption.dat", abslambda, absorptionspectrum

absfullwave=interpol(absorptionspectrum, abslambda, fullwave)

;;;;;;;;;  this computes a grid of magnitudes (arbitrary flux scale) 
;;;;;;;;;  for a range of blackbody temperatures, absorption strengths, 
;;;;;;;;;  and reddening
	
bbabsgrid, z, modelmags, n_bbs, temp_array, n_abs, abs_array, n_ebv, ebv_array

for nepochloop=0, totalepochs-1 do begin

	phase=allmjds[nepochloop]-referenceepoch
	print, "nepochloop: ", nepochloop, 'phase: ', phase
	mags=allmag_array[*,nepochloop]
	magerrs=allmagerr_array[*,nepochloop]

;;;;;;; this compares the observed colors at this epoch 
;;;;;;; with the array of models to find the best match in color
	
	colorchisquare=fltarr(n_bbs, n_abs, n_ebv)

	for i=0,n_bbs-1 do for eindex=0,n_ebv-1 do for a=0,n_abs-1 do colorchisquare[i,a,eindex]=total(  ((mags[0:4]-mags[5])-(modelmags[i,a,eindex,0:4]-modelmags[i,a,eindex,5]))^2.0/(magerrs[0:4]^2.0))

	minmodel=min(colorchisquare, location)
	print, "minimum chisquare ", minmodel
	ind = array_indices(colorchisquare, location)

	besttemp=temp_array[ind[0]]
	bestabs = abs_array[ind[1]]
	bestebv = ebv_array[ind[2]]

	print, besttemp, bestabs, bestebv

	alltemps_array[nepochloop]     =besttemp
	allabs_array[nepochloop]       =bestabs
	allebv_array[nepochloop]       =bestebv
	allchi_array[nepochloop]       =minmodel

;;;;; pick the best flux scaling by comparison of the observed v mag 
;;;;; and the model v mag with the best colors
	
	modelvmag=modelmags[ind[0],ind[1],ind[2],5]
	factor=2.512^(modelvmag-mags[5])
	magdif=	modelvmag-mags[5]

	allmodelmag_array[*,nepochloop]=modelmags[ind[0],ind[1],ind[2],*]-magdif

	plot, allmjds, allmag_array[5,0:nepochloop], yrange=[20,15]
	oplot, allmjds, allmodelmag_array[5,0:nepochloop], psym=4

	print, 'm2 -v color of model and observations and shifted dif: '
	print, modelmags[ind[0],ind[1],ind[2],1]-modelmags[ind[0],ind[1],ind[2],5], $
	mags[1]-mags[5], modelmags[ind[0],ind[1],ind[2],5]-mags[5]-magdif

	;rebuild spectrum in the rest frame for the full wavelength range

readcol,"gaia16apd_absorption.dat", abslambda, absorptionspectrum

absfullwave=interpol(absorptionspectrum, abslambda, fullwave)


	T=besttemp
	bbspec=1L*2.0*h*c^2.0/((fullwave)^5.0*(e^(h*c/((fullwave)*k*T))-1.0))
	Ebv=bestebv
	Aarray=sne_mw_reddening((fullwave),Ebv)
	absfactor=bestabs
	absorbedspec=bbspec*absfullwave^absfactor
	specred=absorbedspec*10.0^(-Aarray/2.5)
	
	modeledspec=specred*factor
	;; this will rescale the flux to 10 parsecs
	distancefactor=(1.0+z)*(lum_dist/10.0)^2.0

	pjb_uvotspec_all, [transpose(fullwave*(1.0+z)), transpose(modeledspec)], mag_array=mag_array

;;; check what went into bbabsgrid

; read in the absorption spectrum which is the ratio of 
; the Gaia16apd spectrum and a 17kK blackbody below 3000 Angstroms
readcol,"gaia16apd_absorption.dat", abslambda, absorptionspectrum

;  redshift the absorption spectrum into the observer frame 
;  and interpolate to the filter curves
abs_redlambda=interpol(absorptionspectrum, abslambda, lambda/(1.0+z))

	; create a blackbody spectrum in the observer frame
	T=besttemp
	bbspec=1L*2.0*h*c^2.0/((lambda/(1.0+z))^5.0*(e^(h*c/((lambda/(1.0+z))*k*T))-1.0))

		;; apply the absorption to the reddened spectrum  
		abs_factor=bestabs					
		absorbedspec=bbspec*abs_redlambda^abs_factor

			Ebv=bestebv
			Aarray=sne_mw_reddening((lambda/(1.0+z)),Ebv)
			specred=absorbedspec*10.0^(-Aarray/2.5)

			tempflux=specred*factor

			;;pass spectrum through effective area curves and convert to counts
			v_counts=V_EA*tempflux*(10*lambda/hc)
			b_counts=B_EA*tempflux*(10*lambda/hc)
			u_counts=U_EA*tempflux*(10*lambda/hc)
			w1_counts=W1_EA*tempflux*(10*lambda/hc)
			m2_counts=M2_EA*tempflux*(10*lambda/hc)
			w2_counts=W2_EA*tempflux*(10*lambda/hc)

			;;calculate a synthetic magnitude from the spectrum
			v_spec=-2.5*alog10(total(v_counts))+17.89
			b_spec=-2.5*alog10(total(b_counts))+19.11
			u_spec=-2.5*alog10(total(u_counts))+18.34
			w1_spec=-2.5*alog10(total(w1_counts))+17.44
			m2_spec=-2.5*alog10(total(m2_counts))+16.85
			w2_spec=-2.5*alog10(total(w2_counts))+17.38

;;;;;;;;;;;;;;;

	print, 'from bbabsgrid spectrum   ', [w2_spec,m2_spec,w1_spec,u_spec,b_spec,v_spec]
	print, 'mags from modeled spectrum', mag_array[0:5]
	print, 'model mags                ', transpose(modelmags[ind[0],ind[1],ind[2],*]-magdif)
	print, 'observations              ', mags

	for t=0,n_elements(fullwave)-1 do printf, lun2, phase/(1.0+z), fullwave[t],  distancefactor*modeledspec[t]

;	if nepochloop eq 17 then stop

endfor

; close spectrum file
close, lun2
free_lun, lun2


plot, allmjds, allmag_array[0,*], yrange=[20,15]

oplot, allmjds, allmodelmag_array[0,*], psym=4

plot, allmjds, allmag_array[1,*], yrange=[20,15]

oplot, allmjds, allmodelmag_array[1,*], psym=4


plot, allmjds, allmag_array[2,*], yrange=[20,15]

oplot, allmjds, allmodelmag_array[2,*], psym=4


plot, allmjds, allmag_array[3,*], yrange=[20,15]

oplot, allmjds, allmodelmag_array[3,*], psym=4


plot, allmjds, allmag_array[4,*], yrange=[20,15]

oplot, allmjds, allmodelmag_array[4,*], psym=4


plot, allmjds, allmag_array[5,*], yrange=[20,15]
oplot, allmjds, allmodelmag_array[5,*], psym=4


print, 'final stop for callbbabsgrid'
stop
end
