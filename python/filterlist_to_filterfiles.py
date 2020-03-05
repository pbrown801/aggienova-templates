def valid_wavelength(wavelength, template_minmax):
    if(wavelength <= template_minmax[1]) and (wavelength >= template_minmax[0]):
        return True
    return False

def filterlist_to_filterfiles(filterlist, template_spectrum):
    from mangle_simple import pivot_wavelength

    # wavelengths_template_spectrum contains lowest and highest value in range of template_spectrum
    spectra_path = '../spectra/' + template_spectrum
    spectra_file = open(spectra_path, "r")
    wavelengths_template_spectrum = []
    spectra_file_lines = spectra_file.readlines()
    spectra_file.close()
    line_0 = True
    for line_number, line in enumerate(spectra_file_lines, start=0):
        line = line.strip()
        if (line_number == 0) and (line[0] != "#"):
            line = line.split(" ")
            wavelengths_template_spectrum.append(float(line[0]))
            line_0 = False
        if line_0 and line_number == 1:
            line = line.split(" ")
            wavelengths_template_spectrum.append(float(line[0]))
        if line_number == len(spectra_file_lines) - 1:
            line = line.split(" ")
            wavelengths_template_spectrum.append(float(line[0]))

    zeropointlist = []
    pivotlist = []
    filterfilelist=[' '] * len(filterlist)

    for idx,filtertocheck in enumerate(filterlist):
        if filtertocheck == 'UVW2':
            filterfilelist[idx]='../filters/UVW2_2010.txt'
            pivot=pivot_wavelength('../filters/UVW2_2010.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(17.39)
        if filtertocheck == 'UVM2':
            filterfilelist[idx]='../filters/UVM2_2010.txt'
            pivot=pivot_wavelength('../filters/UVM2_2010.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(16.86)
        if filtertocheck == 'UVW1':
            filterfilelist[idx]='../filters/UVW1_2010.txt'
            pivot=pivot_wavelength('../filters/UVW1_2010.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(17.44)
        if filtertocheck == 'U':
            filterfilelist[idx]='../filters/U_UVOT.txt'
            pivot=pivot_wavelength('../filters/U_UVOT.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(18.34)
        if filtertocheck == 'B':
            filterfilelist[idx]='../filters/B_UVOT.txt'
            pivot=pivot_wavelength('../filters/B_UVOT.txt')
            pivotlist.append(pivot)
            zeropointlist.append(19.1)
        if filtertocheck == 'V':
            filterfilelist[idx]='../filters/V_UVOT.txt'
            pivot=pivot_wavelength('../filters/V_UVOT.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(17.88)
        if filtertocheck == 'R':
            filterfilelist[idx]='../filters/R_Harris_c6004.txt'
            pivot=pivot_wavelength('../filters/R_Harris_c6004.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(19.86)
        if filtertocheck == 'I':
            filterfilelist[idx]='../filters/johnson_i.txt'
            pivot=pivot_wavelength('../filters/johnson_i.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(14.91)
        if filtertocheck == 'g':
            filterfilelist[idx]='../filters/LSST_g.dat'
            pivot=pivot_wavelength('../filters/LSST_g.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(14.91)
        if filtertocheck == 'r':
            filterfilelist[idx]='../filters/LSST_r.dat'
            pivot=pivot_wavelength('../filters/LSST_r.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(14.42)
        if filtertocheck == 'i':
            filterfilelist[idx]='../filters/LSST_i.dat'
            pivot=pivot_wavelength('../filters/LSST_i.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(13.87)
        if filtertocheck == 'u':
            filterfilelist[idx]='../filters/LSST_u.dat'
            pivot=pivot_wavelength('../filters/LSST_u.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.84)
        if filtertocheck == 'z':
            filterfilelist[idx]='../filters/LSST_z.dat'
            pivot=pivot_wavelength('../filters/LSST_z.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(13.33)
        if filtertocheck == 'y':
            filterfilelist[idx]='../filters/LSST_y4.dat'
            pivot=pivot_wavelength('../filters/LSST_y4.dat')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.59)
        if filtertocheck == 'F200W':
            filterfilelist[idx]='../filters/F200W_NRC_and_OTE_ModAB_mean.txt'
            pivot=pivot_wavelength('../filters/F200W_NRC_and_OTE_ModAB_mean.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(22.8)
        if filtertocheck == 'F444W':
            filterfilelist[idx]='../filters/F444W_NRC_and_OTE_ModAB_mean.txt'
            pivot=pivot_wavelength('../filters/F444W_NRC_and_OTE_ModAB_mean.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(21.34)
        if filtertocheck == 'J':
            filterfilelist[idx]='../filters/J_2mass.txt'
            pivot=pivot_wavelength('../filters/J_2mass.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.95)
        if filtertocheck == 'H':
            filterfilelist[idx]='../filters/H_2mass.txt'
            pivot=pivot_wavelength('../filters/H_2mass.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(12.45)
        if filtertocheck == 'K':
            filterfilelist[idx]='../filters/Ks_2mass.txt'
            pivot=pivot_wavelength('../filters/Ks_2mass.txt')
            if valid_wavelength(pivot, wavelengths_template_spectrum):
                pivotlist.append(pivot)
                zeropointlist.append(11.77)
    return(filterfilelist,zeropointlist,pivotlist)
