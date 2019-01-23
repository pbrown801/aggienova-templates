pro validatemodel ;, SNname, z, templatefile

; templatefile='/Users/pbrown/Desktop/SN/SNANA/snsed/NON1A/SDSS-018892.SED'

templatefile='ANT-Gaia16apd.sed.restframe.dat'

readcol, templatefile, restphase, lambda_rest, f_lambda, /silent

referenceepoch=57505.3

epochlist= restphase[UNIQ(restphase, SORT(restphase))]
z=0.1
SNname='Gaia16apd'
;
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat',   dt=dt

lum_dist=lumdist(z)
n_epochs=n_elements(epochlist)

template_mag_array=fltarr(6, n_epochs)

distancefactor=(1.0+z)*(lum_dist/10.0)^2.0

for n=0, n_epochs-1 do begin

	spectrum=[transpose(lambda_rest[where(phase eq epochlist[n])]*(1.0+z)), transpose( f_lambda[where(phase eq epochlist[n])]/distancefactor)]
;print, spectrum
	pjb_uvotspec_all, spectrum, mag_array=mag_array

	template_mag_array[*,n]=mag_array[0:5]

endfor


;;;;;;;;;;;;;;;;;;;;;;;;;;;;


lightcurvefilename='ANT_'+SNname+'_validationplot.eps'

;;;; pick out arrays of detections


goodw2=where(finite(dt.w2[1,*]) eq 1)
goodm2=where(finite(dt.m2[1,*]) eq 1)
goodw1=where(finite(dt.w1[1,*]) eq 1)
gooduu=where(finite(dt.uu[1,*]) eq 1)
goodbb=where(finite(dt.bb[1,*]) eq 1)
goodvv=where(finite(dt.vv[1,*]) eq 1)


;;; only plot the x range corresponding to detections in at least one filter


maghigh=floor( max([ max(dt.mag_array,/nan), max(template_mag_array,/nan)],/nan))+1.0
maglow=floor(  min([ min(dt.mag_array,/nan), min(template_mag_array,/nan)],/nan))-1.0



mjdhighs=[max(dt.w2[0,where(finite(dt.w2[1,*]) eq 1)],/nan),max(dt.m2[0,where(finite(dt.m2[1,*]) eq 1)],/nan),max(dt.w1[0,where(finite(dt.w1[1,*]) eq 1)],/nan),max(dt.uu[0,where(finite(dt.uu[1,*]) eq 1)],/nan),max(dt.bb[0,where(finite(dt.bb[1,*]) eq 1)],/nan),max(dt.vv[0,where(finite(dt.vv[1,*]) eq 1)],/nan), epochlist+referenceepoch  ]
mjdlows=[min(dt.w2[0,where(finite(dt.w2[1,*]) eq 1)],/nan),min(dt.m2[0,where(finite(dt.m2[1,*]) eq 1)],/nan),min(dt.w1[0,where(finite(dt.w1[1,*]) eq 1)],/nan),min(dt.uu[0,where(finite(dt.uu[1,*]) eq 1)],/nan),min(dt.bb[0,where(finite(dt.bb[1,*]) eq 1)],/nan),min(dt.vv[0,where(finite(dt.vv[1,*]) eq 1)],/nan), epochlist+referenceepoch ]


mjdhigh=floor(max(mjdhighs,/nan)/10.0)*10.0+10.0
mjdlow=floor(min(mjdlows,/nan)/10.0)*10.0

epochmark=floor(mjdlow/1000.0)*1000.0

legendxy=[mjdlow-epochmark+(mjdhigh-mjdlow)*0.8, (maghigh-(maghigh-maglow)*0.95)]
namexy=[mjdlow-epochmark+(mjdhigh-mjdlow)*0.5, (maghigh-(maghigh-maglow)*0.9)]


w2symbol=34
m2symbol=45
w1symbol=2
uusymbol=4
bbsymbol=6
vvsymbol=9
;;;;;;;
size=1
normal=1
small=0.5

; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
xsize = 8.8
wall = 0.03
margin=0.16
a = xsize/8.8 - (margin + wall)
b = a * 2d / (1 + sqrt(5))

ysize = (margin + b + wall)*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize
y3 = y2 + wall*8.8/ysize
y4 = y3 + b*8.8/ysize
yc = y4 + wall*8.8/ysize
fontsize=14

xdata=[1,2,3,4]
ydata=[1,2,3,4]
Bpeaktime=dt.time_array[ where(dt.mag_array[4,*] eq min(dt.mag_array[4,*], /nan) ) ]


SET_PLOT, 'PS'

device, filename=lightcurvefilename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, bits_per_pixel=8, /color

plot, xdata,ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Modified Julian Date - '+string(uint(epochmark)),   ytitle='UVOT Vega Mags', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
xrange=[mjdlow-epochmark,mjdhigh-epochmark],yrange=[maghigh,maglow], ystyle=1, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues


;;;; the [0.0,0, reform()] stuff makes sure there is an array to plot even if there is only one data point

if goodw2[0] ne -1 then oploterror, [0.0,0, reform(dt.w2[0,goodw2]-epochmark)], [!values.f_nan,!values.f_nan, reform(dt.w2[1,goodw2])], [0.0,0, reform(dt.w2[2,goodw2])], psym=cgsymcat(w2symbol), color=cgcolor('black'), errcolor=cgcolor('black'), symsize=normal
if goodm2[0] ne -1 then oploterror, [0.0,0, reform(dt.m2[0,goodm2]-epochmark)], [!values.f_nan,!values.f_nan, reform(dt.m2[1,goodm2])], [0.0,0, reform(dt.m2[2,goodm2])], psym=cgsymcat(m2symbol), color=cgcolor('red'), errcolor=cgcolor('red'), symsize=normal
if goodw1[0] ne -1 then oploterror, [0.0,0, reform(dt.w1[0,goodw1]-epochmark)], [!values.f_nan,!values.f_nan, reform(dt.w1[1,goodw1])], [0.0,0, reform(dt.w1[2,goodw1])], psym=cgsymcat(w1symbol), color=cgcolor('maroon'), errcolor=cgcolor('maroon'), symsize=normal
if gooduu[0] ne -1 then oploterror, [0.0,0, reform(dt.uu[0,gooduu]-epochmark)], [!values.f_nan,!values.f_nan, reform(dt.uu[1,gooduu])], [0.0,0, reform(dt.uu[2,gooduu])], psym=cgsymcat(uusymbol), color=cgcolor('purple'), errcolor=cgcolor('purple'), symsize=normal
if goodbb[0] ne -1 then oploterror, [0.0,0, reform(dt.bb[0,goodbb]-epochmark)], [!values.f_nan,!values.f_nan, reform(dt.bb[1,goodbb])], [0.0,0, reform(dt.bb[2,goodbb])], psym=cgsymcat(bbsymbol), color=cgcolor('blue'), errcolor=cgcolor('blue'), symsize=normal
if goodvv[0] ne -1 then oploterror, [0.0,0, reform(dt.vv[0,goodvv]-epochmark)], [!values.f_nan,!values.f_nan, reform(dt.vv[1,goodvv])], [0.0,0, reform(dt.vv[2,goodvv])], psym=cgsymcat(vvsymbol), color=cgcolor('dark green'), errcolor=cgcolor('dark green'), symsize=normal

al_legend, ['vv','bb','uu','w1','m2','w2'], color=[cgcolor('dark green'), cgcolor('blue'),cgcolor('purple') ,cgcolor('maroon') , cgcolor('red'), cgcolor('black') ], psym=[vvsymbol, bbsymbol, uusymbol, w1symbol,m2symbol,w2symbol ], symsize=[size,size,size,size,size,size], position=legendxy, box=0, charsize=0.7


xyouts, mjdlow-epochmark+(mjdhigh-mjdlow)*0.5, (maghigh-(maghigh-maglow)*0.9), SNname, alignment=0.5



oplot, (1.0+z)*epochlist+referenceepoch-epochmark, template_mag_array[0,*], color=cgcolor('black')
oplot, (1.0+z)*epochlist+referenceepoch-epochmark, template_mag_array[1,*], color=cgcolor('red')
oplot, (1.0+z)*epochlist+referenceepoch-epochmark, template_mag_array[2,*], color=cgcolor('maroon')
oplot, (1.0+z)*epochlist+referenceepoch-epochmark, template_mag_array[3,*], color=cgcolor('purple')
oplot, (1.0+z)*epochlist+referenceepoch-epochmark, template_mag_array[4,*], color=cgcolor('blue')
oplot, (1.0+z)*epochlist+referenceepoch-epochmark, template_mag_array[5,*], color=cgcolor('dark green')

device, /close
SET_PLOT, 'X'
;;;;;;;;;;;;;;;;;;;;;;
opencommand='open '+lightcurvefilename
spawn, opencommand
;;;;;;;;;;;;;;;;;;;;;;;;;;;;

print, 'final stop'
stop
end