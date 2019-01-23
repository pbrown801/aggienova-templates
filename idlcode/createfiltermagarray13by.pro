pro createfiltermagarray13by, filterarray, filtermjdarray, filtermagarray, filtermagerrarray


SNname='SN2013by'

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']
filterarray=filters
n_filters=n_elements(filterarray)

maxepochs=200

filtermjdarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagerrarray=make_array(n_filters, maxepochs, value=!Values.F_NAN)

;;;;;;;;;; now read in photometry data

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
uvotmagerr_array=dt.mag_array
uvotmjd_array=dt.time_array


w2good=where(finite(dt.w2[1,*]) eq 1,w2count)

for i=0,w2count-1 do filtermjdarray[0,i]=   dt.w2[0,w2good[i]]
for i=0,w2count-1 do filtermagarray[0,i]=   dt.w2[1,w2good[i]]
for i=0,w2count-1 do filtermagerrarray[0,i]=   dt.w2[2,w2good[i]]

m2good=where(finite(dt.m2[1,*]) eq 1,m2count)

for i=0,m2count-1 do filtermjdarray[1,i]=   dt.m2[0,m2good[i]]
for i=0,m2count-1 do filtermagarray[1,i]=   dt.m2[1,m2good[i]]
for i=0,m2count-1 do filtermagerrarray[1,i]=   dt.m2[2,m2good[i]]

w1good=where(finite(dt.w1[1,*]) eq 1,w1count)

for i=0,w1count-1 do filtermjdarray[2,i]=   dt.w1[0,w1good[i]]
for i=0,w1count-1 do filtermagarray[2,i]=   dt.w1[1,w1good[i]]
for i=0,w1count-1 do filtermagerrarray[2,i]=   dt.w1[2,w1good[i]]

uugood=where(finite(dt.uu[1,*]) eq 1,uucount)

for i=0,uucount-1 do filtermjdarray[3,i]=   dt.uu[0,uugood[i]]
for i=0,uucount-1 do filtermagarray[3,i]=   dt.uu[1,uugood[i]]
for i=0,uucount-1 do filtermagerrarray[3,i]=   dt.uu[2,uugood[i]]



;readcol, 'SN2013by_ValentiPhot.dat', date, amp1, MJD, amp2, Mag, amp3,  MagErr, amp4,  filter,amp5,   instrument, amp6,  date2, amp7, MJD2, amp8, Mag2, amp9,  MagErr2, amp10,  filter2, amp11,   instrument2, slash, $
; format='(A, A, F, A, F, F, A, A, A, A, A, A, A, F, A, F, F, A, A, A, A, A)', /silent

nlines=197

JD=fltarr(nlines)
mag=fltarr(nlines)
magerr=fltarr(nlines)
filter=strarr(nlines)

JD2=fltarr(nlines)
mag2=fltarr(nlines)
magerr2=fltarr(nlines)
filter2=strarr(nlines)


openr, lun, 'SN2013by_ValentiPhot.dat', /get_lun
header = STRARR(2)
   READF, lun, header
p= ' '
for i=0, 196 do begin
	READF, lun, p
	split=strsplit(p, " ", /extract)

	JD[i]=split[2]
	mag[i]=split[4]
	magerr[i]=split[5]
	filter[i]=split[7]

	JD2[i]=split[13]
	mag2[i]=split[15]
	magerr2[i]=split[16]
	filter2[i]=split[18]

endfor
;stop
mjdall=[jd,jd2]-2400000.0
magall=[mag,mag2]
magerrall=[magerr,magerr2]
filterall=[filter,filter2]

vlines=where(filterall eq '$V$')
blines=where(filterall eq '$B$')
rlines=where(filterall eq '$r$')
ilines=where(filterall eq '$i$')


;;;;;;;;;;;;;;;




allbmjds=[transpose(dt.bb[0,where(finite(dt.bb[1,*]) eq 1)]), mjdall[blines]]
allbmags=[transpose(dt.bb[1,where(finite(dt.bb[1,*]) eq 1)]), magall[blines]]
allbmagerrs=[transpose(dt.bb[2,where(finite(dt.bb[1,*]) eq 1)]), magerrall[blines]]

border=sort(allbmjds)
for i=0,n_elements(border)-1 do filtermjdarray[4,i]=   allbmjds[border[i]]
for i=0,n_elements(border)-1 do filtermagarray[4,i]=   allbmags[border[i]]
for i=0,n_elements(border)-1 do filtermagerrarray[4,i]=allbmagerrs[border[i]]

allvmjds=[transpose(dt.vv[0,where(finite(dt.vv[1,*]) eq 1)]), mjdall[vlines]]
allvmags=[transpose(dt.vv[1,where(finite(dt.vv[1,*]) eq 1)]), magall[vlines]]
allvmagerrs=[transpose(dt.vv[2,where(finite(dt.vv[1,*]) eq 1)]), magerrall[vlines]]

vorder=sort(allvmjds)
for i=0,n_elements(vorder)-1 do filtermjdarray[5,i]=   allvmjds[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagarray[5,i]=   allvmags[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagerrarray[5,i]=allvmagerrs[vorder[i]]



rgood=where(finite(magall[rlines]) eq 1, rcount)
rorder=sort(mjdall(rlines))
for i=0,rcount-1 do filtermjdarray[6,i]=   mjdall[rlines[rgood[rorder[i]]]]
for i=0,rcount-1 do filtermagarray[6,i]=   magall[rlines[rgood[rorder[i]]]]
for i=0,rcount-1 do filtermagerrarray[6,i]=   magerrall[rlines[rgood[rorder[i]]]]


igood=where(finite(magall[ilines]) eq 1, icount)
iorder=sort(mjdall(ilines))
for i=0,icount-1 do filtermjdarray[7,i]=   mjdall[ilines[igood[iorder[i]]]]
for i=0,icount-1 do filtermagarray[7,i]=   magall[ilines[igood[iorder[i]]]]
for i=0,icount-1 do filtermagerrarray[7,i]=   magerrall[ilines[igood[iorder[i]]]]


;;;;;;;;;;;;;;;

save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray



;print, 'final stop'
;stop
end
