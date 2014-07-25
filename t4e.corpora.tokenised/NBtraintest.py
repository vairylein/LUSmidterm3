import nltk
import random

IKEA_EN = "./1.ikea/ikea.corpus.tokenised.train.questions.txt"
IKEA_IT = "./3.it.ikea/ikea.corpus.it.tokenised.train.questions.txt"
IG = "./0.ig1/ig1.corpus.tokenised.train.questions.txt"
trains = [IKEA_EN, IKEA_EN, IG]
trainlabel = ["IKEA_EN", "IKEA_IT", "IG1"]

ikea_en = "./1.ikea/ikea.corpus.tokenised.validation.questions.txt"
ikea_it = "./3.it.ikea/ikea.corpus.it.tokenised.validation.questions.txt"
ig = "./0.ig1/ig1.corpus.tokenised.validation.questions.txt"
vals = [ikea_en, ikea_it, ig]

FEATURES = "features.tokenised"

def document_features(document):
	feats = []
	with open(FEATURES,"r") as myfile:
		for line in myfile:
			feats += [line[:-1]]
	
	document_words = set(feats)
	features = {}
	for word in feats:
		features['contains(%s)' % word] = (word in document_words)
	return features



def train():
	l= 0


	#get the features of the validation set
	traindocs=[]
	for train in trains:
	  	with open(train,"r") as mefile:
			text = mefile.readlines()
			f=0
			for line in mefile:
				traindocs += [(line.split()[3:-1],trainlabel[l])]
				f+=1
				
			l += 1
	random.shuffle(traindocs)
	trainfeats = [(document_features(d), c) for (d,c) in traindocs]

	#get features of the training set
	valdocs=[]
	i= 0	
	for val in vals:
		with open(val,"r") as mafile:
			for bla in mafile:
				valdocs += [(bla.split()[4:-1], trainlabel[i])]
			i +=1
	print valdocs
	random.shuffle(valdocs)
	
	valfeats = [(document_features(d), c) for (d,c) in valdocs]


	classifier = nltk.NaiveBayesClassifier.train(trainfeats)
	print(sorted(classifier.labels()))
	print(classifier.classify_many(valfeats))
	print(nltk.classify.accuracy(classifier, valfeats))
	classifier.show_most_informative_features(10)

	print(classifier.classify(document_features(traindocs[23])))