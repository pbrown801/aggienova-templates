import pandas as pd
import numpy as np
import csv



def mangled_to_counts(sn_name, filter_list, mangled_counts, epochs):

    df = pd.DataFrame(data = mangled_counts,
                      index = epochs,
                      columns = filter_list)

    df.to_csv('../input/COUNTS/'+sn_name+'_mangledcounts.csv',index_label = 'Time (MJD)')
