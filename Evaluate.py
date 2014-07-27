import SimilarityMetric as sm
q1 = ./t4e.corpora.stemmed/0.ig1/ig1.corpus.stemmed.train.questions.txt
a2 = ./t4e.corpora.stemmed/0.ig1/ig1.corpus.stemmed.train.answers.txt

qdocs = [q1]
adocs = [a2]
names = ["ig1.train.stemmed"]

def accuracy(name):
	for doc in aqdocs:
		with open(doc,"r") as myfile:
			doct = myfile.readlines()
	sm.string_similarity()


if __name__ == '__main__':
    levensht(sys.argv[1])