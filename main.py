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
			if not filename.endswith('.csv'):
				continue
			df = read_csv(filename, header=None)
			# drop row number
			values = df.values[:, 1:]
			self.subjects.append(values)
		return self.subjects

	def load_from_dat(self):
		return self.subjects

	# plot the x, y, z acceleration and activities for a single subject
	def plot_subject(self, subject):
		print(subject)
		pyplot.figure()
		# create a plot for each column
		for col in range(subject.shape[1]):
			pyplot.subplot(subject.shape[1], 1, col+1)
			pyplot.plot(subject[:, col])
		pyplot.show()


p = Plot(Plot.CSV)
p.load_dataset()
p.plot_subject(p.subjects[0])

