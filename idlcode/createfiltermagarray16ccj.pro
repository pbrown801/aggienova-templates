pro createfiltermagarray16ccj

SNname='SN2016ccj'
shortname='2016ccj'
filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']



n_filters=n_elements(filters)
vbandindex=5
w1bandindex=2

filterarray=filters
maxepochs=200

filtermjdarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagerrarray=make_array(n_filters, maxepochs, value=!Values.F_NAN)


;;;;;;;;;; now read in photometry data

;sn2016ccj_optical_lc.sav - photometric quantities;
;LCOGT Observations: 
;tb: restframe mjd relative to B maximum -57500
;mb: observed magnitude
;errb: errors in magnitude
;fit_tb: polynomial fit to the light curve (time)
;fit_mb: polynomial fit to the light curve (magnitude)

;tb  , mb  , errb  , fit_tb  , fit_mb , $
;tgp , mgp , errgp , fit_tgp , fit_mgp, $ 
;(tv), mv  , errv  , fit_tv  , fit_mv , $
;trp , mrp , errrp , fit_trp , fit_mrp, $
;tip , mip , errip , fit_tip , fit_mip, $ 

;for B, gp, V, rp, and ip band, respectively;
restore, '$DROPSN/SN2016ccj/yinew/new_sn2016ccj_optical_lc.sav'

;; Swift data
pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat', dt=dt

uvotmag_array=dt.mag_array
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


bgood=where(errb lt 0.11 and errb gt 0.001, bcount)

allbmjds=[transpose(dt.bb[0,where(finite(dt.bb[1,*]) eq 1)]), tb[bgood]+57500.0]
allbmags=[transpose(dt.bb[1,where(finite(dt.bb[1,*]) eq 1)]), mb[bgood]]
allbmagerrs=[transpose(dt.bb[2,where(finite(dt.bb[1,*]) eq 1)]), errb[bgood]]

border=sort(allbmjds)
for i=0,n_elements(border)-1 do filtermjdarray[4,i]=   allbmjds[border[i]]
for i=0,n_elements(border)-1 do filtermagarray[4,i]=   allbmags[border[i]]
for i=0,n_elements(border)-1 do filtermagerrarray[4,i]=allbmagerrs[border[i]]


vgood=where(errv lt 0.11 and errv gt 0.001, vcount)

allvmjds=[transpose(dt.vv[0,where(finite(dt.vv[1,*]) eq 1)]), tv[vgood]+57500.0]
allvmags=[transpose(dt.vv[1,where(finite(dt.vv[1,*]) eq 1)]), mv[vgood]]
allvmagerrs=[transpose(dt.vv[2,where(finite(dt.vv[1,*]) eq 1)]), errv[vgood]]

vorder=sort(allvmjds)
for i=0,n_elements(vorder)-1 do filtermjdarray[5,i]=   allvmjds[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagarray[5,i]=   allvmags[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagerrarray[5,i]=allvmagerrs[vorder[i]]

;;; v band index
vbandindex=5
w1bandindex=2


;;; shift in time is necessary to put time in MJD
;;; shift in mag is necessary to put in Vega system

rvegazeropoint=vegazeropoint(filters[6])
rabzeropoint=abzeropoint(filters[6])
ivegazeropoint=vegazeropoint(filters[6])
iabzeropoint=abzeropoint(filters[6])

rshift=rvegazeropoint-rabzeropoint
ishift=ivegazeropoint-iabzeropoint


rgood=where(errrp lt 0.11 and errrp gt 0.001, rcount)
rorder=sort(trp[rgood])
for i=0,rcount-1 do filtermjdarray[6,i]=   trp[rgood[rorder[i]]]+57500.0
for i=0,rcount-1 do filtermagarray[6,i]=   mrp[rgood[rorder[i]]]+rshift
for i=0,rcount-1 do filtermagerrarray[6,i]=   errrp[rgood[rorder[i]]]


igood=where(errip lt 0.11 and errip gt 0.001, icount)
iorder=sort(tip[igood])
for i=0,icount-1 do filtermjdarray[7,i]=   tip[igood[iorder[i]]]+57500.0
for i=0,icount-1 do filtermagarray[7,i]=   mip[igood[iorder[i]]]+ishift
for i=0,icount-1 do filtermagerrarray[7,i]=   errip[igood[iorder[i]]]



save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray, vbandindex, w1bandindex


print, 'final stop'
stop
end
