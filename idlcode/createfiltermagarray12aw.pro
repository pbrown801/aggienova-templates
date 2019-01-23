pro createfiltermagarray12aw, filtermjdarray, filtermagarray, filtermagerrarray, filterarray

;;;; put all observed data together

; .run pjb_phot_array_B141
SNname='SN2012aw'

filterarray=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt', '$SNSCRIPTS/filters/J_2mass.txt', '$SNSCRIPTS/filters/H_2mass.txt', '$SNSCRIPTS/filters/Ks_2mass.txt']
n_filters=n_elements(filterarray)

maxepochs=200

filtermjdarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagerrarray=make_array(n_filters, maxepochs, value=!Values.F_NAN)

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt


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



;;; read in Dall'ora et al. 2014  optical data
; 2013-06-24 &  2456467.661 &  20.678 0.153 & $uw2$ &  $Swift$ & 2013-05-29 &  2456441.823 &  15.112 0.049 & $B$ &  $Swift$ \\ 

readcol, 'SN2012aw_UBVRI.dat', JDshort, phase, Umag, Umagerr, Bmag, Bmagerr, Vmag, Vmagerr, Rmag, Rmagerr, Imag, Imagerr,  /silent

Umag[where(umag eq 0)]=!Values.F_NAN
Umagerr[where(umagerr eq 0)]=!Values.F_NAN
Bmag[where(bmag eq 0)]=!Values.F_NAN
Bmagerr[where(bmagerr eq 0)]=!Values.F_NAN
Vmag[where(vmag eq 0)]=!Values.F_NAN
Vmagerr[where(vmagerr eq 0)]=!Values.F_NAN
Rmag[where(rmag eq 0)]=!Values.F_NAN
Rmagerr[where(rmagerr eq 0)]=!Values.F_NAN
imag[where(imag eq 0)]=!Values.F_NAN
imagerr[where(imagerr eq 0)]=!Values.F_NAN

mjd=jdshort-0.5



allbmjds=[transpose(dt.bb[0,where(finite(dt.bb[1,*]) eq 1)]), mjd[where(finite(bmag) eq 1)]]
allbmags=[transpose(dt.bb[1,where(finite(dt.bb[1,*]) eq 1)]), bmag[where(finite(bmag) eq 1)]]
allbmagerrs=[transpose(dt.bb[2,where(finite(dt.bb[1,*]) eq 1)]), bmagerr[where(finite(bmag) eq 1)]]

border=sort(allbmjds)
for i=0,n_elements(border)-1 do filtermjdarray[4,i]=   allbmjds[border[i]]
for i=0,n_elements(border)-1 do filtermagarray[4,i]=   allbmags[border[i]]
for i=0,n_elements(border)-1 do filtermagerrarray[4,i]=allbmagerrs[border[i]]

allvmjds=[transpose(dt.vv[0,where(finite(dt.vv[1,*]) eq 1)]), mjd[where(finite(Vmag) eq 1)]]
allvmags=[transpose(dt.vv[1,where(finite(dt.vv[1,*]) eq 1)]), Vmag[where(finite(Vmag) eq 1)]]
allvmagerrs=[transpose(dt.vv[2,where(finite(dt.vv[1,*]) eq 1)]), Vmagerr[where(finite(Vmag) eq 1)]]

vorder=sort(allvmjds)
for i=0,n_elements(vorder)-1 do filtermjdarray[5,i]=   allvmjds[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagarray[5,i]=   allvmags[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagerrarray[5,i]=allvmagerrs[vorder[i]]



rgood=where(finite(rmag) eq 1, rcount)
rorder=sort(mjd(rgood))
for i=0,rcount-1 do filtermjdarray[6,i]=   mjd[rgood[rorder[i]]]
for i=0,rcount-1 do filtermagarray[6,i]=   rmag[rgood[rorder[i]]]
for i=0,rcount-1 do filtermagerrarray[6,i]=   rmagerr[rgood[rorder[i]]]


igood=where(finite(imag) eq 1, icount)
iorder=sort(mjd(igood))
for i=0,icount-1 do filtermjdarray[7,i]=   mjd[igood[iorder[i]]]
for i=0,icount-1 do filtermagarray[7,i]=   imag[igood[iorder[i]]]
for i=0,icount-1 do filtermagerrarray[7,i]=   imagerr[igood[iorder[i]]]



readcol, 'SN2012aw_JHK.dat', irJDshort, irphase, Jmag, Jmagerr, Hmag, Hmagerr, Kmag, Kmagerr,  /silent

irmjd=irjdshort-0.5

jmag[where(jmag eq 0)]=!Values.F_NAN
jmagerr[where(jmagerr eq 0)]=!Values.F_NAN
hmag[where(hmag eq 0)]=!Values.F_NAN
hmagerr[where(hmagerr eq 0)]=!Values.F_NAN
kmag[where(kmag eq 0)]=!Values.F_NAN
kmagerr[where(kmagerr eq 0)]=!Values.F_NAN


jgood=where(finite(jmag) eq 1, jcount)
jorder=sort(mjd(jgood))
for i=0,jcount-1 do filtermjdarray[8,i]=   irmjd[rgood[jorder[i]]]
for i=0,jcount-1 do filtermagarray[8,i]=   jmag[rgood[jorder[i]]]
for i=0,jcount-1 do filtermagerrarray[8,i]=   jmagerr[jgood[jorder[i]]]


hgood=where(finite(hmag) eq 1, hcount)
horder=sort(mjd(hgood))
for i=0,hcount-1 do filtermjdarray[9,i]=   irmjd[hgood[horder[i]]]
for i=0,hcount-1 do filtermagarray[9,i]=   hmag[hgood[horder[i]]]
for i=0,hcount-1 do filtermagerrarray[9,i]=   hmagerr[hgood[horder[i]]]


kgood=where(finite(kmag) eq 1, kcount)
korder=sort(mjd(kgood))
for i=0,kcount-1 do filtermjdarray[10,i]=   irmjd[kgood[korder[i]]]
for i=0,kcount-1 do filtermagarray[10,i]=   kmag[kgood[korder[i]]]
for i=0,kcount-1 do filtermagerrarray[10,i]=   kmagerr[kgood[korder[i]]]

save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray



print, 'final stop'
stop
end
