import nltk
import random

IKEA_EN = "./1.ikea/ikea.corpus.stemmed.train.questions.txt"
IKEA_IT = "./3.it.ikea/ikea.corpus.it.stemmed.train.questions.txt"
IG = "./0.ig1/ig1.corpus.stemmed.train.questions.txt"
trains = [IKEA_EN, IKEA_EN, IG]
trainlabel = ["IKEA_EN", "IKEA_EN", "IG"]

ikea_en = "./1.ikea/ikea.corpus.stemmed.validation.questions.txt"
ikea_it = "./3.it.ikea/ikea.corpus.it.stemmed.validation.questions.txt"
ig = "./0.ig1/ig1.corpus.stemmed.validation.questions.txt"
vals = [ikea_en,ikea_it,ig]

FEATURES = "features.stemmed"

def document_features(document):
	with open(FEATURES,"r") as myfile:
		feats = myfile.readlines()

	document_words = set(feats)
	features = {}
	for word in feats:
		features['contains(%s)' % word] = (word in document_words)
	return features



def train():
	l= 0

	for train in trains:
	  	with open(train,"r") as mefile:
			traindocs = [(line.split()[4:-1], trainlabel[l])
				for line in mefile]
			l += 1
	random.shuffle(traindocs)
	trainfeats = [(document_features(d), c) for (d,c) in traindocs]

	print trainfeats [1]
	
	l= 0	
	for val in vals:
		with open(val,"r") as mafile:
			valdocs = [(line.split()[4:-1], trainlabel[l])
				for line in mafile]
			l +=1
	random.shuffle(valdocs)
	valfeats = [(document_features(d), c) for (d,c) in valdocs]

	classifier = nltk.NaiveBayesClassifier.train(trainfeats)
	print(nltk.classify.accuracy(classifier, valfeats))
	classifier.show_most_informative_features(100)

	print(classifier.classify(document_features(traindocs[1])))