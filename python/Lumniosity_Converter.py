import pandas as pd 
import numpy as np
import math

def Dm_to_Lum(sn_name):
    def Grab_Lum(Dist_mod, Flux):
        P_cm= 3.08567758128*10**(18)

        D_cm= 10**((Dist_mod/5)+1)*P_cm

        S_a= 4*np.pi*D_cm**2

        lum= Flux*S_a
        return lum
    
    idex= swift.loc[swift.isin([sn_name]).any(axis=1)].index.tolist()
    idex=idex[0]
    Dist_mod= swift['Dist_mod_cor'][idex]

    Lum= pd.Series(sn_templ.apply(lambda row: Grab_Lum(Dist_mod=Dist_mod, Flux= row['Flux']), axis=1))
    Lum=pd.DataFrame({'MJD': sn_templ['MJD'], 'Wavelength': sn_templ['Wavelength'], 'Luminosity': Lum.tolist()})

    return Lum

def Lum_conv(sn_name,output_file):
    global swift
    swift= pd.read_csv('../input/NewSwiftSNweblist.csv')

    global sn_templ
    '''Input desired template file name with Flux'''
    sn_templ= pd.read_csv(output_file)
    
    sn_name= sn_name.replace("_uvot","")
    '''Input name of supernovae'''
    lum_templ= Dm_to_Lum(sn_name)

    return lum_templ

