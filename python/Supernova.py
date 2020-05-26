#Supernova.py
'''
Class for a supernova. Will hold data perpetually as a class variable
'''
import pandas as pd

class Supernova():

	def __init__(self,name):
	    self.name = name
	    self.desired_filter_list = ['UVW2', 'UVM2','UVW1',  'U', 'B', 'V','R', 'I'] #potentially make a filter class so this doesnt have to be hardcoded
	    self.supernova_data_path = "../input/{}_osc.csv".format(self.name)
	    self.supernova_data = pd.read_csv(self.supernova_data_path, header=None, delimiter=',')


	def getPossibleFilters(self):
		csv_file = open(self.supernova_data_path,"r")
		removeFilterDuplicates(csv_file)

	def removeFilterDuplicates(self, csv_file):
		available_filters = [None]*len(self.desired_filter_list)
		for row in csv_file:
			current_filter = row[5]
			if current_filter in self.desired_filter_list:
				available_filters.append(current_filter)
		csv_file.close()
		self.desired_filter_list = available_filters

	def getCountRates(self, template):


	def isDataLocal(self, magnitudes):
		supernova_data = pd.read_csv(self.supernova_data_path, header=None, delimiter=',')
		
	    data = input_file.read()
	    data = data.splitlines()
	    data_list = []
	    for line in data:
	        print(line)
	        data_list.append(line.split(','))
    #print(data_list)


