#!/usr/bin/env python
# coding: utf-8

# In[80]:


import os 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

filter_file_name = 'LSST_G.dat'
spectra_file_name = 'Gaia16apd_uv.dat'

filter_file = open (os.path.expanduser("~/Documents/jupyter_notebooks/nova/%s") % (filter_file_name))
spectra_file = open(os.path.expanduser('~/Documents/jupyter_notebooks/nova/%s') % (spectra_file_name))

spectra = pd.read_csv(spectra_file, header= None,engine='python')
filters = pd.read_csv(filter_file, header= None, engine='python')

wavelength_spectra = []
flux_spectra = []
wavelength_filters = []
area_filters = []

for i in range(0, len(spectra)):
    hold = spectra[0][i]
    split_text = hold.split(' ')
    wavelength_spectra.append(eval(split_text[0]))
    flux_spectra.append(eval(split_text[1]))

for i in range(0, len(filters)):
    hold = filters[0][i]
    split_text = hold.split('  ')
    wavelength_filters.append(eval(split_text[0]))
    area_filters.append(eval(split_text[1]))


# In[90]:


plt.plot(wavelength_spectra, flux_spectra)
plt.xlabel('wavelength spectra')
plt.ylabel('flux spectra')


# In[91]:


plt.plot(wavelength_filters, area_filters)
plt.xlabel('wavelength_filters')
plt.ylabel('area_filters')


# In[108]:


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


# In[109]:


plt.plot(wavelength_filters, ergs)
plt.xlabel('wavelength_filters')
plt.ylabel('ergs/s/angstrom')


# In[110]:


ten_percent_x = ten_percent_x_vals[-1]
ten_percent_y = ten_percent_y_vals[-1]
print(ten_percent_x, ten_percent_y)


# In[111]:


fifty_percent_x = fifty_percent_x_vals[-1]
fifty_percent_y = fifty_percent_y_vals[-1]
print(fifty_percent_x, fifty_percent_y)


# In[113]:


ninety_percent_x = ninety_percent_x_vals[-1]
ninety_percent_y = ninety_percent_y_vals[-1]
print(ninety_percent_x, ninety_percent_y)

