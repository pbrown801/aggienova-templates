pro test


sniimodelspecs='sniimodels/'+['tst_n20_5_B.fl', 'tst_n20_6_v1.fl', 'n7_j20b_v4_s1_l3_v2.fl', 'n7_j16b_v4_s1_l3_v1_B.fl', 'n16_n10_s0_v1_B_new2.fl', 'n16_n10_s0_v1_B_new2_3.fl', 'n16_n10_s0_v1_B_new6.fl',  'nj4_1v1_new3_abund.fl', 'nj4_1v1_new3_abund.fl', 'nj4_1v1_new2_abund.fl', 'nj4_1v1_new1_abund.fl', 'nj4_1v1_new_abund.fl']

nepochs=n_elements(sniimodelspecs)

for n=0,nepochs-1 do begin

	templatespectrumfile=sniimodelspecs[n]

	readcol, templatespectrumfile, sp_wave,sp_flux,/silent

	print, sp_wave[0]
	print, sp_wave[n_elements(sp_wave)-1]

endfor




stop

end