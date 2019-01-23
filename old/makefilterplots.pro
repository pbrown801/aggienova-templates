pro makefilterplots

spectrum16apd='spectra/Gaia16apd_uv.dat'
uvot_specphot, spectrum16apd, mags16apd, speccounts=counts16apd, countspectrum=countspectrum16apd, lambda=lambda
readcol,spectrum16apd,sp_wave16apd,sp_flux16apd,/silent

spectrum94i='spectra/SN1994I_UV.dat'
uvot_specphot, spectrum94i, mags94i, speccounts=counts94i, countspectrum=countspectrum94i, lambda=lambda
readcol,spectrum94i,sp_wave94i,sp_flux94i,/silent

spectrum11fe='spectra/SN2011fe_uv.dat'
uvot_specphot, spectrum11fe, mags11fe, speccounts=counts11fe, countspectrum=countspectrum11fe, lambda=lambda
readcol,spectrum11fe,sp_wave11fe,sp_flux11fe,/silent


spectrum16ccj='spectra/SN2016ccj_uv.dat'
uvot_specphot, spectrum16ccj, mags16ccj, speccounts=counts16ccj, countspectrum=countspectrum16ccj, lambda=lambda
readcol,spectrum16ccj,sp_wave16ccj,sp_flux16ccj,/silent


spectrum17erp='spectra/SN2017erp_hst_20170629.dat'
uvot_specphot, spectrum17erp, mags17erp, speccounts=counts17erp, countspectrum=countspectrum17erp, lambda=lambda
readcol,spectrum17erp,sp_wave17erp,sp_flux17erp,/silent

sp_wave17erp=sp_wave17erp[where(finite(sp_flux17erp) eq 1)]
sp_flux17erp=sp_flux17erp[where(finite(sp_flux17erp) eq 1)]
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;  two PLOT  ;;;;;;;;;;;;;;;;;;;;
;

nplots=2
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 8.8
wall = 0.03
margin=0.12
a = xsize/8.8 - (margin + wall)
b = a * 2d / (1 + sqrt(5))

ysize = (margin + nplots*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a
nxticks=11
nyticks=3

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize
xrange=[1600,6000]
yrange1=[0,4]
yrange2=[0,4]


figurename='filters_sne_aggienova.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,60], ytitle='Effective Area [cm^2]', ystyle=1, xrange=xrange, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues, xtickname=[' ', '2000', ' ',' ','3200',' ','4000',' ',' ','5200',' ','6000'] 
y=5-x


;;Read in the filter Effective Area curves
readcol,"filters/V_UVOT.txt",lambda,V_EA,/silent
readcol,"filters/B_UVOT.txt",lambda,B_EA,/silent
readcol,"filters/U_UVOT.txt",lambda,U_EA,/silent
readcol,"filters/UVW1_2010.txt",lambda,W1_EA,/silent
readcol,"filters/UVM2_2010.txt",lambda,M2_EA,/silent
readcol,"filters/UVW2_2010.txt",lambda,W2_EA,/silent
readcol,"filters/UVW1-rc.txt",lambda,W1rc_EA,/silent
readcol,"filters/UVW2-rc.txt",lambda,W2rc_EA,/silent

cgoplot, lambda, V_EA, color='dark green'
cgoplot, lambda, B_EA, color='blue'
cgoplot, lambda, U_EA, color='purple'
cgoplot, lambda, W1_EA, color='black'
cgoplot, lambda, M2_EA, color='maroon'
cgoplot, lambda, W2_EA, color='brown'



xyouts, 1700,40, 'uvw2', charsize=1.0
xyouts, 2100,30, 'uvm2', charsize=1.0
xyouts, 2400,40, 'uvw1', charsize=1.0
xyouts, 3300,55, 'u', charsize=1.0
xyouts, 4300,45, 'b', charsize=1.0
xyouts, 5400,35, 'v', charsize=1.0


x=1


plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle=xtitle6,   ytitle='log( flux ) + constant', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,4], ystyle=1, xrange=xrange, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, ytickv=ytickvalues , xtickname=replicate(' ',nxticks+1)



cgoplot, sp_wave11fe,alog10(sp_flux11fe/counts11fe[5]*10^16.0/1.1/2.5)+3, color='red', linestyle=2
cgoplot, sp_wave94i,alog10(sp_flux94i/counts94i[5]*10^16.0/1.1/2.5)+3, color='dark green', linestyle=1
cgoplot, sp_wave16apd,alog10(sp_flux16apd/counts16apd[5]*10^16.0/1.1/2.5)+3, color='blue', linestyle=0

al_legend, ['Gaia16apd -- SL','SN2011fe -- Ia','SN1994I -- Ic'], color=['blue','red','dark green'], linestyle=[0,2,1], pos=[3200,1.5], box=0



device, /close
SET_PLOT, 'X'
$open filters_sne_aggienova.eps 


nplots=1
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 8.8
wall = 0.03
margin=0.12
a = xsize/8.8 - (margin + wall)
b = a * 2d / (1 + sqrt(5))

ysize = (margin + nplots*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a
nxticks=11
nyticks=3

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize
xrange=[1600,6000]
yrange1=[0,4]
yrange2=[0,4]

figurename='filters_redshiftedspectrum.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,2], ytitle='log( flux ) + 16.2', yticks=2, ystyle=1, xrange=xrange, xstyle=1, $
xticks=23, xtickv=xtickvalues, ytickv=ytickvalues, xtickname=[' ', ' ', '2000', ' ',' ',' ',' ','3000',' ',' ',' ',' ','4000',' ',' ',' ',' ','5000',' ',' ',' ',' ','6000',' ']
y=5-x


;;Read in the filter Effective Area curves
readcol,"$SNSCRIPTS/V_UVOT.txt",lambda,V_EA,/silent

cgoplot, lambda, V_EA/20.0*1.2, color='dark green', thick=5

xyouts, 5400,35, 'v', charsize=1.0

cgoplot, sp_wave16apd,  alog10(sp_flux16apd)+16.2, color='blue', linestyle=0, thick=5

cgoplot, sp_wave16apd*1.3,  alog10(sp_flux16apd/9.0/1.3)+16.2, color='red', linestyle=2, thick=5

;al_legend, ['z=0.1','z=0.3'], color=['blue','red'], linestyle=[0,2], thick=[5,5], pos=[3500,1.9], box=0


xyouts, 3000, 1.75, 'Gaia16apd @ 1.5 billion light years'
xyouts, 2000, 1.0, '@ 5 billion light years'
xyouts, 5200, 0.5, 'v filter'


device, /close
SET_PLOT, 'X'
$open filters_redshiftedspectrum.eps 

uvirrange=[2000,50000]

figurename='redshiftedspectrum.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[-22,-14], ytitle='log( flux density ) ', yticks=2, ystyle=1, xrange=uvirrange, xstyle=1, $
xticks=xticks, xtickv=xtickvalues, ytickv=ytickvalues
;, xtickname=[' ', ' ', '2000', ' ',' ',' ',' ','3000',' ',' ',' ',' ','4000',' ',' ',' ',' ','5000',' ',' ',' ',' ','6000',' ']
y=5-x

;  originally at redshift of 0.1
hostz=0.1
hostdist=lumdist(hostz)
cgoplot, sp_wave16apd,  alog10(sp_flux16apd), color='blue', linestyle=0, thick=2


zlist=[0.2,0.5,1.0,2.0, 5.0, 10.0, 15.0, 20.0]

for i=0,n_elements(zlist)-1 do begin

z=zlist[i]
zdist=lumdist(z)
cgoplot, sp_wave16apd*(1.0+z)/(1.0+hostz),  alog10(sp_flux16apd/(1.0+z)*(1.0+hostz)*hostdist^2.0/zdist^2.0), color='red', thick=1

endfor

;xyouts, 3000, 1.75, 'Gaia16apd @ 1.5 billion light years'


device, /close
SET_PLOT, 'X'
$open redshiftedspectrum.eps 


figurename='redshiftedabspectrum.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[30,16], ytitle='AB mag', yticks=yticks, ystyle=1, xrange=uvirrange, xstyle=1, $
xticks=xticks, xtickv=xtickvalues, ytickv=ytickvalues
;, xtickname=[' ', ' ', '2000', ' ',' ',' ',' ','3000',' ',' ',' ',' ','4000',' ',' ',' ',' ','5000',' ',' ',' ',' ','6000',' ']
y=5-x

;m(AB) = -2.5 log(f_nu) - 48.60
;f_lambda*lambda^2/c
c = 1D*2.99792458E18 ; in angstroms per second
;  originally at redshift of 0.1
hostz=0.1
hostdist=lumdist(hostz)
cgoplot, sp_wave16apd,  -48.60 - 2.5*alog10(sp_flux16apd*sp_wave16apd^2.0/c), color='blue', linestyle=0, thick=2

zlist=[0.2,0.5,1.0,2.0, 5.0, 10.0, 15.0, 20.0]

for i=0,n_elements(zlist)-1 do begin

z=zlist[i]
zdist=lumdist(z)
cgoplot, sp_wave16apd*(1.0+z)/(1.0+hostz),   -48.60 - 2.5*alog10(sp_flux16apd*(sp_wave16apd*(1.0+z)/(1.0+hostz))^2.0/c/(1.0+z)*(1.0+hostz)*hostdist^2.0/zdist^2.0), color='red', thick=1

endfor


cgoplot, [17000,22000], [29,29]

xyouts, 17000, 29.7, 'JWST F200W'


cgoplot, [38000,50000], [27.8,27.8]

xyouts, 38000, 29, 'JWST F444W'


device, /close
SET_PLOT, 'X'
$open redshiftedabspectrum.eps 


uvirrange=[2000,50000]

figurename='spectrumcomparison16ccj11fe.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

;  spectra/SN2016ccj_uv.dat
hostz=0.0415
hostdist=lumdist(hostz)
x=0
plot, sp_wave16ccj/(1.0+hostz),sp_flux16ccj*hostdist^2.0, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,6], ytitle='Flux density x 10^10', yticks=yticks, ystyle=1, xrange=[1000,6000], xstyle=1, $
xticks=xticks, xtickv=xtickvalues, ytickv=ytickvalues
;, xtickname=[' ', ' ', '2000', ' ',' ',' ',' ','3000',' ',' ',' ',' ','4000',' ',' ',' ',' ','5000',' ',' ',' ',' ','6000',' ']
y=5-x

;;;;; original version divided by distance instead of multiplying.


cgoplot, sp_wave16ccj[where(finite(sp_flux16ccj) eq 1)]/(1.0+hostz),sp_flux16ccj[where(finite(sp_flux16ccj) eq 1)]*hostdist^2.0*10.0e10, color='blue', linestyle=0, thick=2

z_11fe=0.000804
distance_11fe=6.7
dist_11fe=6.7

cgoplot, sp_wave11fe/(1.0+z_11fe),sp_flux11fe*distance_11fe^2.0*10.0e10, color='red', linestyle=0, thick=2

xyouts, 4000, 5.5, 'SN2016ccj near peak', color='blue'

xyouts, 4000, 0.8, 'SN2011fe near peak', color='red'




device, /close
SET_PLOT, 'X'
$open spectrumcomparison16ccj11fe.eps 



figurename='SNeIa_GMT.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[26,16], ytitle='AB mag', yticks=yticks, ystyle=1, xrange=[2000,10000], xstyle=1, $
xticks=xticks, xtickv=xtickvalues, ytickv=ytickvalues
;, xtickname=[' ', ' ', '2000', ' ',' ',' ',' ','3000',' ',' ',' ',' ','4000',' ',' ',' ',' ','5000',' ',' ',' ',' ','6000',' ']
y=5-x

;m(AB) = -2.5 log(f_nu) - 48.60
;f_lambda*lambda^2/c
c = 1D*2.99792458E18 ; in angstroms per second

z_16ccj=0.041
dist_16ccj=lumdist(z_16ccj)

z_11fe=0.000804
dist_11fe=6.7

z_17erp=0.006174
dist_17erp=28.8

;cgoplot, sp_wave16ccj/(1.0+z_16ccj),  -48.60 - 2.5*alog10(sp_flux16ccj*sp_wave16ccj^2.0/c), color='purple', linestyle=0, thick=2

;cgoplot, sp_wave11fe/(1.0+z_11fe),  -48.60 - 2.5*alog10(sp_flux11fe*sp_wave11fe^2.0/c), color='blue', linestyle=0, thick=2

;cgoplot, sp_wave17erp/(1.0+z_17erp),  -48.60 - 2.5*alog10(sp_flux17erp*sp_wave17erp^2.0/c), color='red', linestyle=0, thick=2

xyouts, 6000, 18, 'SN2016ccj z=0.1'
xyouts, 8000, 19, 'SN2011fe'
xyouts, 6000, 20.5, 'SN2017erp'

xyouts, 8500, 21.5, 'z=0.4'

xyouts, 9000, 25.8, 'z=1'

xyouts, 2300, 17, 'Type Ia Supernovae', charsize=1.5
;xyouts, 25000, 18, 'Supernovae'


zlist=[0.1, 0.4, 1.0]

for i=0,n_elements(zlist)-1 do begin

z=zlist[i]
zdist=lumdist(z)
cgoplot, sp_wave16ccj*(1.0+z)/(1.0+z_16ccj),   -48.60 - 2.5*alog10(sp_flux16ccj*(sp_wave16ccj*(1.0+z)/(1.0+z_16ccj))^2.0/c/(1.0+z)*(1.0+z_16ccj)*dist_16ccj^2.0/zdist^2.0), color='purple', thick=1

cgoplot, sp_wave11fe*(1.0+z)/(1.0+z_11fe),   -48.60 - 2.5*alog10(sp_flux11fe*(sp_wave11fe*(1.0+z)/(1.0+z_11fe))^2.0/c/(1.0+z)*(1.0+z_11fe)*dist_11fe^2.0/zdist^2.0), linestyle=2, color='blue', thick=1

cgoplot, sp_wave17erp*(1.0+z)/(1.0+z_17erp),   -48.60 - 2.5*alog10(sp_flux17erp*(sp_wave17erp*(1.0+z)/(1.0+z_17erp))^2.0/c/(1.0+z)*(1.0+z_17erp)*dist_17erp^2.0/zdist^2.0), color='red', thick=1


endfor



device, /close
SET_PLOT, 'X'
$open SNeIa_GMT.eps 

figurename='Gaia16apd_GMT.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

x=0
plot, xrange, yrange1, /nodata, /noerase, $
position=[x1,y1+(x)*b*8.8/ysize,x2,y1+(x+1)*b*8.8/ysize], $
xtitle='Wavelength [Angstroms]', charsize=1.0,  $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[26,15], ytitle='AB mag', yticks=yticks, ystyle=1, xrange=[2000,10000], xstyle=1, $
xticks=xticks, xtickv=xtickvalues, ytickv=ytickvalues
;, xtickname=[' ', ' ', '2000', ' ',' ',' ',' ','3000',' ',' ',' ',' ','4000',' ',' ',' ',' ','5000',' ',' ',' ',' ','6000',' ']
y=5-x

;m(AB) = -2.5 log(f_nu) - 48.60
;f_lambda*lambda^2/c
c = 1D*2.99792458E18 ; in angstroms per second
;  originally at redshift of 0.1
hostz=0.1
hostdist=lumdist(hostz)
cgoplot, sp_wave16apd,  -48.60 - 2.5*alog10(sp_flux16apd*sp_wave16apd^2.0/c), color='blue', linestyle=0, thick=2

zlist=[0.2,0.5,1.0,2.0,3.0]

for i=0,n_elements(zlist)-1 do begin

z=zlist[i]
zdist=lumdist(z)
cgoplot, sp_wave16apd*(1.0+z)/(1.0+hostz),   -48.60 - 2.5*alog10(sp_flux16apd*(sp_wave16apd*(1.0+z)/(1.0+hostz))^2.0/c/(1.0+z)*(1.0+hostz)*hostdist^2.0/zdist^2.0), color='red', thick=1

endfor

xyouts, 5500, 16.8, 'z = 0.1'
xyouts, 6000, 18.5, '0.2'
xyouts, 7000, 20.5, '0.5'
xyouts, 7500, 21.7, '1'
xyouts, 8000, 23, '2'
xyouts, 9000, 25.2, 'z = 3'

xyouts, 2300, 16, 'Superluminous Supernova Gaia16apd', charsize=1.3

device, /close
SET_PLOT, 'X'
$open Gaia16apd_GMT.eps 



print, 'final stop'
stop
end
