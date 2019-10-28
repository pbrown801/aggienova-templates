
def filterlist_to_filterfiles(filterlist):
    filterfilelist=[' '] * len(filterlist)
    for idx,filter in enumerate(filterlist):
        if filter == 'UVW2' or filter == 'UVM2' or filter == 'UVW1':
            filterfilelist[idx]='../filters/'+filter+'_2010.txt'
        if filter == 'U' or filter == 'B' or filter == 'V':
            filterfilelist[idx]='../filters/'+filter+'_UVOT.txt'
        if filter == 'R':
            filterfilelist[idx]='../filters/R_Harris_c6004.txt'
        if filter == 'I':
            filterfilelist[idx]='../filters/johnson_i.txt'
        if filter == 'g' or filter == 'r' or filter == 'i' or filter == 'u' or filter =='z':
            filterfilelist[idx]='../filters/LSST_'+filter+'.dat'
        if filter == 'y':
            filterfilelist[idx]='../filters/LSST_y4.dat'
        if filter == 'F200W' or filter == 'F444W':
            filterfilelist[idx]='../filters/'+filter+'_NRC_and_OTE_ModAB_mean.txt'
        if filter == 'J' or filter == 'H':
            filterfilelist[idx]='../filters/'+filter+'_2mass.txt'
        if filter == 'K':
            filterfilelist[idx]='../filters/Ks_2mass.txt'

    return filterfilelist;


'''
    for idx,filter in enumerate(filterfilelist):
        if (filter == 'UVW2' or 'UVM2' or 'UVW1'):
                filterfilelist[idx]= filter+'_2010.txt'
        if (filter == 'U' or 'B' or 'V'):
                filterfile[idx]= filter+'_UVOT.txt'
        if (filter == 'R'):
                filterfilelist[idx]='R_Harris_c6004.txt'
        if (filter == 'I'):
                filterfilelist[idx]='johnson_i.txt'
        if (filter == 'g' or 'r' or 'i' or 'u' or 'z'):
                filterfilelist[idx]='LSST_'+filter+'.dat'
        if (filter == 'y'):
                filterfilelist[idx]='LSST_y4.dat'
        if (filter == 'F200W' or 'F444W'):
                filterfilelist[idx]=filter+'_NRC_and_OTE_ModAB_mean.txt'     
'''
    
# filterlist = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I']
# filterfilelist = filterlist_to_filterfiles(filterlist)
# print(filterfilelist)




