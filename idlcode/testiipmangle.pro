pro testiipmangle

filters=['$SNSCRIPTS/filters/UVW2_B11.txt','$SNSCRIPTS/filters/UVM2_B11.txt','$SNSCRIPTS/filters/UVW1_B11.txt','$SNSCRIPTS/filters/U_P08.txt','$SNSCRIPTS/filters/B_P08.txt','$SNSCRIPTS/filters/V_P08.txt','$SNSCRIPTS/filters/r_passband_period_one_and_two.txt','$SNSCRIPTS/filters/i_passband_period_one_and_two.txt']
n_filters=n_elements(filters)

mags=[17.7561, 17.7924, 16.7167, 15.3912, 15.2130, 14.5870, 14.3740, 14.4560]
magerrs=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

sniimodelphases=[1.5, 2.5, 7.5, 9.5, 14.5, 15.5, 20.6,  27.6, 32.6, 41.6, 56.6, 72.5]

sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']

testspectrum=sniimodelspecs[8]
testmag_array=fltarr(n_filters)
for n=0, n_filters-1 do testmag_array[n]=vegaphot(testspectrum, filters[n])
mags=testmag_array

;makesedfromphot, mags, filters, sed
makeweightedsedfromphot, mags, magerrs, filters, sed


sniimodelphases=[1.5, 2.5, 7.5, 9.5, 14.5, 15.5, 20.6,  27.6, 32.6, 41.6, 56.6, 72.5]

sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']

testspectrum=sniimodelspecs[8]

readcol, testspectrum, sp_wave, sp_flux, /silent
plot, sp_wave, sp_flux, xrange=[1000,10000], /ylog
oplot, sed[0,*], sed[1,*], psym=-4, symsize=2, thick=2



print, 'final stop'
stop
end