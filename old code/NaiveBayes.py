from __future__ import division
import collections
import math

class NBClassifier:

	def __init__(self,doc):
		self.train_data = doc
		self.features = {}
		self.labels = []
		self.fcounts = collections.defaultdict(lambda: 1)
		self.featureVs = []
		self.lcounts = collections.defaultdict(lambda:0)

	def TrainClassifier():

		for fv in self.featureVs:
			self.counts[fv[1]] += 1
			for counter in range(0,len(fv[0]): 
				self.fcounts[(fv[1])], self.labels[counter, fv[counter])] +=1

		for label in self.lcounts:
			for feature in self.label[:len(self.label)-]:
				self.lcounts[label] += len(self.features[feature])
