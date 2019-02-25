# code to take in emily's csv file and make plot of count rate vs mjd including all filters
import numpy as np
import matplotlib.pyplot as plt
import csv

file = input('enter file name:')
with open('file') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    filters = []
    count_rate = []
    mjd = []
    for row in csv_reader:
        filter.append(float(row[0]))
        count_rate.append(float(row[1]))
        mjd.append(float(row[2]))
        line_count += 1



# pull the count rate and mjd for u filter to then graph only that filter
# unsure if i add in any a general code for error bars
u_count = []
u_mjd = []
for i in range(len(filters)):
    if filter[i] =='U':
        u_count.append(count_rate[i])
        u_mjd.append(mjd[i])

x = u_mjd
y = u_count
plot1 = plt.plot(x,y)
plt.title('Data for U band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')

# pull the count rate and mjd for uvw2 filter to then graph only that filter
uvw2_count = []
uvw2_mjd = []
for i in range(len(filters)):
    if filter[i] =='UVW2':
        uvw2_count.append(count_rate[i])
        uvw2_mjd.append(mjd[i])

x2 = uvw2_mjd
y2 = uvw2_count
plot2 = plt.plot(x2, y2)
plt.title('Data for UVW2 band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')

# putting all filters on the same plot
plot1.extend(plot2)

# pull the count rate and mjd for uvm2 filter to then graph only that filter
uvm2_count = []
uvm2_mjd = []
for i in range(len(filters)):
    if filter[i] == 'UVM2':
        uvm2_count.append(count_rate[i])
        uvm2_mjd.append(mjd[i])

x3 = uvm2_mjd
y3 = uvm2_count
plot3 = plt.plot(x3, y3)
plt.title('Data for UVM2 band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')

# adding graph to other filter graphs
plot1.extend(plot3)

# pull the count rate and mjd for uvw1 filter to then graph only that filter
uvw1_count = []
uvw1_mjd = []
for i in range(len(filters)):
    if filter[i] == 'UVW1':
        uvw1_count.append(count_rate[i])
        uvw1_mjd.append(mjd[i])

x4 = uvw1_mjd
y4 = uvw1_count
plot4 = plt.plot(x4, y4)
plt.title('Data for UVW1 band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')

# adding graph to other filter graphs
plot1.extend(plot4)

b_count = []
b_mjd = []
for i in range(len(filters)):
    if filter[i] =='B':
        b_count.append(count_rate[i])
        b_mjd.append(mjd[i])

x5 = b_mjd
y5 = b_count
plot5 = plt.plot(x5, y5)
plt.title('Data for B band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot5)

g_count = []
g_mjd = []
for i in range(len(filters)):
    if filter[i] =='G':
        g_count.append(count_rate[i])
        g_mjd.append(mjd[i])

x6 = g_mjd
y6 = g_count
plot6 = plt.plot(x6, y6)
plt.title('Data for G band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot6)

v_count = []
v_mjd = []
for i in range(len(filters)):
    if filter[i] =='V':
        v_count.append(count_rate[i])
        v_mjd.append(mjd[i])

x7 = v_mjd
y7 = v_count
plot7 = plt.plot(x7, y7)
plt.title('Data for V band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot7)

r_count = []
r_mjd = []
for i in range(len(filters)):
    if filter[i] =='R':
        r_count.append(count_rate[i])
        r_mjd.append(mjd[i])

x8 = r_mjd
y8 = r_count
plot8 = plt.plot(x8, y8)
plt.title('Data for R band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot8)

i_count = []
i_mjd = []
for i in range(len(filters)):
    if filter[i] =='I':
        i_count.append(count_rate[i])
        i_mjd.append(mjd[i])

x9 = i_mjd
y9 = i_count
plot9 = plt.plot(x9, y9)
plt.title('Data for I band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot9)

j_count = []
j_mjd = []
for i in range(len(filters)):
    if filter[i] =='J':
        j_count.append(count_rate[i])
        j_mjd.append(mjd[i])

x10 = j_mjd
y10 = j_count
plot10 = plt.plot(x10, y10)
plt.title('Data for R band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot10)

h_count = []
h_mjd = []
for i in range(len(filters)):
    if filter[i] =='H':
        h_count.append(count_rate[i])
        h_mjd.append(mjd[i])

x11 = h_mjd
y11 = h_count
plot11 = plt.plot(x11, y11)
plt.title('Data for H band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot11)

k_count = []
k_mjd = []
for i in range(len(filters)):
    if filter[i] =='K':
        k_count.append(count_rate[i])
        k_mjd.append(mjd[i])

x12 = k_mjd
y12 = k_count
plot12 = plt.plot(x12, y12)
plt.title('Data for K band')
plt.xlabel('Time (mjd)')
plt.ylabel('Count rate')
# adding graph to other filter graphs
plot1.extend(plot12)

# showing the final plot of all the filters on one graph
plot1.show()
