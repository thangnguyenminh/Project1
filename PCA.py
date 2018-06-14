# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:58:58 2018

@author: Admin
"""

"""Apply PCA to a CSV file and plot its datapoints (one per line).

The first column should be a category (determines the color of each datapoint),
the second a label (shown alongside each datapoint)."""
import sys
import pandas
import pylab as pl
from sklearn import preprocessing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def main():
	"""Load data."""
	try:
		csvfile = 'demo.csv'
	except IndexError:
		print ('%s\n\nUsage: %s [--3d] <csv_file>' % (__doc__, sys.argv[0]))
		return
	data = pandas.read_csv(csvfile, index_col=(0, 1))

	# first column provides labels
	ylabels = [a for a, _ in data.index]
	labels = [text for _, text in data.index]
	encoder = preprocessing.LabelEncoder().fit(ylabels)

	xdata = data.as_matrix(data.columns)
	ydata = encoder.transform(ylabels)
	target_names = encoder.classes_
	plotpca(xdata, ydata, target_names, labels, csvfile)


def plotpca(xdata, ydata, target_names, items, filename):
	"""Make plot."""
	pca = PCA(n_components=2)
	components = pca.fit(xdata).transform(xdata)

	# Percentage of variance explained for each components
	print('explained variance ratio (first two components):',
			pca.explained_variance_ratio_)

	pl.figure()  # Make a plotting figure
	pl.subplots_adjust(bottom=0.1)

	# NB: a maximum of 7 targets will be plotted

	for i, (c, m, target_name) in enumerate(zip(
			'rbmkycg', 'o^s*v+x', target_names)):
		pl.scatter(components[ydata == i, 0], components[ydata == i, 1],
				color=c, marker=m, label=target_name)
		for n, x, y in zip(
				(ydata == i).nonzero()[0],
				components[ydata == i, 0],
				components[ydata == i, 1]):
			pl.annotate(
					items[n],
					xy=(x, y),
					xytext=(5, 5),
					textcoords='offset points',
					color=c,
					fontsize='small',
					ha='left',
					va='top')
	pl.legend()
	pl.title(
        "Scatter plot of the RGB data examples projected on the " 
        "2 first principal components") 
	pl.xlabel("Principal axis 1 - Explains %.2f %% of the variance" % (pca.explained_variance_ratio_[0] * 100.0))
	pl.ylabel("Principal axis 2 - Explains %.2f %% of the variance" % (pca.explained_variance_ratio_[1] * 100.0))
	plt.tight_layout()
	pl.show()

	plt.savefig("pca.png", format='png', dpi = 199)
	plt.savefig("pca.pdf", format='pdf',dpi = 199)
if __name__ == '__main__':
	main()
