# Archive of supernova images at https://archive.stsci.edu/missions/hlsp/sousa/

import os
import pandas as pd
from astropy.io import fits
import requests
import shutil

exist = False
exist2 = False
filterlst = ["bb", "m2", "uu", "vv", "w1", "w2"]


def check_dir(nova_name):
    global exist, exist2
    exist = False
    exist2 = False
    # list of files in current directory
    cur = os.getcwd()
    filelist = os.listdir(cur)
    for x in filelist:
        # if x.endswith('.fits') or x.endswith('.gz'):
        # Checking if the downloaded files of the supernova exist in the current directory
        if '.fits' in x and nova_name in x:
            exist = True
        # Checking for any final data manipulation output files in the currect diectory
        if x.endswith('.fits') and nova_name in x:
            exist2 = True


def download_file(nova_name):
    if (not (exist)):
        print("Downloading " + nova_name + " image files")
        for i in range(6):
            fits_file = "hlsp_sousa_swift_uvot_"+nova_name + \
                "_"+filterlst[i]+"_v1.0_img.fits.gz"
            URL = "https://archive.stsci.edu//missions/hlsp/sousa/"+nova_name+"/"+fits_file
            response = requests.get(URL, allow_redirects=True)
            open(fits_file, 'wb').write(response.content)
    else:
        print("Files already exist")


def manipulate(nova_name, exp_limit):
    f = []
    name = []
    date_obs = [[], [], [], [], [], []]
    exp = [[], [], [], [], [], []]
    dict1 = {}
    dict2 = {}
    obs_idx = []

    if (not (exist2)):
        print("Data Manipulation Starts")
        cur = os.getcwd()
        filelist = os.listdir(cur)
        for x in filelist:
            if x.endswith('.gz') and nova_name in x:
                f.append(x)  # Gets the list of fits files
        # print(f)  # For refrence of the order of the files.

        for i in range(6):
            for j in range(6):
                if filterlst[j] in f[i]:
                    # Gets the names of the supernova with the filter for later use
                    name.append(nova_name+"_" + filterlst[j])

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
                        # Checks to see if the loop skips only the primary header in the fits files which is at index 0.
                        if count != 0:
                            print("DATA FROM FITS IMAGE COULD PRODUCE ERRONEUS DATA")
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

        # print(df)
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
                if (val[c] > exp_limit):
                    count += 1
            if count == 6:
                if i+while_counter < (len(df['diff_time'])-1):
                    t = start + (0.5*(start-df.index[i+while_counter]))
                    dict2[str(t.round('min'))] = val

        # Creating the dataframe using dict2 that makes the date obs the index.
        
        df2 = pd.DataFrame.from_dict(dict2, orient='index', columns=[
            'exp1', 'exp2', 'exp3', 'exp4', 'exp5', 'exp6']).sort_index(axis=0)

        df2['Time'] = df2.index
        df2.to_csv(nova_name+'_'+str(exp_limit)+'.csv', index=False)
        # Gets index from the data frame 2 and appends to an array.
        # Creates a list of fits.HDULists depending on the number of rows in df2. This is needed for the multi extension
        # fits image files.
        obs_idx2 = []
        hd = []
        cr = []
        temp_hd = []
        temp_cr = []
        for i in range(len(df2['exp1'])):
            obs_idx2.append(df2.index[i])
        for i in range(6):
            temp_hd.append('new_hdul'+str(i))
            temp_cr.append('new_crhdul'+str(i))
            hd.append('new_hdul'+str(i))
            cr.append('new_crhdul'+str(i))
            temp_hd[i] = fits.HDUList()
            temp_cr[i] = fits.HDUList()
            hd[i] = fits.HDUList()
            cr[i] = fits.HDUList()

        # Searches the original fits images files for the correct data for each observation date and each of the 6 exposures.
        # The data is appended to a final fits_data array. Added the HDUList for the multi extension fits files.
        fits_data = []
        temphd_sort = [[], [], [], [], [], []]
        tempcr_sort = [[], [], [], [], [], []]
        count = 0
        for i in range(6):
            for j in range(len(obs_idx2)):
                expo = df2.loc[obs_idx2[j]][i]
                for k in range(len(exp[i])):
                    if(expo == exp[i][k]):
                        with fits.open(f[i]) as imgbb:
                            fits_data.append(imgbb[k+1].data)
                            # count_rate_img.append(imgbb[k+1].data/exp[i][k])
                            temp_hd[i].append(imgbb[k+1])
                            cr_data = imgbb[k+1].data/exp[i][k]
                            imgbb[k+1].data = cr_data
                            temp_cr[i].append(imgbb[k+1])
                        break
        # Sorting the temphd and tempcr lists by date observed
        for s in range(len(temp_hd)):
            for l in range(len(temp_hd[s])):
                temphd_sort[s].append(temp_hd[s][l].header['DATE-OBS'])
                tempcr_sort[s].append(temp_cr[s][l].header['DATE-OBS'])
            temphd_sort[s].sort()
            tempcr_sort[s].sort()
        for i in range(len(temphd_sort)):
            for j in range(len(temphd_sort[i])):
                for k in range(len(temp_hd[i])):
                    if temphd_sort[i][j] == temp_hd[i][k].header['DATE-OBS']:
                        hd[i].append(temp_hd[i][k])
                    if tempcr_sort[i][j] == temp_cr[i][k].header['DATE-OBS']:
                        cr[i].append(temp_cr[i][k])
                        break

        # Final sorted output multi extension files
        for i in range(6):
            # Used the names list to appropriately write fits multi extension files
            try:
                hd[i].writeto(name[i] + '.fits')

                cr[i].writeto(name[i] + '_cr.fits')
            except:
                pass
        print("Data Manipulation Ends")


def del_download(nova_name):
    if (exist):
        cur = os.getcwd()
        filelist = os.listdir(cur)
        for i in range(6):
            fits_file = "hlsp_sousa_swift_uvot_"+nova_name + \
                "_"+filterlst[i]+"_v1.0_img.fits.gz"
            if fits_file in filelist:
                os.remove(fits_file)
    else:
        print("Nothing to remove.")


def move(nova_name):
    # Cleaning up directory by moving data manipulation files into count_rate and fits sub-directories if files exist.
    if (exist2):
        print("Moving into folders")
        cur = os.getcwd()
        filelist = os.listdir(cur)
        folder1 = cur + "\\" + 'count_rate'
        folder2 = cur + "\\"+'fits'
        folder1_list = os.listdir(folder1)
        folder2_list = os.listdir(folder2)
        for x in filelist:
            if x.endswith("_cr.fits") and nova_name in x:
                if x not in folder1_list:
                    shutil.move(x, folder1)
                else:
                    print("File already in count_rate folder. Removing from directory")
                    os.remove(x)
        filelist = os.listdir(cur)
        for x in filelist:
            if x.endswith(".fits") and nova_name in x:
                if x not in folder2_list:
                    shutil.move(x, folder2)
                else:
                    print("File already in fits folder. Removing from directory")
                    os.remove(x)
    else:
        print("Nothing to move.")


def main(n_name, exp_limit):
    global exist, exist2
    check_dir(n_name)
    download_file(n_name)
    manipulate(n_name, exp_limit)
    check_dir(n_name)
    del_download(n_name)
    move(n_name)


if __name__ == "__main__":
    main('sn2005cs', 0)
    main('sn2006x', 0)
    main('asassn-13co', 0)
