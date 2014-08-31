import NaiveBayes, Evaluate, sys

test_stemmed_a = "./t4e.corpora.for.test/stemmed.test/answer.txt"
test_stemmed_q = "./t4e.corpora.for.test/stemmed.test/questions.txt"
stemmed_a = "./t4e.corpora.stemmed/train.stemmed.answers"
stemmed_q = "./t4e.corpora.stemmed/train.stemmed.questions"
stemmed_docs_final = [stemmed_q,stemmed_a, test_stemmed_q,test_stemmed_a]

test_tokenised_a = "./t4e.corpora.for.test/tokenised.test/answer.txt"
test_tokenised_q = "./t4e.corpora.for.test/tokenised.test/questions.txt"
tokenised_a = "./t4e.corpora.tokenised/train.tokenised.answers"
tokenised_q = "./t4e.corpora.tokenised/train.tokenised.questions"
tokenised_docs_final = [tokenised_q,tokenised_a, test_tokenised_q,test_tokenised_a]

if __name__ = == '__main__':
	NaiveBayes.
