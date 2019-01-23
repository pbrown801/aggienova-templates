'''
This program lets you parse through a user-downloaded .json file from the Open Supernova Archive
Keep track of what directories you download the .json files in
This program then pulls the photometry and spectra data and places them into arrays and lists

numpy is needed to run this code

Update 1.1: Program can now save magnitude and spectra data to a .npz file
Update 1.2: Program can now temporarily change directory outside of python and save .npz file into a directory (code found at bottom)
Update 1.3: Program can now extract magnitude error data from json and save into .npz file
Update 1.4: Could no longer connect via urllib2. Bypassed by manually downloading .json file from website. No big deal.
            Just adds a few more housekeeping steps.
'''

#####Import the modules that this program uses#####

import json
import numpy as np
import os
import os.path


#####Run this program in the SAME DIRECTORY YOUR .json FILE IS IN!!!#####

print "Make sure you're in the right directory before running!"
print ""


SNname = raw_input("Enter supernova name: ")

#####Performs a file test to see if this supernova has already been parsed#####

filetest= "/Users/brittonbeeny/Desktop/astroresearch/%s.npz" % (SNname)

if os.path.exists(filetest):
    print "This supernova has been processed"


#####If this is a new supernova, program runs#####
else:
    print ''
    ###file opening###
    filename = '%s.json' % (SNname)


    f = open(filename,'r')
    json = json.load(f)


    #####And AWAY WE GO!#####

    print "Working on extracting data..."



    #####This next section goes through the photometry section of the .json file
    #####It collects each magnitude according to filter. Very repetitive.

    total = len(json[SNname]['photometry'])
    #V-band magnitudes & errors
    Vindexlist = []
    magvlist = []
    magverr = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'V':
                Vindexlist.append(x)
            else:
                pass
        except:
            pass
    Vindexarray = np.asarray(Vindexlist)
    for index in Vindexarray:
        magvlist.append(float(json[SNname]['photometry'][index]['magnitude']))
    vmag_array = np.asarray(magvlist)
    print "V magnitudes extracted..."
    print ""

    for index in Vindexarray:
        if 'e_magnitude' in json[SNname]['photometry'][index]:
            magverr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
    vmag_err = np.asarray(magverr)
    print "V magnitude errors extracted"
    print ''



    #B-band magnitudes & errors
    Bindexlist = []
    magblist = []
    magberr = []
    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'B':
                Bindexlist.append(x)
            else:
                pass
        except:
            pass
    Bindexarray = np.asarray(Bindexlist)
    for index in Bindexarray:
        magblist.append(float(json[SNname]['photometry'][index]['magnitude']))
    bmag_array = np.asarray(magblist)
    print "B Magnitudes extracted..."
    print ""
    try:
        for index in Bindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magberr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        bmag_err = np.asarray(magberr)
        print "B magnitude errors extracted..."
        print ''
    except:
        pass



    #U-band magnitudes & errors
    Uindexlist = []
    magulist = []
    maguerr = []
    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'U':
                Uindexlist.append(x)
            else:
                pass
        except:
            pass
    Uindexarray = np.asarray(Uindexlist)
    for index in Uindexarray:
        magulist.append(float(json[SNname]['photometry'][index]['magnitude']))
    umag_array = np.asarray(magulist)
    print "U Magnitudes extracted..."
    print ""
    try:
        for index in Uindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                maguerr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        umag_err = np.asarray(maguerr)
        print "U magnitude errors extracted..."
        print ''
    except:
        pass



    #R-band magnitudes & errors
    Rindexlist = []
    magrlist = []
    magrerr = []
    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'R':
                Rindexlist.append(x)
            else:
                pass
        except:
            pass
    Rindexarray = np.asarray(Rindexlist)
    for index in Rindexarray:
        magrlist.append(float(json[SNname]['photometry'][index]['magnitude']))
    rmag_array = np.asarray(magrlist)
    print "R Magnitudes extracted..."
    print ""
    try:
        for index in Rindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magrerr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        rmag_err = np.asarray(magrerr)
        print "R magnitude errors extracted..."
        print ''
    except:
        pass



    #I-band magnitudes & errors
    Iindexlist = []
    magilist = []
    magierr = []
    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'I':
                Iindexlist.append(x)
            else:
                pass
        except:
            pass
    Iindexarray = np.asarray(Iindexlist)
    for index in Iindexarray:
        magilist.append(float(json[SNname]['photometry'][index]['magnitude']))
    imag_array = np.asarray(magilist)
    print "I Magnitudes extracted..."
    print ""
    try:
        for index in Iindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magierr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        imag_err = np.asarray(magierr)
        print "I magnitude errors extracted..."
        print ''
    except:
        pass



    #w1 magnitudes and errors

    w1indexlist = []
    magw1list =[]
    magw1err = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'W1':
                w1indexlist.append(x)
            else:
                pass
        except:
            pass
    w1indexarray = np.asarray(w1indexlist)


    for index in w1indexarray:
        magw1list.append(float(json[SNname]['photometry'][index]['magnitude']))
    w1mag_array = np.asarray(magw1list)

    if len(w1mag_array) > 0:
        print "W1 magnitudes extracted..."
        print ""
    elif len(w1mag_array) == 0:
        print "No W1 magnitudes found..."
        print ""

    try:
        for index in w1indexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magw1err.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        w1mag_err = np.asarray(magw1err)
    except:
        pass
    if len(w1mag_err) > 0:
        print "W1 magnitude errors extracted"
        print ""
    elif len(w1mag_err) == 0:
        print "No W1 magnitude errors found..."
        print ""

    #w2 magnitudes and errors
    w2indexlist = []
    magw2list =[]
    magw2err = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'W2':
                w2indexlist.append(x)
            else:
                pass
        except:
            pass
    w2indexarray = np.asarray(w2indexlist)
    for index in w2indexarray:
        magw2list.append(float(json[SNname]['photometry'][index]['magnitude']))
    w2mag_array = np.asarray(magw2list)
    if len(w2mag_array) > 0:
        print "W2 magnitudes extracted..."
        print ""
    elif len(w2mag_array) == 0:
        print "No W2 magnitudes found..."
        print ""


    try:
        for index in w2indexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magw2err.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        w2mag_err = np.asarray(magw2err)
    except:
        pass
    if len(w2mag_err) > 0:
        print "W2 magnitude errors extracted..."
        print ""
    elif len(w2mag_err) == 0:
        print "No W2 magnitude errors found..."
        print ""
    #m2 magnitudes and errors
    m2indexlist = []
    magm2list =[]
    magm2err = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'M2':
                m2indexlist.append(x)
            else:
                pass
        except:
            pass
    m2indexarray = np.asarray(m2indexlist)
    for index in m2indexarray:
        magm2list.append(float(json[SNname]['photometry'][index]['magnitude']))
    m2mag_array = np.asarray(magm2list)
    if len(m2mag_array) > 0:
        print "M2 magnitudes extracted..."
        print ""
    elif len(m2mag_array) == 0:
        print "No M2 magnitudes found..."
        print ""


    try:
        for index in m2indexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magm2err.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
               pass
        m2mag_err = np.asarray(magm2err)

    except:
        pass

    if len(m2mag_err) > 0:
        print "M2 magnitude errors extracted..."
        print ""
    elif len(m2mag_err) == 0:
        print "No M2 magnitude errors found..."
        print ""
    #J magnitudes and errors
    jindexlist = []
    magjlist =[]
    magjerr = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'J':
                jindexlist.append(x)
            else:
                pass
        except:
            pass
    jindexarray = np.asarray(jindexlist)
    for index in jindexarray:
        magjlist.append(float(json[SNname]['photometry'][index]['magnitude']))
    jmag_array = np.asarray(magjlist)
    if len(jmag_array) > 0:
        print "J magnitudes extracted..."
        print ""
    elif len(jmag_array) == 0:
        print "No J magnitudes found"
        print ""


    try:
        for index in jindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magjerr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
               pass
        jmag_err = np.asarray(magjerr)
    except:
        pass
    if len(jmag_err) > 0:
        print "J magnitude errors extracted..."
        print ""
    elif len(jmag_err) == 0:
        print "No J magnitude errors found..."
        print ""
    #H magnitude errors
    hindexlist = []
    maghlist =[]
    magherr = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'H':
                hindexlist.append(x)
            else:
                pass
        except:
            pass
    hindexarray = np.asarray(hindexlist)
    for index in hindexarray:
        maghlist.append(float(json[SNname]['photometry'][index]['magnitude']))
    hmag_array = np.asarray(maghlist)
    if len(hmag_array) > 0:
        print "H magnitudes extracted..."
        print ""
    elif len(hmag_array) == 0:
        print "No H magnitudes found..."
        print ""


    try:
        for index in hindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magherr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        hmag_err = np.asarray(magherr)
    except:
        pass
    if len(hmag_err) > 0:
        print "H magnitude errors extracted..."
        print ""
    elif len(hmag_err) == 0:
        print "No H magnitude errors found..."
        print ""

    #K magnitudes and errors
    kindexlist = []
    magklist =[]
    magkerr = []

    for x in range(total):
        try:
            if json[SNname]['photometry'][x]['band'] == 'K':
                kindexlist.append(x)
            else:
                pass
        except:
            pass
    kindexarray = np.asarray(kindexlist)
    for index in kindexarray:
        magklist.append(float(json[SNname]['photometry'][index]['magnitude']))
    kmag_array = np.asarray(magklist)
    if len(kmag_array) > 0:
        print "K magnitudes extracted..."
        print ""
    elif len(kmag_array) == 0:
        print "No K magnitudes found..."
        print ""


    try:
        for index in kindexarray:
            if 'e_magnitude' in json[SNname]['photometry'][index]:
                magkerr.append(float(json[SNname]['photometry'][index]['e_magnitude']))
            else:
                pass
        kmag_err = np.asarray(magkerr)
    except:
        pass
    if len(kmag_err) > 0:
        print "K magnitude errors extracted..."
        print ""
    elif len(kmag_err) == 0:
        print "No K magnitude errors found..."
        print ""

    #####This section goes through the .json file and
    #####essentially grabs the "Time" axis of a lightcurve

    vtimelist=[]
    for index in Vindexarray:
        try:
            vtimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    vtime_array = np.asarray(vtimelist)

    btimelist=[]
    for index in Bindexarray:
        try:
            btimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    btime_array = np.asarray(btimelist)

    utimelist=[]
    for index in Uindexarray:
        try:
            utimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    utime_array = np.asarray(utimelist)

    rtimelist=[]
    for index in Rindexarray:
        try:
            rtimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    rtime_array = np.asarray(rtimelist)

    itimelist=[]
    for index in Iindexarray:
        try:
            itimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    itime_array = np.asarray(itimelist)

    w1timelist=[]
    for index in w1indexarray:
        try:
            w1timelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    w1time_array = np.asarray(w1timelist)

    w2timelist=[]
    for index in w2indexarray:
        try:
            w2timelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    w2time_array = np.asarray(w2timelist)

    m2timelist=[]
    for index in m2indexarray:
        try:
            m2timelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    m2time_array = np.asarray(m2timelist)

    jtimelist=[]
    for index in jindexarray:
        try:
            jtimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    jtime_array = np.asarray(jtimelist)

    htimelist=[]
    for index in hindexarray:
        try:
            htimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    htime_array = np.asarray(htimelist)

    ktimelist=[]
    for index in kindexarray:
        try:
            ktimelist.append(float(json[SNname]['photometry'][index]['time']))
        except:
            print 'error on index ', [index]
    ktime_array = np.asarray(ktimelist)





    #####This next section collects spectral data#####

    print "Extracting spectral data..."
    print ''

    totalspec = len(json[SNname]['spectra'])

    wavelengthlist=[]
    fluxlist = []
    print "There are %i spectra available" % (totalspec)
    print ''

    ###first for loop creates N number of zero arrays to put into wavelengthlist
    print "Extracting wavelength data..."
    print "Appending to list..."
    print ''
    for spectra in range(totalspec):
        interiorwlarray = np.zeros(len(json[SNname]['spectra'][spectra]['data']))

    ###this for loop extracts the individual wavelengths and puts them into zero arrays

        for x in range(len(json[SNname]['spectra'][spectra]['data'])):
            interiorwlarray[x]=json[SNname]['spectra'][spectra]['data'][x][0]

        wavelengthlist.append(interiorwlarray)
    print "Extracting flux data..."
    print "Appending to list..."
    print ''
    for spectra in range(totalspec):
        interiorfluxarray = np.zeros(len(json[SNname]['spectra'][spectra]['data']))

    ###this for loop extracts the individual fluxes and puts them into zero arrays
        for x in range(len(json[SNname]['spectra'][spectra]['data'])):
            interiorfluxarray[x]=json[SNname]['spectra'][spectra]['data'][x][1]

        fluxlist.append(interiorfluxarray)
    epoch_list = []
    for spectra in range(totalspec):
        epoch_list.append(float(json[SNname]['spectra'][spectra]['time']))
    epoch_array = np.asarray(epoch_list)
    print "Epochs for spectra extracted..."
    print ""



    #################################Save Section################################################

    '''
    This section allows you to save the .npz files into any directory you want.
    Change the desired path to any path that suits your organizational needs.
    The return_path must be the directory you ran this program from. I leave mine
    as an example.
    '''

    cwd = os.getcwd()

    path = raw_input('Enter the destination directory. If you want to save to the cwd, type "cwd"\n> ')
    if path == 'cwd':
        os.chdir(cwd)
    else:
        os.chdir(path)

    ###Save in the new directory###

    savefile = '%s' % (SNname)
    np.savez(savefile, vmag_array=vmag_array, bmag_array=bmag_array, umag_array=umag_array, rmag_array=rmag_array,
             imag_array=imag_array, vtime_array=vtime_array,btime_array=btime_array, utime_array=utime_array, rtime_array=rtime_array,
             itime_array=itime_array, wavelengthlist=wavelengthlist, fluxlist=fluxlist, vmag_err=vmag_err,bmag_err=bmag_err,umag_err=umag_err,
             rmag_err=rmag_err,imag_err=imag_err,epoch_array=epoch_array,w1mag_array=w1mag_array,w2mag_array=w2mag_array,m2mag_array=m2mag_array,
             jmag_array=jmag_array,hmag_array=hmag_array,kmag_array=kmag_array,w1time_array=w1time_array,w2time_array=w2time_array,
             m2time_array=m2time_array,jtime_array=jtime_array,htime_array=htime_array,ktime_array=ktime_array,w1mag_err=w1mag_err,
             w2mag_err=w2mag_err,m2mag_err=m2mag_err,jmag_err=jmag_err,hmag_err=hmag_err,kmag_err=kmag_err)


    print "Arrays and lists for %s successfully saved" % (SNname)
    print ''

    ###Return to original directory###

    return_command = os.chdir(cwd)
