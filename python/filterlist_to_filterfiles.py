
def filterlist_to_filterfiles(filterfilelist):

    for idx,filter in enumerate(filterfilelist):
        if filter == 'UVW2':
            filterfilelist[idx]='UVW2_2010.txt'
        if filter == 'UVM2':
            filterfilelist[idx]='UVM2_2010.txt'
        if filter == 'UVW1':
            filterfilelist[idx]='UVW1_2010.txt'
        if filter == 'U':
            filterfilelist[idx]='U_UVOT.txt'
        if filter == 'B':
            filterfilelist[idx]='B_UVOT.txt'
        if filter == 'V':
            filterfilelist[idx]='V_UVOT.txt'
        if filter == 'R':
            filterfilelist[idx]='R_Harris_c6004.txt'
        if filter == 'I':
            filterfilelist[idx]='johnson_i.txt'
        if filter == 'g':
            filterfilelist[idx]='LSST_g.dat'
        if filter == 'r':
            filterfilelist[idx]='LSST_r.dat'
        if filter == 'i':
            filterfilelist[idx]='LSST_i.dat'
        if filter == 'u':
            filterfilelist[idx]='LSST_u.dat'
        if filter == 'z':
            filterfilelist[idx]='LSST_z.dat'
        if filter == 'y':
            filterfilelist[idx]='LSST_y4.dat'
        if filter == 'F200W':
            filterfilelist[idx]='F200W_NRC_and_OTE_ModAB_mean.txt'
        if filter == 'F444W':
            filterfilelist[idx]='F444W_NRC_and_OTE_ModAB_mean.txt'

    return filterfilelist;

# filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I']
# filterfilelist = filterlist_to_filterfilelist(filterlist)
# print(filterfilelist)




