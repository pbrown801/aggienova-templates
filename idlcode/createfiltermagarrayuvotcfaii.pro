pro createfiltermagarrayuvotcfaii, SNname, filters

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']
n_filters=n_elements(filters)
;;; v band index
vbandindex=5
w1bandindex=2

filterarray=filters
n_filters=n_elements(filters)
maxepochs=200

filtermjdarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagarray=   make_array(n_filters, maxepochs, value=!Values.F_NAN)
filtermagerrarray=make_array(n_filters, maxepochs, value=!Values.F_NAN)


;;;;;;;;;; now read in photometry data

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



;;; read in CfA optical data

readcol, 'CFA_SNII_NATSYSTEM_LC.txt', cfaName, cfaBand, cfaMJD, cfaN, cfaNatMag,  cfadMag,   cfaCampaign,  cfaCamera, format='(A, A, F, I, F, F, A, A)', /silent

vlines=where(cfaName eq SNname and cfaband eq 'V')
blines=where(cfaName eq SNname and cfaband eq 'B')
rlines=where(cfaName eq SNname and cfaband eq "r'")
ilines=where(cfaName eq SNname and cfaband eq "i'")


allbmjds=[transpose(dt.bb[0,where(finite(dt.bb[1,*]) eq 1)]), cfamjd[blines[where(finite(cfanatmag[blines]) eq 1)]]]
allbmags=[transpose(dt.bb[1,where(finite(dt.bb[1,*]) eq 1)]), cfanatmag[blines[where(finite(cfanatmag[blines]) eq 1)]]]
allbmagerrs=[transpose(dt.bb[2,where(finite(dt.bb[1,*]) eq 1)]), cfadmag[blines[where(finite(cfanatmag[blines]) eq 1)]]]

border=sort(allbmjds)
for i=0,n_elements(border)-1 do filtermjdarray[4,i]=   allbmjds[border[i]]
for i=0,n_elements(border)-1 do filtermagarray[4,i]=   allbmags[border[i]]
for i=0,n_elements(border)-1 do filtermagerrarray[4,i]=allbmagerrs[border[i]]

allvmjds=[transpose(dt.vv[0,where(finite(dt.vv[1,*]) eq 1)]), cfamjd[vlines[where(finite(cfanatmag[vlines]) eq 1)]]]
allvmags=[transpose(dt.vv[1,where(finite(dt.vv[1,*]) eq 1)]), cfanatmag[vlines[where(finite(cfanatmag[vlines]) eq 1)]]]
allvmagerrs=[transpose(dt.vv[2,where(finite(dt.vv[1,*]) eq 1)]), cfadmag[vlines[where(finite(cfanatmag[vlines]) eq 1)]]]

vorder=sort(allvmjds)
for i=0,n_elements(vorder)-1 do filtermjdarray[5,i]=   allvmjds[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagarray[5,i]=   allvmags[vorder[i]]
for i=0,n_elements(vorder)-1 do filtermagerrarray[5,i]=allvmagerrs[vorder[i]]



rgood=where(finite(cfanatmag[rlines]) eq 1, rcount)
rorder=sort(cfamjd[rlines[rgood]])
for i=0,rcount-1 do filtermjdarray[6,i]=   cfamjd[rlines[rgood[rorder[i]]]]
for i=0,rcount-1 do filtermagarray[6,i]=   cfanatmag[rlines[rgood[rorder[i]]]]
for i=0,rcount-1 do filtermagerrarray[6,i]=   cfadmag[rlines[rgood[rorder[i]]]]


igood=where(finite(cfanatmag[ilines]) eq 1, icount)
iorder=sort(cfamjd[ilines[igood]])
for i=0,icount-1 do filtermjdarray[7,i]=   cfamjd[ilines[igood[iorder[i]]]]
for i=0,icount-1 do filtermagarray[7,i]=   cfanatmag[ilines[igood[iorder[i]]]]
for i=0,icount-1 do filtermagerrarray[7,i]=   cfadmag[ilines[igood[iorder[i]]]]

save, filename=SNname+'_filtermags.sav', SNname, filterarray, filtermjdarray, filtermagarray, filtermagerrarray, vbandindex, w1bandindex, n_filters


print, 'final stop'
stop
end
