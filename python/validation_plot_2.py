from speccounts import specin_countsout
import pandas as pd
import numpy as np

def main(sn_name):
    with open("../input/vega.dat") as f:
        f.readline()
        f.
    # output_spectrum = pd.read_csv("../output/"+sn_name+"_template.csv")
    outputMJD =np.array(output_spectrum["MJD"])
    outputWavelength=np.array(output_spectrum["Wavelength"])
    outputFlux=np.array(output_spectrum["Flux"])
    outputCounts, outputMags=specin_countsout(outputWavelength,outputFlux)
    print("Counts",outputCounts)
    print("Mag",outputMags)

    

if __name__ == "__main__":
    main("SN2005cs_uvot")
