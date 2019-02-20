import numpy as np
import matplotlib.pyplot as plt


spectra_file_input = input("What spectra file do you want to use?: ")
filter_file_input = input("What filter file do you want to use?: ")


spectra_file_name = ('/users/zuhayrali/aggienova-templates/spectra/%s' % (spectra_file_input))
filter_file_name = ('/users/zuhayrali/aggienova-templates/filters/%s' % (filter_file_input))




spectra_file_load = np.loadtxt(spectra_file_name)

filter_file_load = np.loadtxt(filter_file_name)


wavelength_spectra = []
flux_spectra = []
wavelength_filters = []
area_filters = []    


for i in range(0, len(spectra_file_load)):
    wavelength_spectra.append(spectra_file_load[i][0])
for i in range(0,len(spectra_file_load)):
    flux_spectra.append(spectra_file_load[i][1])


for i in range(0, len(filter_file_load)):
    wavelength_filters.append(filter_file_load[i][0])
for i in range(0, len(filter_file_load)):
    area_filters.append(filter_file_load[i][1])


fig, axes = plt.subplots()
plt.plot(wavelength_spectra, flux_spectra)
plt.xlim(0,20000)
plt.xlabel('wavelength spectra')
plt.ylabel('flux spectra')


fig, axes = plt.subplots()
plt.plot(wavelength_filters, area_filters)
plt.xlabel('wavelength_filters')
plt.ylabel('area_filters')


interpolated_data = np.interp(wavelength_filters, wavelength_spectra, flux_spectra)
ergs = np.array(interpolated_data) * np.array(area_filters)

integral = np.trapz(ergs, wavelength_filters)

ten_percent = (integral) * 0.1
fifty_percent = (integral) * 0.5
ninety_percent = (integral) * 0.9

ten_percent_y_vals = []
ten_percent_x_vals = []
integral_test = 0

for i in range(0, len(wavelength_spectra)):
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


fig, axes = plt.subplots() 
plt.plot(wavelength_filters, ergs)
plt.xlabel('wavelength_filters')
plt.ylabel('ergs/s/angstrom')


ten_percent_x = ten_percent_x_vals[-1]
ten_percent_y = ten_percent_y_vals[-1]
print(ten_percent_x, ten_percent_y)


fifty_percent_x = fifty_percent_x_vals[-1]
fifty_percent_y = fifty_percent_y_vals[-1]
print(fifty_percent_x, fifty_percent_y)


ninety_percent_x = ninety_percent_x_vals[-1]
ninety_percent_y = ninety_percent_y_vals[-1]
print(ninety_percent_x, ninety_percent_y)