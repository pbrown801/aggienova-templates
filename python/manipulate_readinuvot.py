import os
import pandas as pd
import numpy as np
from astropy.io import fits

# Create Dataframe out of the data
def read_data(snname):
    lines = [] 
    data = open(os.path.join('..','input',snname + '_uvotB15.1.dat'), 'r')
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
    return df[['Filter', 'MJD[days]', 'Rate[c/s]',  'RateErr[c/s]']], ['Filter', 'MJD[days]', 'Rate[c/s]',  'RateErr[c/s]']

# Manipulates the input dataframe to combine each of the 6 bands with common times
def manipulate(snname_df, cols, avg):
    MJD = []
    MAG = []
    combined_lists=[]
    df_groups = []
    combined_groups = []
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
    # Combine each of the same indexed lines in each group so that we have the similar timed row data from each band group in a list
    for i in range(len(df_groups[0])):
        temp_combined = []
        for j in range(len(df_groups)):
            temp_combined.append(df_groups[j][i])
        # Create a dataframe temporaily to compute avg time values for the similar MJD times for the different bands
        df2=pd.DataFrame(temp_combined, columns=cols)
        MJD.append(np.average(df2['MJD[days]'])) 
        combined_groups.append(temp_combined)
    if (avg.upper() == 'Y'): # Change all the similar times for each row to a average time
        counts_array_list = []
        for i in range(len(combined_groups)):
            counts_array_list_temp = []
            for j in range(len(combined_groups[i])):
                combined_groups[i][j][1]=MJD[i]
                # Create dataframe like countsarray file output from observedmagstocounts.py
                if j==0:
                    counts_array_list_temp.append(combined_groups[i][j][1])
                counts_array_list_temp.append(combined_groups[i][j][2])
                counts_array_list_temp.append(combined_groups[i][j][3])
            counts_array_list.append(counts_array_list_temp)
    counts_array = pd.DataFrame(counts_array_list, columns = cols_counts_array)
    # Combine all the different timed data for each band into a list
    for lists in combined_groups:
        combined_lists.append(lists)
    return combined_lists, counts_array
    

def uvot(sn_name, avg_time):
    df, cols=read_data(sn_name)
    combined_data, counts_array=manipulate(df, cols, avg_time)
    # print(counts_array)
    counts_array.to_csv('../input/'+sn_name+'_uvot_countsarray'+'.csv', index=False)
    return combined_data

# if __name__ == "__main__":
#     uvot('SN2005cs', 'y')