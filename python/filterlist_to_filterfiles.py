
def filterlist_to_filterfiles(filterlist):

    filterfilelist=[' '] * len(filterlist)
    for idx,filter in enumerate(filterlist):
        if filter == 'UVW2':
            filterfilelist[idx]='../filters/UVW2_2010.txt'
        if filter == 'UVM2':
            filterfilelist[idx]='../filters/UVM2_2010.txt'
        if filter == 'UVW1':
            filterfilelist[idx]='../filters/UVW1_2010.txt'
        if filter == 'U':
            filterfilelist[idx]='../filters/U_UVOT.txt'
        if filter == 'B':
            filterfilelist[idx]='../filters/B_UVOT.txt'
        if filter == 'V':
            filterfilelist[idx]='../filters/V_UVOT.txt'
        if filter == 'R':
            filterfilelist[idx]='../filters/R_Harris_c6004.txt'
        if filter == 'I':
            filterfilelist[idx]='../filters/johnson_i.txt'
        if filter == 'g':
            filterfilelist[idx]='../filters/LSST_g.dat'
        if filter == 'r':
            filterfilelist[idx]='../filters/LSST_r.dat'
        if filter == 'i':
            filterfilelist[idx]='../filters/LSST_i.dat'
        if filter == 'u':
            filterfilelist[idx]='../filters/LSST_u.dat'
        if filter == 'z':
            filterfilelist[idx]='../filters/LSST_z.dat'
        if filter == 'y':
            filterfilelist[idx]='../filters/LSST_y4.dat'
        if filter == 'F200W':
            filterfilelist[idx]='../filters/F200W_NRC_and_OTE_ModAB_mean.txt'
        if filter == 'F444W':
            filterfilelist[idx]='../filters/F444W_NRC_and_OTE_ModAB_mean.txt'
        if filter == 'J':
            filterfilelist[idx]='../filters/J_2mass.txt'
        if filter == 'H':
            filterfilelist[idx]='../filters/H_2mass.txt'
        if filter == 'K':
            filterfilelist[idx]='../filters/Ks_2mass.txt'
    return filterfilelist;

# filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I']
# filterfilelist = filterlist_to_filterfiles(filterlist)
# print(filterfilelist)




