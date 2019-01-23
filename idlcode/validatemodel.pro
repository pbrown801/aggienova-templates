pro validatemodel, SNname, z, referenceepoch, ebvmw, ebvhost

restore, filename=SNname+'_filtermags.sav' ;, SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray, bigmjdarray, bigmagarray, bigmagerrarray, explosiondate, explosiondateerr

n_filters=n_elements(filterarray)
vbandindex=5

if n_elements(filtercolor_array) lt 1 then filtercolor_array=make_array(n_elements(filterarray), value='black')


; templatefile='/Users/pbrown/Desktop/SN/SNANA/snsed/NON1A/SDSS-018892.SED'

templatefile='$SNFOLDER/localtemplates/ANT-'+SNname+'.20A.sed.restframe.dat'

readcol, templatefile, restphase, lambda_rest, f_lambda, /silent

epochlist= restphase[UNIQ(restphase, SORT(restphase))]

lum_dist=lumdist(z)
n_epochs=n_elements(epochlist)

if SNname eq 'SN2011e' then n_epochs=50

template_mag_array=fltarr(n_elements(filterarray), n_epochs-2)
templateabs_mag_array=fltarr(n_elements(filterarray), n_epochs-2)

;;; this was used to generate the aggienova templates in 2017   
;;;  distancefactor=(1.0+z)*(lum_dist/0.0000100)^2.0
distancefactor=(1.0+z)*(lum_dist/0.0000100)^2.0

for n=1, n_epochs-2 do begin
;for n=1, 50 do begin

	print, ' n', n

	spectrumwaverest=lambda_rest[where(restphase eq epochlist[n])]

	spectrumflux=f_lambda[where(restphase eq epochlist[n])] ;/distancefactor
	scaledspectrumflux=spectrumflux/distancefactor

	fm_unred, spectrumwaverest, scaledspectrumflux, -ebvhost, spectrumdehostred
	fm_unred, spectrumwaverest*(1.0+z[0]), spectrumdehostred, -ebvmw[0], spectrumdered

	originalspectrum=[transpose(spectrumwaverest),transpose(spectrumflux)]
	spectrum=[transpose(spectrumwaverest*(1.0+z)),transpose(spectrumdered)]
	pjb_uvotspec_all, spectrum, mag_array=mag_array

print, spectrum[0:1,0:1]

	for f=0, n_elements(filterarray)-1 do template_mag_array[f,n-1]=vegaphot(spectrum, filterarray[f])
	for f=0, n_elements(filterarray)-1 do templateabs_mag_array[f,n-1]=vegaphot(originalspectrum, filterarray[f])

endfor

;;;;;;;;;;;;;;;;;;;;;;;;;;;;  set up plots


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


;;;;;;;;;;;;;;;;;;;;;;;;;;;;


lightcurvefilename='ANT_'+SNname+'_validationplot.eps'

;;;; pick out arrays of detections




;;; only plot the x range corresponding to detections in at least one filter


maghigh=floor( max([ max(filtermagarray,/nan), max(template_mag_array,/nan)],/nan))+1.0
maglow=floor(  min([ min(filtermagarray,/nan), min(template_mag_array,/nan)],/nan))-1.0



mjdhighs=[max(filtermjdarray), epochlist[1:n_elements(epochlist)-2]+referenceepoch ]
mjdlows=[min(filtermjdarray), epochlist[1:n_elements(epochlist)-2]+referenceepoch ]


mjdhigh=floor(max(mjdhighs,/nan)/10.0)*10.0+10.0
mjdlow=floor(min(mjdlows,/nan)/10.0)*10.0

epochmark=floor(mjdlow/1000.0)*1000.0

legendxy=[mjdlow-epochmark+(mjdhigh-mjdlow)*0.8, (maghigh-(maghigh-maglow)*0.95)]
namexy=[mjdlow-epochmark+(mjdhigh-mjdlow)*0.5, (maghigh-(maghigh-maglow)*0.9)]



SET_PLOT, 'PS'

device, filename=lightcurvefilename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, bits_per_pixel=8, /color

plot, xdata,ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Modified Julian Date - '+string(uint(epochmark)),   ytitle='Vega Mags', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
xrange=[mjdlow-epochmark,mjdhigh-epochmark],yrange=[maghigh,maglow], ystyle=1, xstyle=1, $
;xrange=[0,80],yrange=[20,12], ystyle=1, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

;;;; the [0.0,0, reform()] stuff makes sure there is an array to plot even if there is only one data point

xyouts, mjdlow-epochmark+(mjdhigh-mjdlow)*0.5, (maghigh-(maghigh-maglow)*0.9), SNname, alignment=0.5

for f=0,n_elements(filterarray)-1 do 	cgoplot, (1.0+z)*epochlist[1:n_elements(epochlist)-1]+referenceepoch-epochmark, template_mag_array[f,*], color=filtercolor_array[f]

for f=0,n_elements(filterarray)-1 do 	cgoplot, filtermjdarray[f,*]-epochmark, filtermagarray[f,*], psym=4, color=filtercolor_array[f]

for f=0,n_elements(filterarray)-1 do 	cgoplot, bigmjdarray-epochmark, bigmagarray[f,*], psym=3, color=filtercolor_array[f]


device, /close
SET_PLOT, 'X'
;;;;;;;;;;;;;;;;;;;;;;
opencommand='open '+lightcurvefilename
spawn, opencommand






lightcurvefilename='ANT_'+SNname+'_templateabsmags.eps'

;;;; pick out arrays of detections




;;; only plot the x range corresponding to detections in at least one filter


maghigh=floor( max(templateabs_mag_array,/nan))+1.0
maglow=floor(  min(templateabs_mag_array,/nan))-1.0



mjdhighs=[epochlist[1:n_elements(epochlist)-2]+referenceepoch ]
mjdlows=[epochlist[1:n_elements(epochlist)-2]+referenceepoch ]


mjdhigh=floor(max(mjdhighs,/nan)/10.0)*10.0+10.0
mjdlow=floor(min(mjdlows,/nan)/10.0)*10.0

epochmark=floor(mjdlow/1000.0)*1000.0

legendxy=[mjdlow-epochmark+(mjdhigh-mjdlow)*0.8, (maghigh-(maghigh-maglow)*0.95)]
namexy=[mjdlow-epochmark+(mjdhigh-mjdlow)*0.5, (maghigh-(maghigh-maglow)*0.9)]


SET_PLOT, 'PS'

device, filename=lightcurvefilename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, bits_per_pixel=8, /color

plot, xdata,ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Modified Julian Date - '+string(uint(epochmark)),   ytitle='Vega Mags', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
xrange=[mjdlow-epochmark,mjdlow-epochmark+20.0],yrange=[maghigh,maglow], ystyle=1, xstyle=1, $
;xrange=[0,80],yrange=[20,12], ystyle=1, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

;;;; the [0.0,0, reform()] stuff makes sure there is an array to plot even if there is only one data point

xyouts, mjdlow-epochmark+(mjdhigh-mjdlow)*0.5, (maghigh-(maghigh-maglow)*0.9), SNname, alignment=0.5

for f=0,n_elements(filterarray)-1 do 	cgoplot, (1.0+z)*epochlist[1:n_elements(epochlist)-1]+referenceepoch-epochmark, templateabs_mag_array[f,*], color=filtercolor_array[f]


device, /close
SET_PLOT, 'X'
;;;;;;;;;;;;;;;;;;;;;;
opencommand='open '+lightcurvefilename
spawn, opencommand



;;;;;;;;;;;;;;;;;;;;;;;;;;;;

plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, yrange=[30,14]

for f=0,n_filters-1 do cgoplot, bigmjdarray, bigmagarray[f,*], psym=3, color=filtercolor_array[f]
for f=0,n_elements(filterarray)-1 do 	cgoplot, filtermjdarray[f,*], filtermagarray[f,*], psym=4, color=filtercolor_array[f]

for f=0,n_elements(filterarray)-1 do 	cgoplot, (1.0+z)*epochlist[1:n_elements(epochlist)-1]+referenceepoch, template_mag_array[f,*], color=filtercolor_array[f]

;;;  this is what is in the ps plot
plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, yrange=[30,14]
for f=0,n_elements(filterarray)-1 do 	cgoplot, (1.0+z)*epochlist[1:n_elements(epochlist)-1]+referenceepoch, template_mag_array[f,*], color='red'

for f=0,n_elements(filterarray)-1 do 	cgoplot, filtermjdarray[f,*], filtermagarray[f,*], psym=4,  color='blue'

for f=0,n_elements(filterarray)-1 do 	cgoplot, bigmjdarray, bigmagarray[f,*], psym=3, color='white'





print, 'final stop'
stop
end