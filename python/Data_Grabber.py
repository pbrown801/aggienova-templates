# -*- coding: utf-8 -*-
'''
Created on Wed Oct  7 12:14:39 2020

@author: Alexander Crabtree
            acrabtree15@gmail.com
'''
import requests
import json
import pandas as pd
import numpy as np
import math
import sys
import itertools
import threading
import time
from astropy import units as u
#from astroquery.irsa_dust import IrsaDust          OLD
from astroquery.ipac.irsa.irsa_dust import IrsaDust     #NEW
from astropy.coordinates import Angle,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from bs4 import BeautifulSoup


import urllib3           #NEW - for verifying the astrocats website/passing the SSL certificate verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)     #NEW


#for future updates, may consider wrapping function/s with .ThreadPoolExecutor or something similar to get faster output terminal time
    #as of last run, took around ~4hrs to collect current data

def getLink(name):
    '''
    Grabs the link from this site for the Host name of supernovae in CSV,
    returns the parsed page
    '''
    try:
        link = "http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?"
        inputs = {'objname': name,
				'extend': 'no',
				'hconst': '73.04',
				'omegam': '0.27',
				'omegav': '0.73',
				'corr_z': '1',
				'out_csys': 'Equatorial',
				'out_equinox': 'J2000.0',
				'obj_sort': "RA or Longitude",
				'of': 'pre_text',
				'zv_breaker': '30000.0',
				'list_limit':'10',
				'img_stamp': 'YES'}
        #NEW: added timeout=10 so it wont stay forever on one thing if it freezes
        page = requests.get(link, params = inputs, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    #except requests.ConnectionError:
    #NEW: using except Exception to catch timeouts and errors
    except Exception: 
        soup = ''
        return soup

'''
Takes parsed page from getlink and searches for all velocites listed below
then returns the data.
'''
def scrapeValues(soup):
	
    try:
        soup = soup.find("a", attrs={'name':'DerivedValues_0'})
        velocities = soup.next_sibling.next_sibling.next_sibling.find("pre")
        Helio = list(velocities.children)[2]
        VGS = list(velocities.children)[16]
        Helio = Helio.lstrip('\n')
        VGS = VGS.lstrip('\n')
        Hvals = [int(s) for s in Helio.split() if s.isdigit()]
        VGSVals = [int(s) for s in VGS.split() if s.isdigit()]
        vels = [Hvals[0],Hvals[1],VGSVals[0],VGSVals[1]]
        return vels
    except: 
        vels = [np.nan,np.nan,np.nan,np.nan]
        return vels

def get_coords(gals):
    """
    Takes list of galaxies and looks up their coordinates by name.
    If no name found: warn, skip, remove galaxy from list

    Returns:
        gals: list of galaxies minus those that weren't found
        start_coord: list of coordinates corresponding to center of galaxies in 'gals'
    """
    start_coord = []
    #bar = FillingCirclesBar('Loading galaxies', max = len(gals))
    try:
        tempCoord = SkyCoord.from_name(str(gals), frame = 'icrs')
        start_coord= tempCoord
            #bar.next()
    except NameResolveError:
        #if gals != str(''):
            #print('\nSkipping',gals,'because it couldn\'t be found.')
            #start_coord= ''
        #else:
            start_coord= np.nan
    #bar.finish()
    return(start_coord)

def coord_breakup(coord):
    """
    Breaks up a coordinate into its components
    """
    if pd.isna(coord) == True:
        ra = np.nan
        dec = np.nan
        return ra, dec
    else:
        ra = Angle(coord.ra.hour,unit = u.hour)
        dec = coord.dec
        return ra, dec


def getredshift(soup):
    '''
    Takes parsed page from getlink and searches for redshift then returns that data
    '''
    try:
        soup = soup.find("a", attrs={'name':'BasicData_0'})
        soup = soup.next_sibling.next_sibling.next_sibling.find("pre")
        redshift = list(soup.children)[0]
        # print(redshift)
        redshift = str(redshift).split("Redshift",1)[1]
        # print(redshift)
        redshift = redshift.split(":",1)[1]
        redshift = redshift.split(" +",1)[0].strip(' ')
        return(redshift)
    except:
        redshift = np.nan
        return redshift
   

def Morphology(soup):
    '''
    Takes parsed page from getlink and searches for morphology then returns the data
    '''
    try:
        soup = soup.find("a", attrs={'name':'BasicData_0'})
        morphology = soup.next_sibling.next_sibling.next_sibling.find("pre")
        morphology = list(morphology.children)[2]
        morphology = (morphology.split(": ",4)[4]).rstrip()
        return morphology
    except:
        morphology = np.nan
        return morphology


def LatLong(soup):
    '''
    Takes parsed page from getlink and searches for Latitude and Longitude then returns the data
    '''
    try:
        soup = soup.find("a", attrs={'name':'Positions_0'})
        coords = soup.next_sibling.next_sibling.find("pre")
        coords = list(coords.children)[4]
        coords = (coords.split("Galactic ",1)[1]).lstrip()
        long, lat = str(coords.split()[0]), str(coords.split()[1])
 
        return long, lat
    except:
        long, lat= np.nan,np.nan
        return long, lat  
 


def SN_host_ra_dec():
    def jprint(obj):
        '''
        Used to interpret the data from astrocats catalog
        '''
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    '''
    Requests data ra, dec, and host data of all supernovae in astrocats catalog
    '''
    sn_data= requests.get("https://api.astrocats.space/catalog/ra+dec+host?first", verify=False)  #NEW (verify=False)
    sn_catalog= sn_data.json()

    def SNHost(SNname):
        '''
        Checks if any CSV Supernova names are in astrocats catalog
        If yes returns Host Name data, If no returns nan value
        '''
        
        if SNname in sn_catalog:
            try:
                host_names= sn_catalog[SNname]['host']['value']
            except Exception:
                host_names= np.nan
        else:
            host_names= np.nan

        return host_names

    def SNRa(SNname):
        '''
        Checks if any CSV Supernova names are in astrocats catalog
        If yes returns Ra data, If no returns nan value
        '''
        
        if SNname in sn_catalog:
            try:
                snra= "'%s" % sn_catalog[SNname]['ra']['value']
            except Exception:
                snra= np.nan
        else:
            snra= np.nan
        return snra

    def SNDec(SNname):
        '''
        Checks if any CSV Supernova names are in astrocats catalog
        If yes returns Dec data, If no returns nan value
        '''
        
        if SNname in sn_catalog:
            try:
                sndec= sn_catalog[SNname]['dec']['value']
            except Exception: #if no dec value input what is given for dec
                sndec= np.nan
        else:
            sndec= np.nan
        return sndec
        
    '''
    The next 3 lines uses pandas apply function and lambda function to quickly
    parse supernovae names into the 3 above functions and saves data to
    relavent columns in CSV
    '''

    swift["HostName"]= swift.apply(lambda row: SNHost(row['SNname']) if pd.isna(row['HostName']) else row['HostName'], axis=1)
    swift["SNra"]= swift.apply(lambda row: SNRa(row['SNname']) if pd.isna(row['HostName']) else row['SNra'], axis=1)
    swift["SNdec"]= swift.apply(lambda row: SNDec(row['SNname']) if pd.isna(row['HostName']) else row['SNdec'], axis=1)


def GrabSNtypes():
    def SNtype(SNname):
        '''
        Takes Supernovae names from CSV and looks them up in the URL below
        Then parses the page for the supernovae type and returns it
        '''
        
        url = "https://www.wis-tns.org/object/"+SNname

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            sn_type= soup.find_all('div', class_= 'value')
            sn_type= sn_type[1].get_text()
            if str('---') == sn_type:
                sn_type= np.nan
            else:
                sn_type= sn_type.replace('|'.join(['SN']), '')
        except Exception:
            sn_type= np.nan
        ''' 
        Also collects any Host names not found in SN_host_ra_dec() function
        '''
        try:
            sn_host= soup.find_all('div', class_= 'field field-hostname')
            sn_host= sn_host[0].span.next_sibling.text

        except Exception:
            sn_host= np.nan


        return sn_host, sn_type

    def SNtype_empty(SNname):
            ''' 
            Returns empty nan series if condition is met
            '''
            sn_type, sn_host= np.nan, np.nan
            return sn_host, sn_type


    swift_temp= pd.DataFrame({'SNname':swift['SNname'], 'HostName':swift['HostName'], 'type':swift['type']})
    rep= '|'.join(['SN'])
    swift_temp['SNname']= swift_temp['SNname'].str.replace(rep, '')

    sntype= pd.Series(swift_temp.apply(lambda row: SNtype(row['SNname']) if pd.notna(row['SNname']) and (pd.isna(row['type']) or pd.isna(row['HostName'])) else SNtype_empty(row['SNname']), axis=1))
    sntype= pd.DataFrame(sntype.tolist(), columns=['HostName', 'type'], index=sntype.index)
    sntype= sntype.replace({r'^\s*$'}, np.nan, regex=True)
    return sntype


def getAVbest(inputcoordinates):
    '''
    Coordinates are input as a single string. Output is the recommended Av value for MW reddening, error, and reference
    '''
    
    #inputcoordinates = sys.argv[1]
    testCoords = SkyCoord(inputcoordinates,frame='fk5')
    #print('\n-----\nReading input files...')
    inFile = 'Brown_Walker_table_1.dat'
    inTable = pd.read_csv(inFile,header=None,delimiter=' ')
    ra = Angle(inTable.iloc[:,1])
    dec = Angle(inTable.iloc[:,2])
    sourceCoords = SkyCoord(ra,dec,frame='fk5')
    
    #print('Calculating separation from table coordinates')
    separations = testCoords.separation(sourceCoords).arcminute
    # compare to the distances in the table
    within = np.less(separations,inTable.iloc[:,3])
    
    # Are any of the input coordinates within the tabulated distance 
    # of the coordinates in the table?
    correctedAV = np.where(within,inTable.iloc[:,4],None) #get calculated value
    fix=any(within)
    #print('fix?',fix)
    
    if fix:
        AV = next((item for item in correctedAV if item is not None),None)
        correctedAVerr = np.where(within,inTable.iloc[:,5],None) #get calculated val
        newAVerr = next((item for item in correctedAVerr if item is not None),None)
        AVerr = math.sqrt((int(float(newAVerr)))**2+(int(AV)*0.1)**2)
        sources=np.where(within,inTable.iloc[:,6],None)
        source = next((item for item in sources if item is not None),None)+",S_F_2011"
        
    if not fix:
        AVtable = IrsaDust.get_extinction_table(testCoords,show_progress = False)
        AV=AVtable['A_SandF'][2]
        AVerr = AV*0.1
        source = 'S_F_2011'

    #print(AV, AVerr, source)
    return (AV, AVerr, source)


def AV_best():
    def AV_empty(Ra, Dec):
        ''' 
        Returns empty nan values if condition is met
        '''
        AV, AVerr, AVsour= np.nan, np.nan, np.nan
        return AV, AVerr, AVsour
    def GrabAVbest(Ra,Dec):
        '''
        Takes Supernovae Ra,Dec data and puts in in the right format before
        runing it through the getAVbest function, if there is an Exception
        returns nan values
        '''
        ra_fix, dec_fix = Ra, Dec
        ra_fix= ra_fix.replace("'", "")
        combined= SkyCoord(ra=ra_fix, dec=dec_fix, unit=(u.hour, u.deg)).to_string('hmsdms')
        try:
            AV, AVerr, AVsour= getAVbest(combined)
        except Exception:
            AV, AVerr, AVsour= np.nan, np.nan, np.nan
        
        return AV, AVerr, AVsour

    avdata= pd.Series(swift.apply(lambda row: GrabAVbest(row['SNra'], row['SNdec']) if (pd.isna(row['AV']) and pd.notna(row['SNra'])) else AV_empty(row['SNra'], row['SNdec']), axis= 1))
    avdata= pd.DataFrame(avdata.to_list(), columns=['AV', 'AVerr', 'AVsour'], index=avdata.index)
    avdata= avdata.replace({r'^\s*$'}, np.nan, regex=True)

    return avdata


def AllHostData():
    '''
    Collects all data on Host names by running appropriate data through related 
    function or empty function.
    '''
    #NEW, total calcs total number of rows in data set and stores it
    total = len(swift)
    
    def host_coords(HostName, idx, sn_name):
        #NEW, print for tracking progress
        print(f"[{idx+1}/{total}] Host coords: '{HostName}' (SN: {sn_name})")
        ra,dec= coord_breakup(get_coords(HostName))
        return ra,dec
    def host_coords_empty(HostName):
        ra,dec= np.nan, np.nan
        return ra, dec
    
    def host_lat_long(HostName, idx, sn_name):
        #NEW, print for tracking progress
        print(f"[{idx+1}/{total}] NED Lat/Long: '{HostName}' (SN: {sn_name})")
        gal_link=getLink(HostName)
        lon,lat= LatLong(gal_link)
        return lon, lat
    def host_lat_long_empty(HostName):
        lon,lat= np.nan, np.nan
        return lon, lat
    
    def gethostredshift(HostName, idx, sn_name):
        print(f"[{idx+1}/{total}] Host Redshift: '{HostName}' (SN: {sn_name})")
        gal_link=getLink(HostName)
        red= getredshift(gal_link)
        return red
    def gethostredshift_empty(HostName):
        red= np.nan
        return red
    
    def morphology(HostName, idx, sn_name):
        print(f"[{idx+1}/{total}] Host Morphology: '{HostName}' (SN: {sn_name})")
        gal_link=getLink(HostName)
        morph= Morphology(gal_link)
        return morph
    def morphology_empty(HostName):
        morph= np.nan
        return morph
    
    def velocities(HostName, idx, sn_name):
        print(f"[{idx+1}/{total}] Host Velocities: '{HostName}' (SN: {sn_name})")
        gal_link=getLink(HostName)
        vels= scrapeValues(gal_link)
        return vels
    def velocities_empty(HostName):
        vels= np.nan, np.nan, np.nan, np.nan
        return vels
    
    '''
    All 5 lines uses pandas apply and the lambda function with an if else staments inside. Checks if HostName cell is not empty
    and checks specfic cell is empty for all cases. If so runs them through their corresponding functions if not runs them
    through their corresponding empty functions
    '''

    
    print("\n--- Fetching Host Coordinates ---")
    coord = pd.Series(swift.apply(lambda row: host_coords(row['HostName'], row.name, row['SNname']) if (pd.notna(row['HostName']) and pd.isna(row['HostRa'])) else host_coords_empty(row['HostName']), axis=1))
    coord = pd.DataFrame(coord.tolist(), columns=['HostRa', 'HostDec'], index=coord.index)

    print("\n--- Fetching NED Lat/Long Metadata ---")
    lon_lat = pd.Series(swift.apply(lambda row: host_lat_long(row['HostName'], row.name, row['SNname']) if (pd.notna(row['HostName']) and pd.isna(row['Long'])) else host_lat_long_empty(row['HostName']), axis=1))
    lon_lat = pd.DataFrame(lon_lat.tolist(), columns=['Long', 'Lat'], index=lon_lat.index).replace({r'^\s*$': np.nan}, regex=True)

    print("\n--- Fetching Host Redshifts ---")
    reds = pd.Series(swift.apply(lambda row: gethostredshift(row['HostName'], row.name, row['SNname']) if (pd.notna(row['HostName']) and pd.isna(row['redshift'])) else gethostredshift_empty(row['HostName']), axis=1))
    reds = pd.DataFrame(reds.tolist(), columns=['redshift'], index=reds.index).replace({r'^\s*$': np.nan}, regex=True)

    print("\n--- Fetching Host Morphology ---")
    morp = pd.Series(swift.apply(lambda row: morphology(row['HostName'], row.name, row['SNname']) if (pd.notna(row['HostName']) and pd.isna(row['Morphology'])) else morphology_empty(row['HostName']), axis=1))
    morp = pd.DataFrame(morp.tolist(), columns=['Morphology'], index=morp.index).replace({r'^\s*$': np.nan}, regex=True)

    print("\n--- Fetching Host Velocities ---")
    hvels = pd.Series(swift.apply(lambda row: velocities(row['HostName'], row.name, row['SNname']) if (pd.notna(row['HostName']) and pd.isna(row['host_velocity'])) else velocities_empty(row['HostName']), axis=1))
    hvels = pd.DataFrame(hvels.tolist(), columns=['host_velocity', 'host_vel_err', 'host_vel_corr', 'host_vel_corr_err'], index=hvels.index)

    all_data = pd.concat([coord, lon_lat, reds, morp, hvels], axis=1)
    return all_data



def Dist_mod():
    def Dist_mod_empty(hv, hv_err):
        '''
        Returns empty nan series if condition is met
        '''
        distance_mod_cor, distance_mod_cor_err = np.nan, np.nan
        return distance_mod_cor, distance_mod_cor_err
    def Hubble_flow_redshift(redshift):
        '''
        Takes host_velocity and host_vel_err data and returns distance modulus
        and distance modulus err in a series
        '''
        h0 = 73.04
        h0err = 1.04
        #NEW: theres an error here is just printing redshift and type right after,
            #TypeError: can't multiply sequence by non-int of type 'float'
        #so, redshift must be converted to float before the math calculations, and not computed as string
        
        #print(redshift)                        OLD
        #print(type(redshift))                  OLD
    # From Riess et al 2022 SH0ES result
        #hv=redshift*2.99*10.0**5.0             OLD
        #hv_err=0.1*hv                          OLD
            
        try:
            #NEW: redshift_val, moved hv and hv_err inside try
            redshift_val = float(redshift)
            hv=redshift*2.99*10.0**5.0
            hv_err=0.1*hv
            distance_mod_cor = 5*math.log(float(hv)/h0,10)+25 #hubble flow
            distance_mod_cor_err = math.sqrt(((5*float(hv_err))/(float(hv)*math.log(10,10)))**2+((5*200)/(float(hv)*math.log(10,10)))**2 + ((5*5.0)/(h0*math.log(10,10)))**2)
        except Exception:
            distance_mod_cor, distance_mod_cor_err = np.nan, np.nan

        return  distance_mod_cor, distance_mod_cor_err

    
    def Distance_mod_cor(hv, hv_err):
        '''
        Takes host_velocity and host_vel_err data and returns distance modulus
        and distance modulus err in a series
        '''
        h0 = 73.04
        h0err = 1.04
	# From Riess et al 2022 SH0ES result
        if pd.isna(hv_err):
            hv_err=0.1*hv
        try:
            distance_mod_cor = 5*math.log(float(hv)/h0,10)+25 #hubble flow
            distance_mod_cor_err = math.sqrt(((5*float(hv_err))/(float(hv)*math.log(10,10)))**2+((5*200)/(float(hv)*math.log(10,10)))**2 + ((5*5.0)/(h0*math.log(10,10)))**2)
        except Exception:
            distance_mod_cor, distance_mod_cor_err = np.nan, np.nan

        return  distance_mod_cor, distance_mod_cor_err

    dist= pd.Series(swift.apply(lambda row: Distance_mod_cor(row['host_vel_corr'], row['host_vel_corr_err']) if pd.notna(row['host_vel_corr']) else Hubble_flow_redshift(row['redshift']) if (pd.isna(row['host_vel_corr']) and pd.notna(row['redshift'])) else Dist_mod_empty(row['host_velocity'], row['host_vel_err']), axis=1))
    dist= pd.DataFrame(dist.tolist(), columns=['Hubble_dm', 'Hubble_dm_err'], index=dist.index)
    dist= dist.replace({r'^\s*$'}, np.nan, regex=True)
    return dist

def fixtypes(type):
    t=1
    newtype=' '
    if type == 'Ia' or type == 'Ia-CSM' or type == 'Ia-SC' or type == 'Ia-99by' or type == 'Ia-pec?' or type == 'Ia-99aa':
        newtype = 'Ia'
    

    if type == 'Iax' or type == 'Ia-02cx' or type == 'Ia-02cx-like':
        newtype='Iax'


    if  type == 'Ib' or type == 'SNIb'  or type == 'Ic' or type == 'SNIc' or type == 'Ic' or type == 'SNIc' or type == 'Ib/c' or type == 'SNIb/c'  or type == 'Ibn' or type == 'SNIbn' or  type == 'SLSN-I' or type == 'SLSNI'  or  type == 'Ic-BL' or type == 'SNIc-BL' or type == 'Ic-bl':
        newtype='Ib/c'


    if   type == 'IIP' or type == 'SNIIP' or type == 'SNII'  or  type == 'IIL' or type == 'SNIIL' or type == 'SNII'  or  type == 'SLSN-II' or  type == 'SLSNII'  or  type == 'IILn' or type == 'SNIIn' or type == 'SNII'  or  type == 'IIb' or type == 'SNIIb' or type == 'SNIIb'  or  type == 'SLSN-II' or  type == 'SLSNII' :
        newtype='II'



    return type, newtype

def SNdates(SNname):
    '''
    Takes Supernovae names from CSV and looks them up in the URL below
    Then parses the page for relevant information to Supernova Discovery,
    Last non-detection, and recieved date.
    '''
    url = "https://www.wis-tns.org/object/"+SNname+"/discovery-cert"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    sn_data= soup.find_all('span', class_='underline')
    
    disc_date= sn_data[0].find_next_sibling('span').text
    disc_string= 'Discovery date: '

    lnd_date= sn_data[1].find_next_sibling('span').text
    lnd_string= 'Last non-detection date: '

    if disc_string in disc_date:
        disc_date= disc_date.replace(disc_string, '')
    
    if lnd_date in ['Archival info: DSS', 'Archival info: Other', 'Archival info: SDSS']:
        lnd_date= ''
        disc_date= "'" + disc_date
        
    else:
        if lnd_string in lnd_date:
            lnd_date= lnd_date.replace(lnd_string, '')
        disc_date= "'" + disc_date
        lnd_date= "'" + lnd_date

    return(disc_date, lnd_date)

def GrabDates():
    def GrabSNdates_empty(SNname):
        ''' 
        Returns empty nan series if condition is met
        '''
        disc,lnd= np.nan,np.nan
        return disc,lnd
    def GrabSNdates(SNname):
        '''
        Takes supernovae names and runs them through SNdates and returns a
        series with dates data
        '''
        try:
            disc,lnd= SNdates(SNname)
        except Exception:
            disc,lnd= np.nan,np.nan
            
        return disc,lnd

    '''
    Next 3 lines creates a supernovae list from our CSV except the SN in front of 
    most of the names are removed
    '''
    swift_temp= pd.DataFrame({'SNname':swift['SNname'], 'Discover':swift['Discover_date'], 'Last':swift['Last_non-detection_date']})
    rep= '|'.join(['SN'])
    swift_temp['SNname']= swift_temp['SNname'].str.replace(rep, '')

    dates= pd.Series(swift_temp.apply(lambda row: GrabSNdates(row['SNname']) if pd.notna(row['SNname']) and (pd.isna(row['Discover']) or pd.isna(row['Last'])) else GrabSNdates_empty(row['SNname']), axis=1))
    dates= pd.DataFrame(dates.tolist(), columns=['Discover_date', 'Last_non-detection_date'], index=dates.index)
    dates= dates.replace({r'^\s*$'}, np.nan, regex=True)

    return dates

def Best_Distances():
    def Distances_empty(host_vel, Hubble_dm, Hubble_dm_err, Hubble_dm_ref, SBF_dm, SBF_dm_err, SBF_dm_ref, Cep_dm, Cep_dm_err, Cep_dm_ref, TRGB_dm, TRGB_dm_err, TRGB_dm_ref):
        '''
        returns nans to series if there is no host_velocity value available
        '''
        best_dm, best_dm_err, best_dm_meth, best_dm_ref= np.nan, np.nan, np.nan, np.nan
        return best_dm, best_dm_err, best_dm_meth, best_dm_ref

    def Distances(host_vel, Hubble_dm, Hubble_dm_err, Hubble_dm_ref, SBF_dm, SBF_dm_err, SBF_dm_ref, Cep_dm, Cep_dm_err, Cep_dm_ref, TRGB_dm, TRGB_dm_err, TRGB_dm_ref):
        '''
        If there is a host_velocity value, checks if there are values for sbf_dist and cep_dist.
        If none for both returns dist_mod as Hubble flow distance.
        If SBF, returns sbf_dist as SBF.
        If Cepheid, returns cep_dist as Cepheid.
        '''
        try:
            if pd.isnull(Cep_dm)==True and pd.isnull(SBF_dm)==True:
                best_dm= Hubble_dm
                best_dm_err= Hubble_dm_err
                best_dm_meth= "HF"
                best_dm_ref= Hubble_dm_ref
            elif pd.isnull(Cep_dm)==True and pd.isnull(SBF_dm)==False:
                best_dm= SBF_dm
                best_dm_err= SBF_dm_err
                best_dm_method= "SBF"
                best_dm_ref= SBF_dm_ref
            else:
                best_dm= Cep_dm
                best_dm_err= Cep_dm_err
                best_dm_meth= "Cepheid"
                best_dm_ref= Cep_dm_ref
        
        except Exception:
                    best_dm, best_dm_err, best_dm_meth, best_dm_ref= np.nan, np.nan, np.nan, np.nan

        return best_dm, best_dm_err, best_dm_meth, best_dm_ref
        
    best_dist= pd.Series(swift.apply(lambda row: Distances(row['host_velocity'], row['Hubble_dm'], row['Hubble_dm_err'], row['Hubble_dm_ref'], row['SBF_dm'], row['SBF_dm_err'], row['SBF_dm_ref'], row['Cep_dm'], row['Cep_dm_err'], row['Cep_dm_ref'],row['TRGB_dm'], row['TRGB_dm_err'], row['TRGB_dm_ref']) if pd.notna(row['host_velocity']) else Distances_empty(row['host_velocity'], row['Hubble_dm'], row['Hubble_dm_err'], row['Hubble_dm_ref'], row['SBF_dm'], row['SBF_dm_err'], row['SBF_dm_ref'], row['Cep_dm'], row['Cep_dm_err'], row['Cep_dm_ref'],row['TRGB_dm'], row['TRGB_dm_err'], row['TRGB_dm_ref']), axis=1))
    best_dist= pd.DataFrame(best_dist.to_list(), columns=['best_dm', 'best_dm_err', 'best_dm_method', 'best_dm_ref'], index= best_dist.index)
    best_dist= best_dist.replace({r'^\s*$'},np.nan, regex=True)

    return best_dist


def set_best_dm():

    # The default method is the Hubble flow distance.  But if it has a Cepheid, SBF, or TRGB distances, it uses those in that priority (by setting them in reverse.)

    #New error found here: 
        #TypeError: Invalid value '['31.77' '32.16' '30.65' '31.45' '31.28' '31.74' '31.45' '33.07' '31.606'
    #error occurs bc code is trying to operate on a pandas DataFrame/Series of data type float64 using strings instead of floats
        #so, need to convert those strings to floats

    #NEW: converts string text into floating point numbers/float64
        #if an entry cant be converted to a number, the error coerce safely converts it into NaN
    #converts DM columns to float to avoid dtype mismatch errors
    dm_cols = ["Hubble_dm", "Hubble_dm_err", "SBF_dm", "SBF_dm_err", "TRGB_dm", "TRGB_dm_err", "Cep_dm", "Cep_dm_err"]
    for col in dm_cols:
        if col in swift.columns:
            swift[col] = pd.to_numeric(swift[col], errors='coerce')

    #ensures best_dm baseline numerical columns exist
    swift["best_dm"] = swift["Hubble_dm"]
    swift["best_dm_err"] = swift["Hubble_dm_err"]

    #set reference and method columns as object/string types
    swift["best_dm_ref"] = swift["Hubble_dm_ref"].astype(object) if "Hubble_dm_ref" in swift.columns else np.nan
    swift["best_dm_ref"] = swift["best_dm_ref"].astype(object)
    swift["best_dm_meth"] = "HF"
    swift["best_dm_meth"] = swift["best_dm_meth"].astype(object)

    #These determine and assign the best distance measurment for each host galaxy in data based on accuracy
    #1st is TRGB/tip of the red giant branch
    if "TRGB_dm" in swift.columns:
        mask_trgb = pd.notna(swift["TRGB_dm"])
        swift.loc[mask_trgb, "best_dm"] = swift.loc[mask_trgb, "TRGB_dm"]
        swift.loc[mask_trgb, "best_dm_err"] = swift.loc[mask_trgb, "TRGB_dm_err"]
        if "TRGB_dm_ref" in swift.columns:
            swift.loc[mask_trgb, "best_dm_ref"] = swift.loc[mask_trgb, "TRGB_dm_ref"]
        swift.loc[mask_trgb, "best_dm_meth"] = "TRGB"

    #2nd is SBF/surface brightness fluctuations, overrides TRGB if available
    if "SBF_dm" in swift.columns:
        mask_sbf = pd.notna(swift["SBF_dm"])
        swift.loc[mask_sbf, "best_dm"] = swift.loc[mask_sbf, "SBF_dm"]
        swift.loc[mask_sbf, "best_dm_err"] = swift.loc[mask_sbf, "SBF_dm_err"]
        if "SBF_dm_ref" in swift.columns:
            swift.loc[mask_sbf, "best_dm_ref"] = swift.loc[mask_sbf, "SBF_dm_ref"]
        swift.loc[mask_sbf, "best_dm_meth"] = "SBF"

    #3rd is Cephied, highest preference and overrides the other methods if it's available
    if "Cep_dm" in swift.columns:
        mask_cep = pd.notna(swift["Cep_dm"])
        swift.loc[mask_cep, "best_dm"] = swift.loc[mask_cep, "Cep_dm"]
        swift.loc[mask_cep, "best_dm_err"] = swift.loc[mask_cep, "Cep_dm_err"]
        if "Cep_dm_ref" in swift.columns:
            swift.loc[mask_cep, "best_dm_ref"] = swift.loc[mask_cep, "Cep_dm_ref"]
        swift.loc[mask_cep, "best_dm_meth"] = "Cep"
    

def main():
   
    '''A fun function'''
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rUpdating Now! ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        #NEW, commented this out, the print clears the screen everytime it's updated
        #print(chr(27) + "[2J")
        sys.stdout.write('\rDone!')

    global swift

    inputcsv='SortedFinalforSwiftSNyears2026.csv'
#   inputcsv='SwiftSNweblist2016PTF.csv'
#   inputcsv='SwiftSNweblist2016on.csv'
    '''
    This if-else statment asks if you want to update or add new supernovae values to CSV file
    '''
    choice_1= "U" #input("Would you like to add new supernovae names or just update current CSV? (Type: SN or U):")
    if choice_1 == str('U'):
        print("Updating CSV now!")

        ''' 
        This section soley updates the swift data, that is it checks for new data that is currently missing from the swift data.
        '''

        '''
        Next 4 lines are important to animate function
        '''
        done = False
        #print(chr(27) + "[2J")
        threader = threading.Thread(target=animate)
        threader.start()

        '''
        Reads in SwiftSN CSV and makes swift global
        '''
        print("read in file ", inputcsv)
        #swift= pd.read_csv(inputcsv)
        swift= pd.read_csv(inputcsv,on_bad_lines='warn',delimiter=',')
  
        '''
        Replaces all anon, Anon, AnonHost, and blanks with nan values
        '''
        print("replacing anons with nans")
        swift= swift.replace({r'anon',r'Anon',r'AnonHost', r'^\s*$'},np.nan, regex=True)

        '''
        Executes function that grabs host, ra, and dec data on supernovae
        '''
        
        print('retrieve coordinates')
        SN_host_ra_dec()

        '''
        Executes function that grabs host and type data on supernovae
        '''
        print('retrieve type and host')
        swift= swift.fillna(GrabSNtypes())

        '''
        Executes function that grabs AV, AVerr, and source data on supernovae
        '''
        print('Find the best Av')
        swift= swift.fillna(AV_best())

        '''
        Executes function that grabs lots of data on host galaxy of supernovae
        '''
        print('retrieve lots of host information')
        swift= swift.fillna(AllHostData())

        '''
        Executes function that calculates distance modulus data on supernovae
        '''
        print('calculate distances')
        swift_hubble= Dist_mod()
        swift= swift.drop(swift.columns.intersection(swift_hubble.columns), axis=1).join(swift_hubble)

    #    #reorders the Hubble_dm and Hubble_dm_err columns
   #     col_list=swift.columns.to_list()
  #      col_list[41:41]=col_list[-2:]
 #       col_list= col_list[:-2]
#        swift= swift.reindex(columns=col_list)


        '''
        Executes function that finds the best distances available for supernovae (HF, SBF, or Cepheid)
        '''
        set_best_dm()
        #swift.best_dm=swift.Hubble_dm
        #swift.loc[(pd.notna(swift["TRGB_dm"]),"best_dm")]=swift.loc[(pd.notna(swift["TRGB_dm"]),"TRGB_dm")]
        #swift.loc[(pd.notna(swift["SBF_dm"]),"best_dm")]=swift.loc[(pd.notna(swift["SBF_dm"]),"SBF_dm")]

        #swift.loc[(pd.notna(swift["Cep_dm"]),"best_dm")]=swift.loc[(pd.notna(swift["Cep_dm"]),"Cep_dm")]

#        swift_dist= Best_Distances()
#        swift= swift.drop(swift.columns.intersection(swift_dist.columns), axis=1).join(swift_dist)

#        #reorders the columns to put the best columns in front of the Hubble_dm and Hubble_dm_err columns
#        col_list=swift.columns.to_list()
#        col_list[41:41]=col_list[-4:]
#        col_list= col_list[:-4]
#        swift= swift.reindex(columns=col_list)
        ##### issue: what if column numbers change?

        print('find detection dates')
        '''
        Executes function that grabs detection and last non detection dates on supernovae
        '''
        swift= swift.fillna(GrabDates())

        '''
        Fills nan values back with blanks then saves csv to either same file or
        your pick of file name
        '''
        swift=swift.fillna('')

        print('Save the csv file')

        swift.to_csv('New'+inputcsv, index= False)

        '''Last segment of animate function that makes the animation run'''
        done= True

    else:

        '''
        Because of how the functions are set up, in this section I renamed the swift dataframe to swift_merge so that
        I could use the swift name for the dataframe for the inputed SNe Names, this way it updates the info on the
        new names quicker.
        '''
        swift_merge= pd.read_csv(inputcsv)

        swift= pd.DataFrame(columns= swift_merge.columns)

        choice_2=""

        while choice_2 != str('Done'):
            SN=""
            SN= input("Type supernova name:")
            new_SN= pd.DataFrame([str(SN)], columns= ['SNname'])
            swift= pd.concat([new_SN, swift]).reset_index(drop = True)
            choice_2= input("Press enter to input another name or type Done to start update! :")
        print("Updating CSV now!")

        '''
        Next 4 lines are important to animate function
        '''
        done = False
        print(chr(27) + "[2J")
        threader = threading.Thread(target=animate)
        threader.start()

        '''
        Executes function that grabs host, ra, and dec data on supernovae
        '''
        print('run SN_host_ra_dec')
        SN_host_ra_dec()

        '''
        Executes function that grabs host and type data on supernovae
        '''
        print('run swift.fillna(GrabSNtypes())')
        swift= swift.fillna(GrabSNtypes())

        '''
        Executes function that grabs AV, AVerr, and source data on supernovae
        '''
        print('run swift.fillna(AV_best())')
        swift= swift.fillna(AV_best())

        '''
        Executes function that grabs lots of data on host galaxy of supernovae
        '''
        print('run swift.fillna(AllHostData)')
        swift= swift.fillna(AllHostData())

        '''
        Executes function that calculates distance modulus data on supernovae
        '''
        print('run swift_hubble')
        swift_hubble= Dist_mod()
        swift= swift.drop(swift.columns.intersection(swift_hubble.columns), axis=1).join(swift_hubble)

#        #reorders the Hubble_dm and Hubble_dm_err columns
#        col_list=swift.columns.to_list()
#        col_list[41:41]=col_list[-2:]
#        col_list= col_list[:-2]
#        swift= swift.reindex(columns=col_list)

        '''
        Executes function that grabs detection and last non detection dates on supernovae
        '''
        print('run swift.fillna')
        swift= swift.fillna(GrabDates())

        '''
        Executes function that finds the best distances available for supernovae (HF, SBF, or Cepheid)
        '''
        print('run swift.drop')
        swift_dist= Best_Distances()
        swift= swift.drop(swift.columns.intersection(swift_dist.columns), axis=1).join(swift_dist)

#        #reorders the columns to put the best columns in front of the Hubble_dm and Hubble_dm_err columns
#        col_list=swift.columns.to_list()
#        col_list[41:41]=col_list[-4:]
#        col_list= col_list[:-4]
#        swift= swift.reindex(columns=col_list)

        ''' 
        Flips the order of the swift dataframe to ensure SN names given first appear at the top.
        '''

        print('run swift.reindex')
        swift= swift.reindex(index=swift.index[::-1])

        ''' 
        Merges the updated new SNe name info with the rest of the swift data
        '''
        print('run pd.concat')
        swift= pd.concat([swift, swift_merge], sort=False).reset_index(drop = True)

        '''
        Fills nan values back with blanks then saves csv to either same file or 
        your pick of file name
        '''
        print('run swift.fillna')
        swift=swift.fillna('')

        swift.to_csv('New'+inputcsv, index= False)

        '''Last segment of animate function that makes the animation run'''
        done= True

if __name__ == "__main__":  main()


#####  

