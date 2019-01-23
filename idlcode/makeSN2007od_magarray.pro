pro makeSN2007od_magarray


createfiltermagarrayuvotcfaii, 'SN2007od', filterarray

; filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']


readcol, 'SN2007od_inserra.dat', inserradate, inserraMJDm, inserraU, inserraUerr, inserraB, inserraBerr, inserraV, inserraVerr, inserraR, inserraRerr, inserraI, inserraIerr, inserraCamera, format='(A, A,A,A,A,A,A,A,A,A,A,A, I)', /silent

inserraMJD=inserraMJDm-0.5

inserraU=float(inserraU)
inserraUerr=float(inserraUerr)
inserraU[where(inserraU eq 0)]=!Values.F_NAN
inserraUerr[where(inserraUerr eq 0)]=!Values.F_NAN

inserraB=float(inserraB)
inserraBerr=float(inserraBerr)
inserraB[where(inserraB eq 0)]=!Values.F_NAN
inserraBerr[where(inserraBerr eq 0)]=!Values.F_NAN


inserraV=float(inserraV)
inserraVerr=float(inserraVerr)
inserraV[where(inserraV eq 0)]=!Values.F_NAN
inserraVerr[where(inserraVerr eq 0)]=!Values.F_NAN


inserraR=float(inserraR)
inserraRerr=float(inserraRerr)
inserraR[where(inserraR eq 0)]=!Values.F_NAN
inserraRerr[where(inserraRerr eq 0)]=!Values.F_NAN

inserraI=float(inserraI)
inserraIerr=float(inserraIerr)
inserraI[where(inserraI eq 0)]=!Values.F_NAN
inserraIerr[where(inserraIerr eq 0)]=!Values.F_NAN





readcol, 'SN2007od_andrews.dat', andrewsepoch, andrewsV, andrewsVerr, andrewsR, andrewsRerr, andrewsI, andrewsIerr, format='(F, F, F, A, A, F, F)', /silent

andrewsMJD=2454398.0+andrewsepoch-2400000.5

andrewsR=float(andrewsR)
andrewsRerr=float(andrewsRerr)
andrewsR[where(finite(andrewsR) eq 0)]=!Values.F_NAN
andrewsRerr[where(finite(andrewsRerr) eq 0)]=!Values.F_NAN


the above need to be added to filtermjdarray and filtermagarray


;;; shift in mag is necessary to put in Vega system

rvegazeropoint=vegazeropoint(filters[6])
rabzeropoint=abzeropoint(filters[6])
ivegazeropoint=vegazeropoint(filters[6])
iabzeropoint=abzeropoint(filters[6])

rshift=rvegazeropoint-rabzeropoint
ishift=ivegazeropoint-iabzeropoint




createIIPmagarray, 'SN2007od', filterarray, filtermjdarray, filtermagarray, filtermagerrarray, bigmjdarray, bigmagarray, bigmagerrarray, 54407.5, 1.0


stop
end