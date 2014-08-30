from __future__ import division
import collections, math

# stemmed_a = "./t4e.corpora.stemmed/train.stemmed.answers"
# stemmed_q = "./t4e.corpora.stemmed/train.stemmed.questions"
# stemmed_both = "./t4e.corpora.stemmed/train.stemmed"
# stemmed_docs = [stemmed_q,stemmed_a]

# ikea_en = "./t4e.corpora.tokenised/1.ikea/ikea.corpus.tokenised.train.questions.txt"
# ikea_it = "./t4e.corpora.tokenised/3.it.ikea/ikea.corpus.it.tokenised.train.questions.txt"
# ig = "./t4e.corpora.tokenised/0.ig1/ig1.corpus.tokenised.train.questions.txt"
# docs = [ikea_en,ikea_it,ig]

#doc in the form [train questions, train answers, test questions, test answers ]
def frequency(doc):

	f ={}

	with open(doc[0],"r") as mefile:
		C2 = 0
		IKEA_IT = 0
		IKEA_EN = 0

		for line in mefile:
			lines = line.split('\t')
			ID = lines[1]
			words = lines[4].replace("<s>","").replace("</s>","").split(" ")

			for word in words:
				if word in f:
					if ID == "C2":
						f[word] = [sum(i) for i in zip(f[word],[1,0,0])]
						C2+=1
					elif ID == "IKEA_EN":
						f[word] = [sum(i) for i in zip(f[word],[0,1,0])]
						IKEA_EN += 1
					elif ID == "IKEA_IT":
						f[word] = [sum(i) for i in zip(f[word],[0,0,1])]
						IKEA_IT+=1
						
				else:
					"smoothing through +1"
					if ID == "C2":
						f[word] = [2,1,1]
						C2+=1
					elif ID == "IKEA_EN":
						f[word] = [1,2,1]
						IKEA_EN += 1
					elif ID == "IKEA_IT":
						f[word] = [1,1,2]
						IKEA_IT+=1

	with open(doc[1],"r") as mefile:
		C2 = 0
		IKEA_IT = 0
		IKEA_EN = 0

		for line in mefile:
			lines = line.split('\t')
			ID = lines[2]
			words = lines[5].replace("<s>","").replace("</s>","").split(" ")
			for word in words:
				if word in f:
					if ID == "C2":
						f[word] = [sum(i) for i in zip(f[word],[1,0,0])]
						C2+=1
					elif ID == "IKEA_EN":
						f[word] = [sum(i) for i in zip(f[word],[0,1,0])]
						IKEA_EN += 1
					elif ID == "IKEA_IT":
						f[word] = [sum(i) for i in zip(f[word],[0,0,1])]
						IKEA_IT+=1
				else:
					if ID == "C2":
						f[word] = [2,1,1]
						C2+=1
					elif ID == "IKEA_EN":
						f[word] = [1,2,1]
						IKEA_EN += 1
					elif ID == "IKEA_IT":
						f[word] = [1,1,2]
						IKEA_IT+=1
	f["**prob**"] = [C2,IKEA_EN,IKEA_IT]

	return f

def augmented_frequency(freq):
	af = {}
	#find max
	maximum0 = 1
	maximum1 = 1
	maximum2 = 1

	for word in freq:
		values = freq[word]
		minimax0 = values[0]
		minimax1 = values[1]
		minimax2 = values[2]
		if minimax0 > maximum0:
			maximum0 = minimax0
		if minimax1 > maximum1:
			maximum1 = minimax1
		if minimax2 > maximum2:
			maximum2 = minimax2

	for word in freq:
		values = freq[word]
		probs = freq["**prob**"]
		af[word] = [ 0.5 + ( (0.5*(values[0]-1)) / maximum0 ), 0.5 + ( (0.5*(values[1]-1)) / maximum1 ), 0.5 + ( (0.5*(values[2]-1)) / maximum2 ) ]

	return af


# given frequency distribution, using augmented frequency

def idf(freq):
	tfidf = {}

	for word in freq:
		tf = freq[word]
		
		N = 3
		df = 3 - tf.count(0.5)
				
		tfidf[word] = [ 1 + tf[0]*math.log(N/df) , 1 + tf[1]*math.log(N/df) , 1	 + tf[2]*math.log(N/df)]


	return tfidf


