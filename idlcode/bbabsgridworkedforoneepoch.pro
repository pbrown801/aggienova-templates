pro bbabsgrid

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

readcol,"gaia16apd_absorption.dat", abslambda, absorptionspectrum

abs_lambda=interpol(absorptionspectrum, abslambda, lambda)

n_bbs=21
n_abs=11
n_filters=6
n_ebv=11

temp_array=fltarr(n_bbs)
abs_array=fltarr(n_abs)
ebv_array=fltarr(n_ebv)
modelmags=fltarr(n_bbs, n_abs, n_ebv, n_filters)
modelchisq=fltarr(n_bbs, n_abs, n_ebv)
t_low=5000.0
t_high=25000

ebv_low=0.0
ebv_high=0.5

abs_low=0.2
abs_high=3

for iindex=0,n_bbs-1 do begin
	
	T=t_low+iindex*(t_high-t_low)/(n_bbs-1.0)
	temp_array[iindex]=T
	bbspec=1L*2.0*h*c^2/(lambda^5*(e^(h*c/(lambda*k*T))-1.0))

	for eindex=0, n_ebv-1 do begin
		Ebv=ebv_low+eindex*(ebv_high-ebv_low)/(n_ebv-1.0)
		ebv_array[eindex]=Ebv
		Aarray=sne_mw_reddening(lambda,Ebv)
		specred=bbspec*10^(-Aarray/2.5)

		for aindex=0, n_abs-1 do begin

			abs_factor=abs_low+aindex*(abs_high-abs_low)/(n_abs-1)
			abs_array[aindex]=abs_factor
			absorbedspec=specred*abs_lambda^abs_factor
			
			tempflux=absorbedspec
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
			w1_spec=-2.5*alog10(total(w1_counts))+17.49
			m2_spec=-2.5*alog10(total(m2_counts))+16.82
			w2_spec=-2.5*alog10(total(w2_counts))+17.35

			modelmags[iindex,aindex,eindex,*]=[w2_spec,m2_spec,w1_spec,u_spec,b_spec,v_spec]

			
		endfor
	endfor
endfor

plot, modelmags[5,*,0,1]-modelmags[5,*,0,3], modelmags[5,*,0,3]-modelmags[5,*,0,5], psym=3

for i=0,n_bbs-1 do oplot, modelmags[i,*,0,1]-modelmags[i,*,0,3], modelmags[i,*,0,3]-modelmags[i,*,0,5], psym=3





plot, modelmags[*,5,0,1]-modelmags[*,5,0,3], modelmags[*,5,0,3]-modelmags[*,5,0,5], psym=4

for a=0,n_abs-1 do oplot, modelmags[*,a,0,1]-modelmags[*,a,0,3], modelmags[*,a,0,3]-modelmags[*,a,0,5], psym=4


                    plot, temp_array, modelmags[*,10,0,1]-modelmags[*,10,0,5], psym=4

for a=0,n_abs-1 do oplot, temp_array, modelmags[*,a,0,1]-modelmags[*,a,0,5], psym=4

plot, abs_array, modelmags[5,*,0,1]-modelmags[5,*,0,3], psym=4

for i=0,n_bbs-1 do oplot, abs_array, modelmags[i,*,0,1]-modelmags[i,*,0,3], psym=4



plot, ebv_array, modelmags[5,5,*,1]-modelmags[5,5,*,3], psym=4

for i=0,n_bbs-1 do oplot, ebv_array, modelmags[i,5,*,1]-modelmags[i,5,*,3], psym=4


plot, ebv_array, modelmags[5,5,*,1]-modelmags[5,5,*,3], psym=4, yrange=[-3,5]

for i=0,n_abs-1 do for b=0,n_bbs-1 do  oplot, ebv_array, modelmags[b,i,*,1]-modelmags[b,i,*,5], psym=4

SNname='Gaia16apd'
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat',   dt=dt

oplot, [0,0.5], [max(dt.mag_array[1,*]-dt.mag_array[5,*]),max(dt.mag_array[1,*]-dt.mag_array[5,*])]

oplot, [0,0.5], [min(dt.mag_array[1,*]-dt.mag_array[5,*]),min(dt.mag_array[1,*]-dt.mag_array[5,*])]




plot, temp_array, modelmags[*,10,0,1]-modelmags[*,10,0,5], psym=4, yrange=[-3,5]

for eindex=0,n_ebv-1 do for a=0,n_abs-1 do oplot, temp_array, modelmags[*,a,eindex,1]-modelmags[*,a,eindex,5], psym=4


oplot, [t_low,t_high], [max(dt.mag_array[1,*]-dt.mag_array[5,*]),max(dt.mag_array[1,*]-dt.mag_array[5,*])]

oplot, [t_low,t_high], [min(dt.mag_array[1,*]-dt.mag_array[5,*]),min(dt.mag_array[1,*]-dt.mag_array[5,*])]


;;;;;;;;;


plot, abs_array, modelmags[5,*,0,1]-modelmags[5,*,0,5], psym=4, yrange=[-3,5]

for i=0,n_bbs-1 do for eindex=0,n_ebv-1 do oplot, abs_array, modelmags[i,*,eindex,1]-modelmags[i,*,eindex,5], psym=4

oplot, [abs_low,abs_high], [max(dt.mag_array[1,*]-dt.mag_array[5,*]),max(dt.mag_array[1,*]-dt.mag_array[5,*])]

oplot, [abs_low,abs_high], [min(dt.mag_array[1,*]-dt.mag_array[5,*]),min(dt.mag_array[1,*]-dt.mag_array[5,*])]


nfiltersinepoch=intarr(n_elements(dt.time_array))
filtercheck=intarr(n_elements(dt.time_array),6)
for n=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[n,f]=finite(dt.mag_array[f,n])
for n=0,n_elements(dt.time_array)-1 do nfiltersinepoch[n]=total(filtercheck[n,*]) 
all6=where(nfiltersinepoch eq 6)

mags=dt.mag_array[*,all6[0]]
magerrs=dt.magerr_array[*,all6[0]]


colorchisquare=fltarr(n_bbs, n_abs, n_ebv)

for i=0,n_bbs-1 do for eindex=0,n_ebv-1 do for a=0,n_abs-1 do colorchisquare[i,a,eindex]=total(  ((mags[0:4]-mags[5])-(modelmags[i,a,eindex,0:4]-modelmags[i,a,eindex,5]))^2.0/(magerrs[0:4]^2.0))

minmodel=min(colorchisquare, location)
ind = array_indices(colorchisquare, location)

besttemp=temp_array[ind[0]]
bestabs=abs_array[ind[1]]
bestebv=ebv_array[ind[2]]

print, besttemp, bestabs, bestebv


print, modelmags(ind[0],ind[1],ind[2],*)
print, mags


print, 'final stop'
stop
end
