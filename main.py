from os import listdir
from pandas import read_csv
from matplotlib import pyplot
import numpy as np
from numpy import nan
from sklearn.impute import SimpleImputer


class Plot:
	CSV = 'csv'
	DAT = 'dat'

	def __init__(self, data_source=CSV):
		self.data_source = data_source
		self.subjects = list()
		self.coordinates = list()

	def load_dataset(self):
		if self.data_source == Plot.CSV:
			self.subjects = self.load_from_csv()
		elif self.data_source == Plot.DAT:
			self.subjects = self.load_from_dat()
		return self.subjects

	def load_from_csv(self):
		directory = 'HAR/'
		for name in listdir(directory):
			filename = directory + '/' + name
			if filename.endswith('.csv'):
				df = read_csv(filename, header=None)
				df[[1, 2, 3, 4]] = df[[1, 2, 3, 4]].replace(0, nan)
				values = df.values[:, 1:]  # drop row number
				imputer = SimpleImputer(missing_values=nan, strategy='mean')
				transformed_values = imputer.fit_transform(values)
				self.subjects.append(transformed_values)
		return self.subjects

	def load_from_dat(self):
		directory = 'HAR_DAT/'
		for name in listdir(directory):
			filename = directory + '/' + name
			self.coordinates = list()
			print("Processing ", filename, "file...")
			if filename.endswith('.dat'):
				dat_file = open(filename, "r")
				lines = dat_file.read()
				rows = lines.splitlines()
				for row in rows:
					columns = row.split(' ')
					hl_activity = columns[244]  # print(columns[244]) # contains HL_Activity/class_activity
					columns = columns[1:37]
					values = np.array(columns).reshape(12, 3)
					values = np.hstack((values, np.full((12, 1), hl_activity)))
					imputer = SimpleImputer(missing_values=nan, strategy='mean')
					transformed_values = imputer.fit_transform(values)
					for transformed_value in transformed_values:
						self.coordinates.append(transformed_value)
				self.subjects.append(np.array(self.coordinates))
		print("Processing finished!")
		return self.subjects

	def plot_subjects(self):
		subjects = self.subjects[0:5]
		pyplot.figure()
		count = 0
		for i in range(len(subjects)):
			pyplot.subplot(len(subjects), 1, i + 1)
			for j in range(subjects[i].shape[1] - 1):
				pyplot.plot(subjects[i][:, j])
				count += 1
				print("plotted ", i, len(self.subjects))
		pyplot.show()

	# returns a list of dict, where each dict has one sequence per activity
	def group_by_activity(self, activities):
		grouped = [{a: s[s[:, -1] == a] for a in activities} for s in self.subjects]
		return grouped

	# calculate total duration in sec for each activity per subject and plot
	def plot_durations(self, grouped, activities):
		# calculate the lengths for each activity for each subject
		freq = 52
		durations = [[len(s[a]) / freq for s in grouped] for a in activities]
		pyplot.boxplot(durations, labels=activities)
		pyplot.show()


p = Plot(Plot.DAT)
p.load_dataset()
#print(len(p.subjects))
#print(p.subjects)
#print(p.subjects[0][11])
#activities = [i for i in range(0, 8)]
#grouped = p.group_by_activity(activities)
#print("Plotting has started...")
p.plot_subjects()
#print(p.subjects)
#p.plot_durations(grouped, activities)
#print("Plotting has done!")
