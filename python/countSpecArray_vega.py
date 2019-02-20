#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os 
import pandas as pd 
import csv
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


# Reading in data from spectra file 

spectra_file_name = '/users/zuhayrali/Documents/jupyter_notebooks/nova/vega.csv'
wavelength_spectra_hold = []
flux_spectra_hold = []
wavelength_spectra = []
flux_spectra = []

with open(spectra_file_name) as file:
    reader = csv.reader(file)
    for row in reader:
        wavelength_spectra_hold.append((row[0]))
        flux_spectra_hold.append((row[1]))
file.close()

wavelength_spectra_hold.pop(0)
flux_spectra_hold.pop(0)

for i in wavelength_spectra_hold: 
    wavelength_spectra.append(eval(i))
for i in flux_spectra_hold:
    flux_spectra.append(eval(i))


# In[4]:


# Reading in data from filter file 
filter_file_name = 'LSST_G.dat'
filter_file = open (os.path.expanduser("~/Documents/jupyter_notebooks/nova/%s") % (filter_file_name))
filters = pd.read_csv(filter_file, header= None, engine='python')

wavelength_filters = []
area_filters = []

for i in range(0, len(filters)):
    hold = filters[0][i]
    split_text = hold.split('  ')
    wavelength_filters.append(eval(split_text[0]))
    area_filters.append(eval(split_text[1]))


# In[5]:


integral = np.trapz(flux_spectra, wavelength_spectra)

ten_percent = (integral) * 0.1
fifty_percent = (integral) * 0.5
ninety_percent = (integral) * 0.9

test_array_y = []
test_array_x = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):
    if integral_test < ten_percent:
        test_array_y.append(flux_spectra[i])
        test_array_x.append(wavelength_spectra[i])
        integral_test = np.trapz(test_array_y, test_array_x)
    else:
        ten_percent_value = test_array_y[-1]

test_array_y_50 = []
test_array_x_50 = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):
    if integral_test < fifty_percent:
        test_array_y_50.append(flux_spectra[i])
        test_array_x_50.append(wavelength_spectra[i])
        integral_test = np.trapz(test_array_y_50, test_array_x_50)
    else:
        fifty_percent_value = test_array_y_50[-1]
        
test_array_y_90 = []
test_array_x_90 = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):
    if integral_test < ninety_percent:
        test_array_y_90.append(flux_spectra[i])
        test_array_x_90.append(wavelength_spectra[i])
        integral_test = np.trapz(test_array_y_90, test_array_x_90)
    else:
        ninety_percent_value = test_array_y_90[-1]
        
plt.subplot(611)
plt.xlim(0,10000)
plt.plot(wavelength_spectra, flux_spectra)
plt.xlabel('wavelength spectra')
plt.ylabel('flux spectra')


# In[9]:


interpolated_data = np.interp(wavelength_filters, wavelength_spectra, flux_spectra)
ergs = np.array(interpolated_data) * np.array(area_filters)

integral = np.trapz(ergs, wavelength_filters)

ten_percent = (integral) * 0.1
fifty_percent = (integral) * 0.5
ninety_percent = (integral) * 0.9

ten_percent_y_vals = []
ten_percent_x_vals = []
integral_test = 0

for i in range(0, len(interpolated_data)):
    if integral_test < ten_percent:
        ten_percent_y_vals.append(ergs[i])
        ten_percent_x_vals.append(wavelength_filters[i])
        integral_test = np.trapz(ten_percent_y_vals, ten_percent_x_vals)
    else:
        break

fifty_percent_y_vals = []
fifty_percent_x_vals = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):
    if integral_test < fifty_percent:
        fifty_percent_y_vals.append(ergs[i])
        fifty_percent_x_vals.append(wavelength_filters[i])
        integral_test = np.trapz(fifty_percent_y_vals, fifty_percent_x_vals)
    else:
        break
        
ninety_percent_y_vals = []
ninety_percent_x_vals = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):
    if integral_test < ninety_percent:
        ninety_percent_y_vals.append(ergs[i])
        ninety_percent_x_vals.append(wavelength_filters[i])
        integral_test = np.trapz(ninety_percent_y_vals, ninety_percent_x_vals)
    else:
        break


# In[18]:


plt.plot(wavelength_filters, ergs)
plt.xlabel('wavelength_filters')
plt.ylabel('ergs/s/angstrom')


# In[19]:


ten_percent_x = ten_percent_x_vals[-1]
ten_percent_y = ten_percent_y_vals[-1]
print(ten_percent_x, ten_percent_y)


# In[20]:


fifty_percent_x = fifty_percent_x_vals[-1]
fifty_percent_y = fifty_percent_y_vals[-1]
print(fifty_percent_x, fifty_percent_y)


# In[21]:


ninety_percent_x = ninety_percent_x_vals[-1]
ninety_percent_y = ninety_percent_y_vals[-1]
print(ninety_percent_x, ninety_percent_y)


# In[ ]:





# In[ ]:





# In[ ]:




