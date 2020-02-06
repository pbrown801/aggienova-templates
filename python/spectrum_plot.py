import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import math


def spectrum_plot(plots):
    plotAvgs = []
    
    for plot in range(len(plots)):
        # Open data file
        try:
            file = open('../output/' + plots[plot] + 'template.csv').readlines()
            row_count = sum(1 for row in file)
            print('Rows = ' + str(row_count))
        except OSError as err:
            print("Could not find template for supernova " + plots[plot] + ": {0}".format(err))

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
        sum = 0
        for i in range(len(wave)):
            log_fluxAvg.append( log_fluxTot[i] / log_fluxCount[i] )
            sum += log_fluxAvg[i]
        
        # Save the avg log(flux) to center line around
        plotAvgs.append(sum / len(wave))

        # Plot current line
        plt.plot(wave, log_fluxAvg, label='SN2007af')


    plt.legend()
    plt.savefig('../testing.png')
    plt.show()

spectrum_plot('This is a BS name')
spectrum_plot('SN2007af')