from os import listdir
from pandas import read_csv
from matplotlib import pyplot


class Plot:
	CSV = 'csv'
	DAT = 'dat'

	def __init__(self, data_source=CSV):
		self.data_source = data_source
		self.subjects = list()

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
				values = df.values[:, 1:]  # drop row number
				self.subjects.append(values)
		return self.subjects

	def load_from_dat(self):
		return self.subjects  # Not implemented yet but returning original subjects only.

	# plot the x, y, z acceleration for each subject
	def plot_subjects(self):
		subjects = self.subjects
		print(subjects)
		pyplot.figure()
		# create a plot for each subject
		for i in range(len(subjects)):
			pyplot.subplot(len(subjects), 1, i + 1)
			# plot each of x, y and z
			for j in range(subjects[i].shape[1] - 1):
				pyplot.plot(subjects[i][:, j])
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


p = Plot(Plot.CSV)
p.load_dataset()
activities = [i for i in range(0, 8)]
grouped = p.group_by_activity(activities)
p.plot_durations(grouped, activities)
p.plot_subjects()

