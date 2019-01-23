pro createmagarrayfromosc, SNname, templatespectrum


restore, '$DROPSN/www/SwiftSN/host.sav'

snindex=where(host.SNname_array eq SNname)
dm=host.dm_best_array[snindex]
dmerr=host.dm_best_err_array[snindex]
z=host.redshift_array[snindex]
z=z[0]

ebvmw=host.AV_SCHLAFLY_array[snindex]/3.1
ebvmw=ebvmw[0]
ebvmwerr=ebvmw*0.1

ebvhost=0.0

if SNname eq 'SN2008ec' then ebvhost=0.18

;; event,time,magnitude,e_magnitude,upperlimit,band,instrument,telescope,source

datafile='data/'+SNname+'_osc.csv'
command1 = "  sed 's/,,/, ,/g ' "+datafile+" > new.csv"

command2 = "  sed s/g\'/sloang/g new.csv > "+datafile

;; awk -F'"' -v OFS='' '{ for (i=2; i<=NF; i+=2) gsub(",", "", $i) } 1' data/SN2008ec_osc.csv > test.csv

spawn, command1
spawn, command2


readcol, datafile, event,time,magnitude,e_magnitude,upperlimit,band,instrument,telescope,source, delimiter=',', format='(A,F, F, F, A, A, A, A)', /nan, comment='#'

w2range=where(band eq 'UVW2' and upperlimit eq 'F')
m2range=where(band eq 'UVM2' and upperlimit eq 'F')
w1range=where(band eq 'UVW1' and upperlimit eq 'F')
Urange=where(band eq 'U'  and upperlimit eq 'F'and instrument eq 'UVOT')
Brange=where(band eq 'B' and upperlimit eq 'F')
Vrange=where(band eq 'V' and upperlimit eq 'F')

johnsonurange=where(band eq 'U'  and upperlimit eq 'F'and instrument ne 'UVOT')
cousinsrrange=where(band eq 'R' or band eq 'Rc' and upperlimit eq 'F')
cousinsirange=where(band eq 'I' or band eq 'Ic' and upperlimit eq 'F')

sloanurange=where(band eq 'u' and upperlimit eq 'F')
sloangrange=where(band eq 'g' and upperlimit eq 'F')
sloanrrange=where(band eq 'r' and upperlimit eq 'F')
sloanirange=where(band eq 'i' and upperlimit eq 'F')
desyrange=where(band eq 'y' and upperlimit eq 'F')
deszrange=where(band eq 'z' and upperlimit eq 'F')

jrange=where(band eq 'J' and upperlimit eq 'F')
hrange=where(band eq 'H' and upperlimit eq 'F')
krange=where(band eq 'K' and upperlimit eq 'F')

filterkeys=['UVW2','UVM2','UVW1','U','B','V','U','R','I','u','g','r','i','y','z','J','H','K']


;;; '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_U.dat',
;;;  '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_u.dat',

possiblefilters=['$SNSCRIPTS/filters/UVW2_B11.txt', '$SNSCRIPTS/filters/UVM2_B11.txt', '$SNSCRIPTS/filters/UVW1_B11.txt', '$SNSCRIPTS/filters/U_P08.txt', '$SNSCRIPTS/filters/B_P08.txt', '$SNSCRIPTS/filters/V_P08.txt', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_U.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_R.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_I.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_u.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_g.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_r.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_i.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_y.dat', '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_z.dat', '$SNSCRIPTS/filters/J_2mass.txt', '$SNSCRIPTS/filters/H_2mass.txt','$SNSCRIPTS/filters/Ks_2mass.txt']

filtercheck=intarr(n_elements(possiblefilters))
filtercheckloop=intarr(n_elements(possiblefilters))

filters=['']
if n_elements(w2range) gt 1 then filters=filters+'$SNSCRIPTS/filters/UVW2_B11.txt'
if n_elements(m2range) gt 1 then filters=filters+'$SNSCRIPTS/filters/UVM2_B11.txt'
if n_elements(w1range) gt 1 then filters=filters+'$SNSCRIPTS/filters/UVW1_B11.txt'
if n_elements(Urange)  gt 1 then filters=filters+'$SNSCRIPTS/filters/U_P08.txt'
if n_elements(Brange)  gt 1 then filters=filters+'$SNSCRIPTS/filters/B_P08.txt'
if n_elements(Vrange)  gt 1 then filters=filters+'$SNSCRIPTS/filters/V_P08.txt'
if n_elements(johnsonurange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_U.dat'
if n_elements(cousinsrrange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_R.dat'
if n_elements(cousinsirange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_I.dat'
if n_elements(sloanurange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_u.dat'
if n_elements(sloangrange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_g.dat'
if n_elements(sloanrrange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_r.dat'
if n_elements(sloanirange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_i.dat'
if n_elements(desyrange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_y.dat'
if n_elements(deszrange) gt 1 then filters=filters+'/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/DES/20130322/20130322_z.dat'
if n_elements(jrange) gt 1 then filters=filters+'$SNSCRIPTS/filters/J_2mass.txt'
if n_elements(hrange) gt 1 then filters=filters+'$SNSCRIPTS/filters/H_2mass.txt'
if n_elements(krange) gt 1 then filters=filters+'$SNSCRIPTS/filters/Ks_2mass.txt'


if n_elements(w2range)       gt 1 then filtercheck[0]=1
if n_elements(m2range)       gt 1 then filtercheck[1]=1
if n_elements(w1range)       gt 1 then filtercheck[2]=1
if n_elements(Urange)        gt 1 then filtercheck[3]=1
if n_elements(Brange)        gt 1 then filtercheck[4]=1
if n_elements(Vrange)        gt 1 then filtercheck[5]=1
if n_elements(johnsonurange) gt 1 then filtercheck[6]=1
if n_elements(cousinsrrange) gt 1 then filtercheck[7]=1
if n_elements(cousinsirange) gt 1 then filtercheck[8]=1
if n_elements(sloanurange)   gt 1 then filtercheck[9]=1
if n_elements(sloangrange)   gt 1 then filtercheck[10]=1
if n_elements(sloanrrange)   gt 1 then filtercheck[11]=1
if n_elements(sloanirange)   gt 1 then filtercheck[12]=1
if n_elements(desyrange)     gt 1 then filtercheck[13]=1
if n_elements(deszrange)     gt 1 then filtercheck[14]=1
if n_elements(jrange)        gt 1 then filtercheck[15]=1
if n_elements(hrange)        gt 1 then filtercheck[16]=1
if n_elements(krange)        gt 1 then filtercheck[17]=1

vegacheck=[1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1]

n_filters=n_elements(possiblefilters)

filterarray=possiblefilters
maxepochs=200

if SNname eq 'SN2011fe' then maxepochs=500

filtermjdarray=    make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagarray=    make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagerrarray= make_array(n_filters, maxepochs, value=!Values.F_NAN)


;;;;;;;;;; now read in photometry data

if n_elements(w2range) gt 1 then filtermjdarray[0,0:n_elements(w2range)-1]=time[w2range] 


for f=0, n_elements(possiblefilters)-1 do begin

	range=where(band eq filterkeys[f] and upperlimit eq 'F')
	if possiblefilters[f] eq '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_R.dat' then range=where(band eq 'R' or band eq 'Rc'  and upperlimit eq 'F')
	if possiblefilters[f] eq '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_I.dat' then range=where(band eq 'I' or band eq 'Ic'  and upperlimit eq 'F')
	if possiblefilters[f] eq '$SNSCRIPTS/filters/U_P08.txt' then range=where(band eq 'U'  and upperlimit eq 'F'and instrument eq 'UVOT')
	if possiblefilters[f] eq '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_U.dat' then range=where(band eq 'U'  and upperlimit eq 'F'and instrument ne 'UVOT')

	if n_elements(range)       gt 1 then filtercheckloop[f]=1

	if n_elements(range) gt 1 then filtermjdarray[f,0:n_elements(range)-1]=time[range] 
	if n_elements(range) gt 1 then filtermagarray[f,0:n_elements(range)-1]=magnitude[range] 

	if possiblefilters[f] eq '/Users/pbrown/Desktop/Dropbox/SN/snscripts/filters/CFA/CFA3_Landolt/Bessell90_U.dat' and n_elements(range) gt 1 then filtermagarray[f,0:n_elements(range)-1]=magnitude[range]


	if n_elements(range) gt 1 then filtermagerrarray[f,0:n_elements(range)-1]=e_magnitude[range] 


endfor



save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray



n_filtersused=total(filtercheck)

usedfilters=where(filtercheck eq 1)
filtersused=where(filtercheck eq 1)


vbandindex=where(possiblefilters[usedfilters] eq '$SNSCRIPTS/filters/V_P08.txt')
w1bandindex=where(possiblefilters[usedfilters] eq '$SNSCRIPTS/filters/UVW1_B11.txt')
vbandindex=vbandindex[0]
w1bandindex=w1bandindex[0]



vmjds=where(finite(filtermjdarray[usedfilters[vbandindex],*]) eq 1)
bigMJDarray=filtermjdarray[usedfilters[vbandindex],vmjds]


;  this here needs to be trimmed so there aren't as many nearby points

n_epochs=n_elements(bigMJDarray)

bigmagarray=make_array(n_filtersused,n_epochs,value=!Values.F_NAN)
bigmagerrarray=make_array(n_filtersused,n_epochs,value=!Values.F_NAN)







;  first put in V data

bigmagarray[vbandindex,*]=[transpose(filtermagarray[usedfilters[vbandindex],where(finite(filtermjdarray[usedfilters[vbandindex],*]) eq 1)])]
bigmagerrarray[vbandindex,*]=[transpose(filtermagerrarray[usedfilters[vbandindex],where(finite(filtermjdarray[usedfilters[vbandindex],*]) eq 1)])]



;;;

for q=0, n_filtersused-1 do begin

f=usedfilters[q]

	min=min(filtermjdarray[f,*])
	max=max(filtermjdarray[f,*])
	within=where(bigMJDarray lt max and bigMJDarray gt min)
	present=where(finite(filtermagarray[f,*]) eq 1,npresent)
	for n=0,n_elements(within)-1 do bigmagarray[q,within[n]]=interpol(filtermagarray[f,present], filtermjdarray[f,present], bigMJDarray[within[n]])
	for n=0,n_elements(within)-1 do bigmagerrarray[q,within[n]]=interpol(filtermagerrarray[f,present], filtermjdarray[f,present], bigMJDarray[within[n]])

endfor

for f=0,n_filtersused-1 do oplot, bigmjdarray, bigmagarray[f,*]


;; I think this part is covered

;;;;;;; now loop through all filters to fill in missing blanks in the interior region
for q=0,n_filtersused-1 do begin

f=filtersused[q]

;print, 'filling in interior region for ', f
;stop
	present=where(finite(bigmagarray[q,*]) eq 1,presentcount)
	min=min(bigmjdarray[present])
	max=max(bigmjdarray[present])
	notpresentwithin=where(bigMJDarray lt max and bigMJDarray gt min and finite(bigmagarray[q,*]) eq 0, notpresentcount)
	if notpresentcount ne 0 then for n=0,n_elements(notpresentwithin)-1 do bigmagarray[q,notpresentwithin[n]]=interpol(bigmagarray[q,present], bigmjdarray[present], bigMJDarray[notpresentwithin[n]])
	if notpresentcount ne 0 then for n=0,n_elements(notpresentwithin)-1 do bigmagerrarray[q,notpresentwithin[n]]=interpol(bigmagerrarray[q,present], bigmjdarray[present], bigMJDarray[notpresentwithin[n]])

endfor

;print, 'after loop'
;stop

;;; extrapolate or interpolate missing values based on the color
;;; starting with UV filters matched to uvw1

;if w1bandindex eq 2 then begin
for f=0, w1bandindex-1 do begin

	color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )
	earlymissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 and bigmjdarray lt bigmjdarray[color[0]], earlymissingcount )
	latemissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0  and bigmjdarray gt bigmjdarray[color[0]], latemissingcount )

	;;; this extrapolates based on the last color

	if latemissingcount ne 0 then bigmagarray[f,latemissing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[w1bandindex, color[colorcount-1]]+ bigmagarray[w1bandindex,latemissing]
	if latemissingcount ne 0 then bigmagerrarray[f,latemissing] = 0.2

;;; this extrapolates to early times based on the first color

	if earlymissingcount ne 0 then bigmagarray[f,earlymissing] = bigmagarray[f,color[0]]-bigmagarray[w1bandindex,color[0]]+ bigmagarray[w1bandindex,earlymissing]
	if earlymissingcount ne 0 then bigmagerrarray[f,earlymissing] = 0.2

;stop
endfor
;endif

;;; then matching all filters to v based on color
for f=0, n_filtersused-1 do begin

	color  =where( finite(bigmagarray[f,*]) eq 1 and bigmagarray[f,*] ne 0.0 ,  colorcount )
	earlymissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0 and bigmjdarray lt bigmjdarray[color[0]], earlymissingcount )
	latemissing=where( finite(bigmagarray[f,*]) eq 0 or bigmagarray[f,*] eq 0.0  and bigmjdarray gt bigmjdarray[color[0]], latemissingcount )

	;if missingcount ne 0 then bigmagarray[f,missing] = interpol( bigmagarray[f,color]-bigmagarray[vbandindex,color], bigmjdarray[color], bigmjdarray[missing] )+bigmagarray[vbandindex,missing]

	;;; this extrapolates based on the last color

	if latemissingcount ne 0 then bigmagarray[f,latemissing] = bigmagarray[f,color[colorcount-1]]-bigmagarray[vbandindex, color[colorcount-1]]+ bigmagarray[vbandindex,latemissing]
	if latemissingcount ne 0 then bigmagerrarray[f,latemissing] = 0.2

;;; this extrapolates to early times based on the first color

	if earlymissingcount ne 0 then bigmagarray[f,earlymissing] = bigmagarray[f,color[0]]-bigmagarray[vbandindex,color[0]]+ bigmagarray[vbandindex,earlymissing]
	if earlymissingcount ne 0 then bigmagerrarray[f,earlymissing] = 0.2



	for n=0,n_filtersused-1 do oplot, bigmjdarray, bigmagarray[n,*]
print, 'in loop with filter ', f
;stop
endfor


plot, bigmjdarray, bigmagarray[vbandindex,*], psym=3, yrange=[25,15], charsize=2

for f=0,n_filtersused-1 do cgoplot, bigmjdarray, bigmagarray[f,*], color='white'
for f=0,n_elements(filterarray)-1 do 	cgoplot, filtermjdarray[f,*], filtermagarray[f,*], psym=4, color='blue'
filterarray=filterarray[usedfilters]

save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray, bigmjdarray, bigmagarray, bigmagerrarray, explosiondate, explosiondateerr, vbandindex, w1bandindex


referenceepoch=floor(min(bigmjdarray))


print, 'validatemodel ', SNname, z, referenceepoch, ebvmw, ebvhost
stop



mangleSNseries, SNname, z, referenceepoch, ebvmw, ebvhost, bigmjdarray, bigmagarray, bigmagerrarray, filterarray, templatespectrum
validatemodel, SNname, z, referenceepoch, ebvmw, ebvhost

print, 'final stop'
stop
end
