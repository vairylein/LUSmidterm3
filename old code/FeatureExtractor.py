from __future__ import division
from collections import Counter
import math



ikea_en = "./t4e.corpora.tokenised/1.ikea/ikea.corpus.tokenised.train.questions.txt"
ikea_it = "./t4e.corpora.tokenised/3.it.ikea/ikea.corpus.it.tokenised.train.questions.txt"
ig = "./t4e.corpora.tokenised/0.ig1/ig1.corpus.tokenised.train.questions.txt"
docs = [ikea_en,ikea_it,ig]





def main(n,name):
	doc_words = []
	word_features = all_words.keys()[:n]
	for doc in docs:
		with open(doc,"r") as mefile:
			for line in mefile:
				doc_words += line.split()[4:-1]

	all_words = Counter(doc_words)

	f = open(name, "w")
	for bla in word_features:
		f.write(bla + "\n")
	f.close()

# word in freqdist
def idf(word,tf,freqdist):
	N =sum(freqdist.values())
	idf = math.log(N/(freqdist[word]/tf))
	return idf