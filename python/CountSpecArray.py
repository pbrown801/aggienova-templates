import numpy as np
import matplotlib.pyplot as plt


spectra_file_input = input("What spectra file do you want to use?: ")
filter_file_input = input("What filter file do you want to use?: ")

spectra_file_name = ('../spectra/%s' % (spectra_file_input))
filter_file_name = ('../filters/%s' % (filter_file_input))


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

# Start pulling data from a second spectrum
spectra_file_input_2 = input("What is the second filter file that you want to use?: ")
spectra_file_name = ('../spectra/%s' % (spectra_file_input_2))
spectra_file_load_2 = np.loadtxt(spectra_file_name_2)

wavelength_spectra_2 = []
flux_spectra_2 = []

for i in range(0, len(spectra_file_load_2)):
    wavelength_spectra_2.append(spectra_file_load_2[i][0])
for i in range(0,len(spectra_file_load_2)):
    flux_spectra_2.append(spectra_file_load_2[i][1])
    
interpolated_data_2 = np.interp(wavelength_filters, wavelength_spectra_2, flux_spectra_2)
ergs_2 = np.array(interpolated_data_2) * np.array(area_filters)

fig = plt.figure() 
ax=fig.add_subplot(111, label=1)
ax2=fig.add_subplot(111, label=2, frame_on=False)

ax.plot(wavelength_filters, ergs, color = 'C0', label=spectra_file_input)
ax.set_xlabel('wavelength_filter', color = 'C0')
ax.set_ylabel('ergs_1', color = 'C0')
ax.tick_params(axis='x', colors="C0")
ax.tick_params(axis='y', colors="C0")

ax2.plot(wavelength_filters, ergs_2, color = 'C3', label=spectra_file_input_2)
ax2.set_xlabel('wavelength_filter', color = 'C3')
ax2.set_ylabel('ergs_2', color = 'C3')
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='x', colors="C3")
ax2.tick_params(axis='y', colors="C3")

plt.show()
