import os
import pandas as pd
import numpy as np
from astropy.io import fits

# Create Dataframe out of the data
def read_data(sn_name):
    lines = [] 
    try:
        data = open(os.path.join('..','input',sn_name + '_uvotB15.1.dat'), 'r')
    except FileNotFoundError:
        print("File is not in input directory or is not a uvot file.")
        exit()
    for line in data:
        # Ignore comments
        if line[0]!= '#': 
            lines.append(line.strip().split()) # strip empty spaces at beginning and end of string and split by space to create a list of 12 data values
    # columns of dataframe
    columns=['Filter', 'MJD[days]', 'Mag', 'MagErr', '3SigMagLim', '0.98SatLim[mag]', 'Rate[c/s]', 'RateErr[c/s]', 'Ap[arcsec]', 'Frametime[s]', 'Exp[s]', 'Telapse[s]']
    # create dataframe from lists of lines
    df=pd.DataFrame(lines, columns=columns)
    # convert all numeric columns to float. NULL becomes NaN
    for i in columns[1:]:
        df[i]=pd.to_numeric(df[i], errors='coerce')
    # return columns that are needed for script
    return df[['Filter', 'MJD[days]', 'Mag', 'MagErr', 'Rate[c/s]',  'RateErr[c/s]']], ['Filter', 'MJD[days]', 'Mag', 'MagErr', 'Rate[c/s]',  'RateErr[c/s]'], min(df['MJD[days]'])

# Manipulates the input dataframe to combine each of the 6 bands with common times
def manipulate(snname_df, cols, avg):
    MJD = []
    df_groups = []
    combined_groups = []
    counts_combined_lists=[]
    mags_combined_lists=[]
    cols_counts_array = ['Time (MJD)']

    # Split into groups by filter
    snname_df=snname_df.groupby(['Filter'])
    filters = [f for f in snname_df.groups]
    filters_err = [str(f)+"err" for f in snname_df.groups]
    for i in range(len(filters)):
        cols_counts_array.append(filters[i])
        cols_counts_array.append(filters_err[i])
    # Sort by time 
    groups=[snname_df.get_group(x).sort_values(by=['MJD[days]']) for x in snname_df.groups]
    # Convert dataframe to list for easier manipulation. 
    # Creates a 3d list of each group of band with its own row of data values from the input data
    for df in groups:
        df_groups.append(df.values.tolist())

    # Get index of each column
    filter_idx=groups[0].columns.get_loc('MJD[days]')
    MJD_idx=groups[0].columns.get_loc('MJD[days]')
    count_rate_idx=groups[0].columns.get_loc('Rate[c/s]')
    count_rate_err_idx=groups[0].columns.get_loc('RateErr[c/s]')
    mag_idx=groups[0].columns.get_loc('Mag')
    mag_err_idx=groups[0].columns.get_loc('MagErr')
    # Combine each of the same indexed lines in each group so that we have the similar timed row data from each band group in a list
    for i in range(len(df_groups[0])):
        temp_combined = []
        for j in range(len(df_groups)):
            temp_combined.append(df_groups[j][i])
        # Create a dataframe temporaily to compute avg time values for the similar MJD times for the different bands
        df2=pd.DataFrame(temp_combined, columns=cols)
        MJD.append(np.average(df2['MJD[days]'])) 
        combined_groups.append(temp_combined)
    # print(combined_groups)
    if (avg.upper() == 'Y'): # Change all the similar times for each row to a average time
        counts_array_list = []
        mags_array_list = []
        for i in range(len(combined_groups)):
            counts_array_list_temp = []
            mags_array_list_temp = []
            for j in range(len(combined_groups[i])):
                combined_groups[i][j][1]=MJD[i]
                # Create dataframe like countsarray file output from observedmagstocounts.py
                if j==0:
                    counts_array_list_temp.append(combined_groups[i][j][MJD_idx])
                    mags_array_list_temp.append(combined_groups[i][j][MJD_idx])
                mags_array_list_temp.append(combined_groups[i][j][mag_idx])
                mags_array_list_temp.append(combined_groups[i][j][mag_err_idx])
                counts_array_list_temp.append(combined_groups[i][j][count_rate_idx])
                counts_array_list_temp.append(combined_groups[i][j][count_rate_err_idx])
            counts_array_list.append(counts_array_list_temp)
            mags_array_list.append(mags_array_list_temp)

    counts_array = pd.DataFrame(counts_array_list, columns = cols_counts_array)
    mags_array = pd.DataFrame(mags_array_list, columns = cols_counts_array)

    # Combine all the different timed data for each band into a list
    for lists in combined_groups:
        temp_lists_counts = []
        temp_lists_mags = []
        for l in lists:
            band= l[filter_idx]
            time = l[MJD_idx]
            mag=l.pop(mag_idx)
            mag_err=l.pop(mag_err_idx-1)
            temp_lists_mags.append([band, time, mag, mag_err])
            temp_lists_counts.append(l)
        counts_combined_lists.append(temp_lists_counts)
        mags_combined_lists.append(temp_lists_mags)
    return counts_combined_lists, counts_array, mags_combined_lists, mags_array
    

def uvot(sn_name, avg_time):
    df, cols, earliest_obv=read_data(sn_name)
    counts_combined_lists, counts_array, mags_combined_lists, mags_array=manipulate(df, cols, avg_time)
    mags_array.to_csv('../output/MAGS/'+sn_name+'_magsarray.csv', index=False)
    counts_array.to_csv('../input/COUNTS/'+sn_name+'_countsarray.csv', index=False)
    return earliest_obv

if __name__ == "__main__":
    uvot('SN2005cs','y')