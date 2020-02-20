# DOES NOT WORK CURRENTLY
# Download sn2005cs fits IMG filter files from https://archive.stsci.edu/prepds/sousa/
# Put into separate folder FITS IMG


import os
import pandas as pd
from matplotlib.colors import LogNorm
from astropy.io import fits
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

f = []
date_obs = [[], [], [], [], [], []]
exp = [[], [], [], [], [], []]
res = {}
dict1 = {}
dict2 = {}
obs_idx = []

cur_path = os.path.dirname(__file__)

new_path = os.path.relpath('.\\FITS_IMG', cur_path)
cur = os.getcwd()
# Path = "../FITS IMG"
filelist = os.listdir(cur)
for x in filelist:
    if x.endswith('.gz'):
        f.append(x)  # Gets the list of fits files
# print(f)  # For refrence of the order of the files.
for j in range(len(f)):
    with fits.open(f[j]) as imgbb:
        count = 0
        for i in imgbb:
            try:
                # Tries to append exposure to 2d list otherwise it passes.
                exp[j].append(imgbb[count].header['EXPOSURE'])
                # Same as exposure
                date_obs[j].append(imgbb[count].header['DATE-OBS'])
            except:
                pass
            count += 1

# Prints out a dataframe of the date obs and corresponding exposure of each folder
for i in range(len(date_obs)):
    for j in range(len(date_obs[i])):
        val = [0, 0, 0, 0, 0]
        val.insert(i, exp[i][j])
        dict1[date_obs[i][j]] = val
# Creating the dataframe using dict1 that makes the date obs the index.
df = pd.DataFrame.from_dict(dict1, orient='index', columns=[
                            'exp1', 'exp2', 'exp3', 'exp4', 'exp5', 'exp6']).sort_index(axis=0)
# Gets index from the data frame and appends to a array.
for i in range(len(df['exp1'])):
    obs_idx.append(df.index[i])

# Setting dataframe indexes to a series and adding a column for difference in time between to rows.
df.index.name = "Obs"
df.index = pd.to_datetime(df.index)
df['diff_time'] = df.index.to_series().diff()

# Combining rows with time difference less than 0 day 15 minutes.
# If a row has all 6 columns of Exposures then it appends to a final dictionary.
# The final dictionary has a key that is the first merged observation array with the last with the value being the merged list.
i = 0
while(i < len(df['diff_time'])-1):
    i += 1
    val = [0, 0, 0, 0, 0, 0]
    if (int(df['diff_time'][i].days == 0) and int(df['diff_time'][i].seconds)/60 < 15 and (i < len(df['diff_time'])-1)):
        start = df.index[i]
        while_counter = 0
    while(int(df['diff_time'][i].days == 0) and int(df['diff_time'][i].seconds)/60 < 15 and (i < len(df['diff_time'])-1)):
        for j in range(6):
            if(dict1[obs_idx[i-1]][j] != 0):
                val[j] = (dict1[obs_idx[i-1]][j])
            if(dict1[obs_idx[i]][j] != 0):
                val[j] = (dict1[obs_idx[i]][j])
        i += 1
        while_counter += 1

    count = 0
    for c in range(6):
        if (val[c] != 0):
            count += 1
    if count == 6:
        if i+while_counter < (len(df['diff_time'])-1):
            t = start + (0.5*(start-df.index[i+while_counter]))
            dict2[str(t.round('min'))] = val

# Creating the dataframe using dict2 that makes the date obs the index.
df2 = pd.DataFrame.from_dict(dict2, orient='index', columns=[
    'exp1', 'exp2', 'exp3', 'exp4', 'exp5', 'exp6']).sort_index(axis=0)

# Gets index from the data frame 2 and appends to an array.
obs_idx2 = []
for i in range(len(df2['exp1'])):
    obs_idx2.append(df2.index[i])

# Searches the original fits images files for the correct data for each observation date and each of the 6 exposures.
# The data is appended to a final fits_data array.
fits_data = []
for i in range(len(obs_idx2)):
    for j in range(6):
        expo = df2.loc[obs_idx2[i]][j]
        for k in range(len(exp[j])):
            if (expo == exp[j][k]):
                with fits.open(f[j]) as imgbb:
                    fits_data.append(imgbb[k].data)
print(fits_data)

# Exporting to CSV File
#export_csv = df.to_csv(r"../IMAGES/exposure.csv", index=True, header=True)
