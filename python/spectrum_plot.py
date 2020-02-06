import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import math

"""
Purpose: plots the log(flux) + c vs. wavelength for one or more supernova
Parameters: 
    plots  = list of supernova names to plot, <supernovaName>templete.csv MUST exist in output
    spread = count to seperate plots by to increase readability (default = 3)
Example: spectrum_plot(['SN2007af', 'some_supernova'], 10)
"""
def spectrum_plot(plots, spread = 3):
    plotAvgs = []
    
    for p in range(len(plots)):
        # Open data file
        try:
            file = open('../output/' + plots[p] + 'template.csv').readlines()
            row_count = sum(1 for r in file)
            #print('Rows = ' + str(row_count))
        except OSError as err:
            print("Could not find template for supernova " + plots[p] + ": {0}".format(err))
            exit

        # Read in output data
        wave = []
        log_fluxTot = [] # Sums of log(flux) vals for each given wave
        log_fluxCount = [] # Count of total times a wave's flux val has been added to Tot
        log_fluxAvg = [] # Avg of all given flux vals for each given wave
        for row in range(1, row_count):
            r = file[row].split(',')
            if(float(r[2]) > 0):
                #print('Adding ' + r[1] + ', ' + str(math.log(float(r[2]), 10)))
                if(not float(r[1]) in wave):
                    wave.append(int(r[1]))
                    log_fluxTot.append( math.log(float(r[2]), 10) )
                    log_fluxCount.append(1)
                else:
                    waveInd = wave.index(int(r[1]))
                    log_fluxTot[waveInd] += math.log(float(r[2]), 10)
                    log_fluxCount[waveInd] += 1
        
        # Compute avg. flux values and find avg total value for 'centering'
        plot_sum = 0
        for i in range(len(wave)):
            log_fluxAvg.append( log_fluxTot[i] / log_fluxCount[i] )
            plot_sum += log_fluxAvg[i]
        
        # Save the avg log(flux) to center line around
        plotAvgs.append(plot_sum / len(wave))
        #print("Avg for supernova " + plots[p] + " = " + str(plotAvgs[p]))

        # Constant value to add to cur plot for spreading (each should be centered around multiples of 3)
        c = spread*(p+1) - plotAvgs[p]

        # Add c to plot
        for i in range(len(wave)):
            log_fluxAvg[i] += c

        # Plot current line
        plt.plot(wave, log_fluxAvg, label=plots[p])


    plt.legend()
    plt.xlabel('Wavelength (angstroms)')
    plt.ylabel('log(flux) + constant')

    # Save figure
    filePath = '../output/'
    for plotName in plots:
        filePath += plotName + '_'
    plt.savefig(filePath + 'logFlux_vs_wavelength.png')
    plt.show()
# END FUNC

spectrum_plot(['SN2007af'])