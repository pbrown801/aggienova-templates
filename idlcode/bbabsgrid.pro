pro bbabsgrid, z, modelmags, n_bbs, temp_array, n_abs, abs_array, n_ebv, ebv_array

t_low=1000.0
t_high=25000.0

ebv_low=0.0
ebv_high=1.0

abs_low=-3.0
abs_high=3.0

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

; read in the absorption spectrum which is the ratio of 
; the Gaia16apd spectrum and a 17kK blackbody below 3000 Angstroms
readcol,"gaia16apd_absorption.dat", abslambda, absorptionspectrum

;  redshift the absorption spectrum into the observer frame 
;  and interpolate to the filter curves
abs_redlambda=interpol(absorptionspectrum, abslambda, lambda/(1.0+z))

n_filters=6

temp_array=fltarr(n_bbs)
abs_array=fltarr(n_abs)
ebv_array=fltarr(n_ebv)
modelmags=fltarr(n_bbs, n_abs, n_ebv, n_filters)
modelchisq=fltarr(n_bbs, n_abs, n_ebv)

for iindex=0,n_bbs-1 do begin
	

	; create a blackbody spectrum in the observer frame
	T=t_low+iindex*(t_high-t_low)/(n_bbs-1.0)
	temp_array[iindex]=T
	bbspec=1L*2.0*h*c^2.0/((lambda/(1.0+z))^5.0*(e^(h*c/((lambda/(1.0+z))*k*T))-1.0))

	for aindex=0, n_abs-1 do begin

		;; apply the absorption to the reddened spectrum  
		abs_factor=abs_low+aindex*(abs_high-abs_low)/(n_abs-1)
		abs_array[aindex]=abs_factor					
		absorbedspec=bbspec*abs_redlambda^abs_factor

		for eindex=0, n_ebv-1 do begin
			; apply reddening to the blackbody spectrum
			Ebv=ebv_low+eindex*(ebv_high-ebv_low)/(n_ebv-1.0)
			ebv_array[eindex]=Ebv
			Aarray=sne_mw_reddening((lambda/(1.0+z)),Ebv)
			specred=absorbedspec*10.0^(-Aarray/2.5)

			tempflux=specred

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


;			pjb_uvotspec_all, [transpose(lambda), transpose(tempflux)], mag_array=mag_array
;			print, mag_array[0:5]-[w2_spec,m2_spec,w1_spec,u_spec,b_spec,v_spec]
			modelmags[iindex,aindex,eindex,*]=[w2_spec,m2_spec,w1_spec,u_spec,b_spec,v_spec]

;			modelmags[iindex,aindex,eindex,*]=mag_array[0:5]

		endfor
	endfor
endfor


;print, 'final stop for bbabsgrid'
;stop
end
