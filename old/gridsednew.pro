;;;;;;;;;;;;;;;;;;
pro gridsednew, inputcounts, inputcounterrs=inputcounterrs, bestsed=bestsed, sedarray=sedarray, chisqarray=chisqarray, sedcount_array=sedcount_array, sigmaone=sigmaone, sedwave=sedwave

inputcounts=inputcounts[0:5]
;  10,000 K black body
;   inputcounts=[5.00085e+06,  4.11938e+06,  8.76916e+06,  2.29198e+07,  1.97022e+07,  7.37948e+06]
inputcounterrs=inputcounts*0.1
; vega
; inputcounts=[8.97155e+06 , 5.51979e+06 , 9.52015e+06 , 2.18502e+07 , 4.41138e+07 , 1.43316e+07 ]
; 92a
; inputcounts=[4.54193   ,   1.81368  ,17.0897, 152.233 , 322.275 , 127.479 ]
inputcounterrs=inputcounts*0.1
; 2000.dat
; inputcounts=[0.764703 , 0.00164981 , 1.17282 , 2.63378 , 44.8891 , 179.715 ]
;ngc6340
; inputcounts=[ 1.20852 , 0.714380 , 3.86486 , 27.1768 , 78.3275 , 64.7172 ] 



IF KEYWORD_SET(inputcounterrs) THEN errorflag=1 else inputcounterrs=inputcounts*0.1

if n_elements(inputcounterrs) eq 1 then inputcounterrs=[inputcounterrs,inputcounterrs,inputcounterrs,inputcounterrs,inputcounterrs,inputcounterrs]

zeropoints=[17.35, 16.82, 17.49, 18.34, 19.11, 17.89]

h = 1D*6.62606957E-27
c = 1D*2.99792458E18 ; in angstroms per second
hc = 1D*1.986E-8
hc = h*c
e = 1D*2.71828
k = 1D*1.38E-16

;read in filter curves
filtercurves=["$SNSCRIPTS/UVW2_2010.txt","$SNSCRIPTS/UVM2_2010.txt","$SNSCRIPTS/UVW1_2010.txt","$SNSCRIPTS/U_UVOT.txt","$SNSCRIPTS/B_UVOT.txt","$SNSCRIPTS/V_UVOT.txt"]
readcol,"$SNSCRIPTS/V_UVOT.txt",lambda,V_EA,/silent
filter_array=fltarr(n_elements(filtercurves),n_elements(lambda) )

for f=0,n_elements(filtercurves)-1 do begin
	readcol,filtercurves[f],filter_wave,filter_ea,/silent
	filter_array[f,*]=filter_ea
endfor

; default flux conversion factors
stellarfluxdensityfactors=[6.2, 8.50, 4.0, 1.63, 1.472, 2.614] *10.0^(-16)
vegaeffwave=[2030,2230,2590,3500,4330,5400,1950,2500]

sedwave=[1600,vegaeffwave[1:4],6000,8000]

checkorientation=size(inputcounts)

if checkorientation[1] eq 1 then stellarsed = [transpose(inputcounts)*stellarfluxdensityfactors[0:5],inputcounts[5]*stellarfluxdensityfactors[5]]
if checkorientation[1] eq 6 then stellarsed = [(inputcounts*stellarfluxdensityfactors[0:5]),inputcounts[5]*stellarfluxdensityfactors[5]]

sedcounts_array=make_array(6,/FLOAT,VALUE=!values.f_nan) 
counts_array=make_array(6,/FLOAT,VALUE=!values.f_nan) 

sedflux_lambda=interpol(stellarsed,sedwave, lambda)

for f=0,5 do counts_array[f]=tsum(lambda,filter_array[f,*]*sedflux_lambda*lambda/hc)
; check if the synthetic counts are within one sigma error of the input counts
check=make_array(6,/FLOAT,VALUE=!values.f_nan) 
for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
sedcounts_array=counts_array
if total(check) eq 6 then sigmaone=1 else sigmaone=0

sedarray=stellarsed
newflux=stellarsed
chisqarray=total(((inputcounts-counts_array)/inputcounterrs)^2.0)

  stellarfluxdensityfactors=[6.2, 8.50, 4.0, 1.63, 1.472, 2.614] *10.0^(-16)
starthighfluxdensityfactors=[6.59, 9.38, 4.52, 1.79, 1.61, 3.10] *10.0^(-16)*1.0
 startlowfluxdensityfactors=[0.01, 2.90, 0.48, 1.18, 1.07, 2.18] *10.0^(-16)/1.0

scaledifferences=starthighfluxdensityfactors/startlowfluxdensityfactors

iteration=0

maxiter=10
oldlowflux=[1.0,1.0,1.0,1.0,1.0,1.0]

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

nsteps=4+iteration


	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=dblarr(7)
	highflux=dblarr(7)
	if iteration eq 0 then for f=0,5 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]/10.00
	if iteration eq 0 then for f=0,5 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]*10.0
	if iteration gt 0 then for f=0,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )
	if iteration gt 0 then for f=0,6 do highflux[f]=max( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )

	for f=0,6 do if highflux[f] eq lowflux[f] then lowflux[f]=lowflux[f]/10.0
	for f=0,6 do if highflux[f] eq lowflux[f]*10.0 then highflux[f]=highflux[f]*10.0

	; if it hasn't found a good match after five iterations, widen the search

	if iteration eq 5 then for f=1,4 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]/10.00
	if iteration eq 5 then for f=1,4 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]*10.0
	if iteration eq 5 then lowflux[0]  =startlowfluxdensityfactors[0]*inputcounts[0]/1000.00
	if iteration eq 5 then highflux[0]=starthighfluxdensityfactors[0]*inputcounts[0]*10.0
	if iteration eq 5 then lowflux[2]  =startlowfluxdensityfactors[2]*inputcounts[2]/100.00
	if iteration eq 5 then lowflux[5]  =startlowfluxdensityfactors[5]*inputcounts[5]/10.00
	if iteration eq 5 then highflux[5]=starthighfluxdensityfactors[5]*inputcounts[5]*10.0


	if iteration eq 6 then for f=1,4 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]/10.00
	if iteration eq 6 then for f=1,4 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]*10.0
	;use uvm2 to set uv scale
	if iteration eq 6 then lowflux[0]  =startlowfluxdensityfactors[1]*inputcounts[1]/1000.00
	if iteration eq 6 then lowflux[2]  =startlowfluxdensityfactors[1]*inputcounts[1]/10.00
	if iteration eq 6 then lowflux[5]  =startlowfluxdensityfactors[5]*inputcounts[5]/10.00
	if iteration eq 6 then highflux[5]=starthighfluxdensityfactors[5]*inputcounts[5]*10.0




for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						; check if the synthetic counts are within one sigma error of the input counts
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0


	iteration=iteration+1.0


endwhile


bestsed=sedarray[*,allbest[0]]



stop
;;;;;;;;;;;;;;;;

	lowflux=dblarr(7)
	highflux=dblarr(7)




iteration=0

maxiter=10
oldlowflux=[1.0,1.0,1.0,1.0,1.0,1.0]

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])


	if iteration eq 0 then for f=0,5 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]
	if iteration eq 0 then for f=0,5 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]

	if iteration gt 0 then for f=0,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )
	if iteration gt 0 then for f=0,6 do highflux[f]=max( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )



	if iteration gt 0 then for f=0,6 do if highflux[f] eq lowflux[f] then lowflux[f]=highflux[f]/10.0
	if iteration gt 0 then for f=0,6 do if highflux[f] eq lowflux[f] then lowflux[f]=highflux[f]/10.0



	if iteration eq 6 then for f=0,6 do if highflux[f] eq lowflux[f] then highflux[f]=highflux[f]*10.0
	if iteration eq 6 then for f=0,6 do if highflux[f] eq lowflux[f] then highflux[f]=highflux[f]*10.0


	if iteration eq 8 then for f=0,6 do if highflux[f] eq lowflux[f] then lowflux[f]=lowflux[f]*10.0
	if iteration eq 8 then for f=0,6 do if highflux[f] eq lowflux[f] then lowflux[f]=lowflux[f]*10.0


for f=0,3 do if lowflux[f] eq oldlowflux[f] then lowflux[f]=lowflux[f]/10.0

for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0


	iteration=iteration+1.0




endwhile


;;;;;;; rank stuff -- not used further

allvalues=make_array(6,maxiter*nsteps,/FLOAT,VALUE=!values.f_nan) 
allminchisq=make_array(6,maxiter*nsteps,/FLOAT,VALUE=!values.f_nan) 

;; should make a ranked list of the values used
for f=0,5 do begin
order=sort(sedarray[f,*])
allvalues[f,0]=sedarray[f,order[0]]
allminchisq[f,0]=min(chisqarray[where(sedarray[f,*] eq allvalues[f,0])])
	for n=1,maxiter*nsteps-1 do begin
		next=where(sedarray[f,order] gt allvalues[f,n-1],count)
		if count gt 0 then allvalues[f,n]=sedarray[f,order[next[0]]]
		if count gt 0 then allminchisq[f,n]=min(chisqarray[where(sedarray[f,*] eq allvalues[f,n])])
	endfor
endfor


for f=0,5 do begin

close=where( allminchisq[f,*] lt min(allminchisq[f,*]+5.0 ) )
lowflux[f]=allvalues[f,close[0]]
if close[0] eq 0 then lowflux[f]=allvalues[f,0]/10.0
highflux[f]=allvalues[f,close[n_elements(close)-1]]
if close[n_elements(close)-1] eq (n_elements(close)-1) then highflux[f]=allvalues[f,n_elements(close)-1]*10.0

	if n_elements(close) eq 1 then highflux[f]=highflux[f]*10.0
	if n_elements(close) eq 1 then lowflux[f]=lowflux[f]/10.0

endfor

highflux[6]=highflux[5]
lowflux[6]=lowflux[5]

;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;

iteration=0

maxiter=10
oldlowflux=[1.0,1.0,1.0,1.0,1.0,1.0]

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=dblarr(7)
	highflux=dblarr(7)

	if iteration eq 0 then for f=0,5 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]
	if iteration eq 0 then for f=0,5 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]

	if iteration gt 0 then for f=0,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )
	if iteration gt 0 then for f=0,6 do highflux[f]=max( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )



for f=0,3 do if lowflux[f] eq oldlowflux[f] then lowflux[f]=lowflux[f]/10.0

for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0


	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]

;;;;;;;;;;;;
iteration=0

maxiter=10
oldlowflux=[1.0,1.0,1.0,1.0,1.0,1.0]

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin


for f=0,5 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]
for f=0,5 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]

for f=0,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )

for f=0,4 do lowflux[f]   =startlowfluxdensityfactors[f]*inputcounts[f]*0.1^iteration
for f=0,4 do highflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]*0.1^(iteration-1.0)


if lowflux[0] ne oldlowflux[0] then begin

for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0

endif
	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]

;;;;;;;;;;;;

iteration=0

maxiter=10
oldlowflux=[1.0,1.0,1.0,1.0,1.0,1.0]

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=dblarr(7)
	highflux=dblarr(7)

	if iteration eq 0 then for f=0,5 do lowflux[f]  =startlowfluxdensityfactors[f]*inputcounts[f]
	if iteration eq 0 then for f=0,5 do highflux[f]=starthighfluxdensityfactors[f]*inputcounts[f]

	if iteration gt 0 then for f=0,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )/min(chisqarray)
	if iteration gt 0 then for f=0,6 do highflux[f]=max( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )

if lowflux[0] ne oldlowflux[0] then begin

for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0

endif
	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]

;;;;;;;;;;;;



if min(chisqarray) gt 1.0 then begin
print, 'trying different grid'
iteration=0

maxiter=10

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=bestsed
	highflux=bestsed

	if iteration eq 0 then for f=0,3 do lowflux[f]  =bestsed[f]*0.001

	if iteration gt 0 then for f=0,6 do lowflux[f]=bestsed[f]*(iteration/maxiter)
	if iteration gt 0 then for f=0,6 do highflux[f]=bestsed[f]*(maxiter/iteration)

for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0

	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]

endif




;;;;;;;;;;;;


if min(chisqarray) gt 1.0 then begin
print, 'trying different things in the UV'
iteration=0

maxiter=10

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=dblarr(7)
	highflux=dblarr(7)


	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=bestsed
	highflux=bestsed

	for f=3,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )
	for f=0,6 do highflux[f]=max( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )

; use m2 to set
	for f=0,2 do lowflux[f]  =startlowfluxdensityfactors[1]*inputcounts[1]*0.1/ (iteration+1.0)^2.0 

if lowflux[0] ne oldlowflux[0] then begin

for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
;; keep b and v set to the best
				newflux[4]=bestsed[4]
				newflux[5]=bestsed[5]
				newflux[6]=bestsed[6]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux

	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0
endif

	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]


endif

;;;;;;;;;;;;;;;;;;;;


if min(chisqarray) gt 1.0 then begin
print, 'trying different things in the UV'
iteration=0

maxiter=20

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=bestsed
	highflux=bestsed

	for f=0,6 do lowflux[f]=min( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )
	for f=0,6 do highflux[f]=max( sedarray[f,where(chisqarray lt min(chisqarray + chisqdif))] )


if lowflux[0] ne oldlowflux[0] then begin


for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux

	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0

endif

	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]

endif


;;;;;;;;;;;;;;;;;;;;
a

if min(chisqarray) gt 1.0 then begin
print, 'trying different grid'
iteration=0

maxiter=10

while (min(chisqarray) gt 0.8 and iteration lt maxiter) or iteration eq 0 do begin

	chisqdif = max([min(chisqarray)*2.0,1.0])

	lowflux=bestsed
	highflux=bestsed

	if iteration eq 0 then for f=0,3 do lowflux[f]  =bestsed[f]*0.001

	if iteration gt 0 then for f=0,6 do lowflux[f]=bestsed[f]*(iteration/maxiter)^2.0
	if iteration gt 0 then for f=0,6 do highflux[f]=bestsed[f]*(maxiter/iteration)^2.0



for l=0.0, nsteps-1 do begin
	newflux[0]=lowflux[0]+((highflux[0]-lowflux[0])*l/(nsteps-1.0))
	for m=0.0, nsteps-1 do begin
		newflux[1]=lowflux[1]+((highflux[1]-lowflux[1])*m/(nsteps-1.0))
		for n=0.0, nsteps-1 do begin
			newflux[2]=lowflux[2]+((highflux[2]-lowflux[2])*n/(nsteps-1.0))
			for o=0.0, nsteps-1 do begin
				newflux[3]=lowflux[3]+((highflux[3]-lowflux[3])*o/(nsteps-1.0))
				for p=0.0, nsteps-1 do begin
					newflux[4]=lowflux[4]+((highflux[4]-lowflux[4])*p/(nsteps-1.0))
					for q=0.0,nsteps-1 do begin
						newflux[5]=lowflux[5]+((highflux[5]-lowflux[5])*q/(nsteps-1.0))
						newflux[6]=newflux[5]
						sedflux_lambda=interpol(newflux,sedwave, lambda)
						for ff=0,5 do counts_array[ff]=tsum(lambda,filter_array[ff,*]*sedflux_lambda*lambda/hc)
						sedcounts_array=[[sedcounts_array], [counts_array]]
						chisqarray=[chisqarray,total(((inputcounts-counts_array)/inputcounterrs)^2.0)]
						sedarray=[[sedarray], [newflux]]
						check=make_array(6,/FLOAT,VALUE=!values.f_nan) 

						for f=0,5 do if abs(inputcounts[f]-counts_array[f]) lt inputcounterrs[f] then check[f]=1
						if total(check) eq 6 then sigmaone=[[sigmaone],[1]] else sigmaone=[[sigmaone],[0]]

					endfor
				endfor
			endfor
		endfor
	endfor
endfor

oldlowflux=lowflux


	allbest=where(chisqarray eq min(chisqarray))

	print, 'grid sed min chi sq ', min(chisqarray)

	chisqdif=chisqdif/2.0

	iteration=iteration+1.0

endwhile


bestsed=sedarray[*,allbest[0]]

endif







print, 'final stop'
stop
end
