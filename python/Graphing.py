import matplotlib.pyplot as plt
import scipy.interpolate as interp
import pandas as pd
import csv


orig_data = []
mag_data = []
mag_err = []
xval = []
yval = []
time = []
time2 = []
new_time = []
f = []
avg = []
x = []
colors = ['w', 'y', 'm', 'c', 'r', 'g', 'b', 'xkcd:aqua',
          'xkcd:coral', 'xkcd:fuchsia', 'xkcd:grey']
lbl = []
# Plot formatting
plt.style.use('dark_background')
f0 = plt.figure(num=0, figsize=(8, 8))
ax01 = f0.add_subplot(211)
f0.subplots_adjust(hspace=1.5)
f0.patch.set_facecolor('xkcd:black')
ax01.set_title('SN2007af')
plt.tight_layout()
ax01.set_ylabel("Counts Array of Different Wavelengths")
ax01.set_xlabel("Time (MJD)")

# file name to be opened. Can be changed by changing the string below.
file_name = "SN2007af_countsarray.csv"

#filters and errors
file = open(file_name, 'r', newline='').readlines()
reader = csv.reader(file, delimiter=',')
filters_from_csv = next(reader)[1::2]
reader = csv.reader(file, delimiter=',')
errors_from_csv = next(reader)[2::2]

# Data frame of the data using pandas
for filters in filters_from_csv:
    data = pd.read_csv(file_name, sep=",")
    data = data.dropna(axis=0, how='all')
    data = data.set_index('Time (MJD)')
    time_temp = list(data.index.values)  # Times
    time_1 = time_temp[0]  # first time in whole set
    time_2 = time_temp[len(time_temp)-1]  # last time in whole set
    data = data[filters]  # Gets the data for only the filters
    data = data.dropna()  # Drops unncessary values like empty
    mag_data.append(list(data))  # list of the data values
    orig_data.append(list(data))
    time.append(list(data.index.values))  # list of times for the datavalues

# Data frame of the error data using pandas
for errors in errors_from_csv:
    data2 = pd.read_csv(file_name, sep=",")
    data2 = data2.dropna(axis=0, how='all')
    data2 = data2.set_index('Time (MJD)')
    time_temp2 = list(data2.index.values)  # Times
    data2 = data2[errors]  # Gets the data for only the filters
    data2 = data2.dropna()  # Drops unncessary values like empty
    mag_err.append(list(data2))  # list of the data values
    time2.append(list(data2.index.values))  # list of times for the datavalues

# avg computation of data points given
for i in range(len(mag_data)):
    tot = 0
    for j in range(len(mag_data[i])):
        tot += mag_data[i][j]
    if (len(mag_data[i]) == 0):
        continue
    else:
        avg.append(tot/len(mag_data[i]))

# Adding the avg of the data points given to the beginning and end of the array.
# Also adding corresponding first time or last time point.
j = 0
for i in range(len(filters_from_csv)-1):
    if len(mag_data[i]) == 0:
        continue
    if ((time[i][0] == time_1) & (time[i][len(time[i])-1] != time_2)):
        time[i] = time[i] + [time_2]
        mag_data[i] = mag_data[i]+[round(avg[j], 3)]
        j += 1
    elif ((time[i][len(time[i])-1] == time_2) & (time[i][0] != time_1)):
        time[i] = [time_1] + time[i]
        mag_data[i] = [round(avg[j], 3)]+mag_data[i]
        j += 1
    elif ((time[i][len(time[i])-1] != time_2) & (time[i][0] != time_1)):
        time[i] = [time_1] + time[i] + [time_2]
        mag_data[i] = [round(avg[j], 3)]+mag_data[i]+[round(avg[j], 3)]
        j += 1
    else:
        continue

# interpolation
# linear if there are constant data values
# else cubic
j = 0
for i in range(len(mag_data)):
    k = 0
    count = 0
    if len(mag_data[i]) == 0:
        continue
    else:
        if mag_data[i][0] == avg[j]:
            for k in range(len(mag_data[i])):
                if mag_data[i][k] == avg[j]:
                    count += 1
            if len(mag_data[i]) == count:
                f.append(interp.interp1d(time[i], mag_data[i], kind='linear'))
                j += 1
                new_time.append(time[i])
                lbl.append(filters_from_csv[i])
        else:
            f.append(interp.interp1d(time[i], mag_data[i], kind='cubic'))
            j += 1
            new_time.append(time[i])
            lbl.append(filters_from_csv[i])

# ERROR processing
# intitalizing the x array for error
for i in range(len(mag_data)):
    if len(mag_data[i]) == 0:
        continue
    x.append(time[i][0])

# The first range is the length of the graph
# Using each interpolation function f produced earlier we input x values to get y values.

for c in range(1000):
    tp = []
    x_temp = []
    inte = []
    for i in range(len(f)):
        temp = f[i]
        tp.append(temp(x[i]))
        x_temp.append(x[i])
        inte.append(((new_time[i][len(new_time[i])-1])-new_time[i][0])/1000)
        x[i] += inte[i]
    xval.append(x_temp)
    yval.append(tp)

yval_fin = []
xval_fin = []
for c in range(len(f)):
    yval1 = []
    xval1 = []
    for i in range(999):
        yval1.append(yval[i][c])
        xval1.append(xval[i][c])
    xval_fin.append(xval1)
    yval_fin.append(yval1)

# We plot the x and y values.
for i in range(len(f)):
    ax01.plot(xval_fin[i], yval_fin[i], colors[i], label=lbl[i])

# We plot the errorbars at the original data points given.
for i in range(len(mag_data)):
    if len(mag_data[i]) == 0:
        continue
    ax01.errorbar(time2[i], orig_data[i], mag_err[i], fmt='o')

ax01.legend()
# Uncomment to save the figure
# plt.savefig('test1.png')
plt.show()
