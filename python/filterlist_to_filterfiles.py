
def filterlist_to_filterfilelist(filterlist):

    filterfilelist=filterlist

    for filter in filterfilelist:

	if filter == UVW2:
		filter='UVW2_2010.txt'
	if filter == UVM2:
		filter='UVM2_2010.txt'
	if filter == UVW1:
		filter='UVW1_2010.txt'
	if filter == U:
		filter='U_UVOT.txt'
	if filter == B:
		filter='B_UVOT.txt'
	if filter == V:
		filter='V_UVOT.txt'
	if filter == g:
		filter='LSST_g.dat'
	if filter == r:
		filter='LSST_r.dat'
	if filter == i:
		filter='LSST_i.dat'
	if filter == u:
		filter='LSST_u.dat'
	if filter == z:
		filter='LSST_z.dat'
	if filter == y:
		filter='LSST_y4.dat'
	if filter == F200W:
		filter='F200W_NRC_and_OTE_ModAB_mean.txt'
	if filter == F444W:
		filter='F444W_NRC_and_OTE_ModAB_mean.txt'

    return filterfilelist;

filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I']
filterlist_to_filterfilelist(filterlist)
print, filterfilelist

                    
                                              
                        
