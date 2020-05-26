#TemplateSpectrum.py
'''
Class for a template spectrum. Will hold data perpetually as class variables
'''

class TemplateSpectrum():

	def __init__(self,name):
	    self.name = name

	def getPossibleFilters(self):
		csv_path = "../input/{}_osc.csv".format(self.name)
		csv_file = open(csv_path,"r")
		removeFilterDuplicates(csv_file)

	def removeFilterDuplicates(self, csv_file):
		available_filters = [None]*len(self.desired_filter_list)
		for row in csv_file:
			current_filter = row[5]
			if current_filter in self.desired_filter_list:
				available_filters.append(current_filter)
		csv_file.close()
		self.desired_filter_list = available_filters

	def function():
		pass


