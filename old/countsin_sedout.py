def countsin_sedout(counts_array):

    print('printing counts within')
    print(counts_array)

    import numpy as np
    import matplotlib.pyplot as plt
    from operator import truediv
#######

    h = 6.6260755e-27
    c = 2.99792458e18
    hc = h*c

    files = ['filters/UVW2_2010.txt', 'filters/UVM2_2010.txt', 'filters/UVW1_2010.txt', 'filters/U_UVOT.txt', 'filters/B_UVOT.txt', 'filters/V_UVOT.txt']

    filter_WL = []
    filter_A = []

    for item in files:

        f = open(item,'r')

        filter_lambda = []
        filter_area = []
        for line in f:
            line = line.rstrip()
            column = line.split()
            wavelen = column[0]
            area = column[1]
            filter_lambda.append(float(wavelen))
            filter_area.append(float(area))

        filter_lambda = np.asarray(filter_lambda,dtype=float)
        filter_area = np.asarray(filter_area,dtype=float)
        
 #       nonzero = np.where(filter_area > 0.0)
        
 #       filter_lambda = filter_lambda[nonzero]
 #       filter_area = filter_area[nonzero]

        filter_WL.append(filter_lambda)
        filter_A.append(filter_area)

        f.close()
###    print(filter_area)
###    plt.plot(filter_lambda,filter_area)
###    plt.show

###    print("something")
###    wait = input("PRESS ENTER TO CONTINUE.")
###    print("something")    
### Starting with the factors associated with Pickles


    factor = [5.77E-16, 7.47E-16, 4.06E-16, 1.53E-16, 1.31E-16, 2.61E-16]
    factor = np.asarray(factor, dtype=float)

    new_WL = [1928,2246,2600,3465,4392,5468]
    flux_top=[]
    new_counts=[12341,12341234,123412341,1234134,12341234,1234132]
    flag = [0,0,0,0,0,0]


    filter_array = np.array([filter_A[0],filter_A[1],filter_A[2],filter_A[3],filter_A[4],filter_A[5]])

    filter_wave = np.array([filter_WL[0],filter_WL[1],filter_WL[2],filter_WL[3],filter_WL[4],filter_WL[5]])

   
    ### Iterating over until we are within 10% of the input counts
    ### Will print the value for the flux for each iteration

    while sum(flag) != 6:
        flux_top=[]
        for count in range(0,len(counts_array)):

            flux_top.append(counts_array[count]*factor[count])

        for x in range(len(flux_top)):
            
            new_spec = np.interp(filter_wave[x], new_WL, flux_top)
            
            new_counts[x] = np.trapz(new_spec*filter_array[x]*filter_wave[x]/hc,filter_wave[x])

            factor = map(truediv, flux_top, new_counts)
            # print(factor)
	    print(new_counts)
            if abs(new_counts[x] - counts_array[x]) <= 0.01*counts_array[x]:
                flag[x] = 1
            else:
                flag[x] = 0
#        print flux_top
    print(new_counts)
#    return(flux_top);
    return(new_spec);


