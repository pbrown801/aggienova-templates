# imports
import pandas as pd

def sel_template(epoch, series_path):
    '''
    Round epoch to the nearest value in the input series file that correspond to template files
    '''
    with open(series_path) as f:
        lines=f.readlines()
    # make a dictionary out of the epooch and file
    file_data = dict([line.strip().split(" ") for line in lines])
    # use the smallest difference between the input epoch and the keys in the dict as the file to use
    return file_data[min(file_data, key=lambda x: abs(float(x)-epoch))]

if __name__ == "__main__":
    template_file=sel_template(5.1, '../spectra/SNII_series.txt')
    print(template_file)