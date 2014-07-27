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

		for fv in featureVs:
			counts[fv[1]] += 1
			for counter in 
				featurecount
