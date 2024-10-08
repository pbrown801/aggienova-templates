import numpy as np
import pandas as pd

# Function to parse the data from the file
def parse_data(file_path):
    columns = ['Filter', 'MJD', 'Mag', 'MagErr', '3SigMagLim', '0.98SatLim', 'Rate', 'RateErr', 'Ap', 'Frametime', 'Exp', 'Telapse']
    data = []

    # Open and read the file
    with open(file_path, 'r') as f:
        for line in f:
            # Ignore lines starting with '#' (comments)
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 12:  # Ensure correct number of columns
                filter_name, mjd, mag, mag_err, sig_lim, sat_lim, rate, rate_err, ap, frame_time, exp, telapse = parts
                # Handle 'NULL' entries as None
                rate = np.nan if rate == 'NULL' else float(rate)
                mjd = float(mjd)
                data.append([filter_name, mjd, rate, rate_err,telapse])

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(data,columns=['Filter','MJD','Rate','RateErr','Telapse'])  # Only use Filter, MJD, and Rate
    #print(df)
    return df


# Function to group data by MJD within the 0.15 MJD tolerance
def organize_by_mjd(df, tolerance=0.15):
    # Initialize an empty list to store rows
    result = []

    # Get unique MJDs
    unique_mjd = sorted(df['MJD'].unique())

    avgmjd_list=[]
    # Iterate through each unique MJD
    for mjd in unique_mjd:
        # Filter data within 0.15 days of the current MJD
        subset = df[np.abs(df['MJD'] - mjd) <= tolerance ]
        #subset = df[np.abs(df['MJD'] - mjd) <= tolerance or (((df['MJD'] - df['Telapse']/60/60/24/2) < mjd) and ((df['MJD'] + df['Telapse']/60/60/24/2) > mjd))]
        avgmjd=np.mean(subset['MJD'])
        #print(avgmjd)
        avgmjd_list.append(avgmjd)
    mjddf=pd.DataFrame(avgmjd_list)
    #print(mjddf)
    mjd_groups=sorted(mjddf[0].unique())
    

    
    # Iterate through each unique MJD
    for mjd in mjd_groups:
        # Filter data within 0.15 days of the current MJD
        subset = df[np.abs(df['MJD'] - mjd) <= tolerance]
        #print(subset)
        # Initialize a row with MJD and placeholders for each filter
        row = [mjd, None, None, None, None, None, None, None, None, None, None, None, None]  # MJD, UVW2, UVM2, UVW1, U, B, V
        
        # Fill in the count rates for each filter
        for _, entry in subset.iterrows():
            #print(entry)
            if entry['Filter'] == 'UVW2':
                row[1] = entry['Rate']
                row[2] = entry['RateErr']
            elif entry['Filter'] == 'UVM2':
                row[3] = entry['Rate']
                row[4] = entry['RateErr']
            elif entry['Filter'] == 'UVW1':
                row[5] = entry['Rate']
                row[6] = entry['RateErr']
            elif entry['Filter'] == 'U':
                row[7] = entry['Rate']
                row[8] = entry['RateErr']
            elif entry['Filter'] == 'B':
                row[9] = entry['Rate']
                row[10] = entry['RateErr']
            elif entry['Filter'] == 'V':
                row[11] = entry['Rate']
                row[12] = entry['RateErr']
        
        # Append the row to the result
        result.append(row)

    # Convert result to a numpy array for convenience
    result_array = np.array(result)
    return result_array


# Main function to run the program
def main(file_path):
    # Parse the data from the file
    df = parse_data(file_path)

    mjd_groups=group_mjds(df, tolerance=0.15)
    
    # Organize the data by MJD with the tolerance of 0.15 days
    result_array = organize_by_mjd(df)

    # Convert to a DataFrame for better visualization
    result_df = pd.DataFrame(result_array, columns=['MJD', 'UVW2', 'UVW2err', 'UVM2', 'UVM2err', 'UVW1', 'UVW1err', 'U', 'Uerr', 'B', 'Berr', 'V', 'Verr'])
    
    #print(result_df)
    return result_df

# Provide the path to your data file here
#file_path = '../input/SN2007af_uvotB15.1.dat'
result = main(file_path)

