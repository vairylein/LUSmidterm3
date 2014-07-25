import nltk

ikea_en = "./1.ikea/ikea.corpus.tokenised.train.questions.txt"
ikea_it = "./3.it.ikea/ikea.corpus.it.tokenised.train.questions.txt"
ig = "./0.ig1/ig1.corpus.tokenised.train.questions.txt"
docs = [ikea_en,ikea_it,ig]

def main(n,name):
	doc_words = []

	for doc in docs:
		with open(doc,"r") as mefile:
			for line in mefile:
				doc_words += line.split()[4:-1]

	all_words = nltk.FreqDist(doc_words)
	word_features = all_words.keys()[:n]


	f = open(name, "w")
	for bla in word_features:
		f.write(bla + "\n")
	f.close()
