#This is the testing script to ensure the accuracy of the process

import csv
#Reading the test files
with open('../output/Test_A.csv', 'r') as file_A, open('../input/Test_Demo.csv', 'r') as file_B:
    Line_1 = file_A.readlines()
    Line_2 = file_B.readlines()

check=True
#Comparing each line of the csv files
for line in Line_2:
    if line not in Line_1:
        #Comma line ending issue fix
        if (line==",,"):
            continue
        #Isolating the issue
        else:
            print(check)
            print("The error has been isolated to the following dataset")
            print(line)

#Issues true if the line is the same
if check:
    print("No issues found.")

