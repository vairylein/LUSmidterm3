from __future__ import division
import FeatureExtractor
import math, sys

test_stemmed_a = "./t4e.corpora.stemmed/test.stemmed.answers"
test_stemmed_q = "./t4e.corpora.stemmed/test.stemmed.questions"
val_stemmed_a = "./t4e.corpora.stemmed/validation.stemmed.answers"
val_stemmed_q = "./t4e.corpora.stemmed/validation.stemmed.questions"
stemmed_a = "./t4e.corpora.stemmed/train.stemmed.answers"
stemmed_q = "./t4e.corpora.stemmed/train.stemmed.questions"
stemmed_docs = [stemmed_q,stemmed_a,val_stemmed_q,val_stemmed_a]
stemmed_docs_final = [stemmed_q,stemmed_a, test_stemmed_q,test_stemmed_a]

test_tokenised_a = "./t4e.corpora.tokenised/test.tokenised.answers"
test_tokenised_q = "./t4e.corpora.tokenised/test.tokenised.questions"
val_tokenised_a = "./t4e.corpora.tokenised/validation.tokenised.answers"
val_tokenised_q = "./t4e.corpora.tokenised/validation.tokenised.questions"
tokenised_a = "./t4e.corpora.tokenised/train.tokenised.answers"
tokenised_q = "./t4e.corpora.tokenised/train.tokenised.questions"
tokenised_docs = [tokenised_q,tokenised_a,val_tokenised_q,val_tokenised_a]
tokenised_docs_final = [tokenised_q,tokenised_a, test_tokenised_q,test_tokenised_a]


def validate(doc, name):

	f= open(name,"w")

	frequencies0 = FeatureExtractor.frequency(doc[:2]) #frequency count smoothed by 1
	frequencies1 = FeatureExtractor.augmented_frequency(frequencies0) # augmented frequencies taking into account document size
	frequencies = FeatureExtractor.idf(frequencies1) # idfs
	total = frequencies["**prob**"]
	totals = sum(total)

	priors =[0.33, 0.33, 0.328] # based on number of documents


	a = ["C2","IKEA_EN","IKEA_IT"]
	correct = 0
	number = 0

	tpC2      = 0
	tpIKEA_EN = 0
	tpIKEA_IT = 0
	fpC2      = 0
	fpIKEA_EN = 0
	fpIKEA_IT = 0
	fnC2      = 0
	fnIKEA_EN = 0
	fnIKEA_IT = 0


	with open(doc[2],"r") as mefile:

		for line in mefile:
			lines = line.split('\t')
			ID = lines[1]
			words = lines[4].replace("<s>","").replace("</s>","").split(" ")
			pC2 = 0
			pIKEA_IT = 0
			pIKEA_EN = 0
			for word in words:
				
				if word in frequencies:
					pC2 += math.log((frequencies[word][0]))
					pIKEA_EN += math.log((frequencies[word][1]))
					pIKEA_IT += math.log((frequencies[word][2]))

				else:
					pC2 += math.log(0.5)
					pIKEA_EN += math.log(0.5)
					pIKEA_IT += math.log(0.5)
			
			b = [pC2+math.log(priors[0]),pIKEA_EN+math.log(priors[1]),pIKEA_IT+math.log(priors[2])]
			# other possibilities
			# d = [pC2,pIKEA_EN,pIKEA_IT] # without priors
			# c = [-pC2*priors[0],-pIKEA_EN*priors[1],-pIKEA_IT*priors[2]] # multiplying by priors
			
			

			proposal = a[b.index(max(b))]
			f.write(proposal + "\t" + ID + "\n")

			# calculate precision, recall, f1
			# count true positives, false positives, false negatives
			print proposal
			

			if ID == proposal:
				if ID == "C2":
					tpC2+=1
				elif ID == "IKEA_EN":
					tpIKEA_EN +=1
				elif ID == "IKEA_IT":
					tpIKEA_IT += 1
				correct += 1
			else:
				if ID == "C2":
					fnC2+=1
				elif ID == "IKEA_EN":
					fnIKEA_EN +=1
				elif ID == "IKEA_IT":
					fnIKEA_IT += 1
				if proposal == "C2":
					fpC2+=1
				elif proposal == "IKEA_EN":
					fpIKEA_EN +=1
				elif proposal == "IKEA_IT":
					fpIKEA_IT += 1

			number +=1

	print fnC2
	precisionC2 = tpC2 / ( tpC2 + fpC2 )
	precisionIKEA_IT = tpIKEA_IT / ( tpIKEA_IT + fpIKEA_IT)
	precisionIKEA_EN = tpIKEA_EN / ( tpIKEA_EN + fpIKEA_EN)
	precisions = [precisionC2, precisionIKEA_EN,precisionIKEA_IT]
	recallC2 = tpC2 / ( tpC2 + fnC2 )
	recallIKEA_IT = tpIKEA_IT / ( tpIKEA_IT + fnIKEA_IT)
	recallIKEA_EN = tpIKEA_EN / ( tpIKEA_EN + fnIKEA_EN)
	recalls = [recallC2,recallIKEA_EN,recallIKEA_IT]

	avgpre = sum(precisions)/3
	avgrec = sum(recalls)/3



	f.write("\n\ncorrect: " + str(correct) + "out of" + str(number))
	f.write("\nprecision: " + str(avgpre))
	f.write("\nrecall: " + str(avgrec))
	f.write("\nF1: " + str( 2* ((avgpre*avgrec) / (avgpre + avgrec)) ))

	f.close()

def test(doc, name):

	f= open(name,"w")

	frequencies0 = FeatureExtractor.frequency(doc[:2],True,True) #frequency count smoothed by 1
	frequencies1 = FeatureExtractor.augmented_frequency(frequencies0) # augmented frequencies taking into account document size
	frequencies = FeatureExtractor.idf(frequencies1) # idfs
	total = frequencies["**prob**"]
	totals = sum(total)

	priors =[0.33, 0.33, 0.329] # based on number of documents

	a = ["C2","IKEA_EN","IKEA_IT"]


	with open(doc[2],"r") as mefile:

		for line in mefile:
			lines = line.split('\t')
			ID = lines[0]
			words = lines[4].replace("<s>","").replace("</s>","").split(" ")
			pC2 = 0
			pIKEA_IT = 0
			pIKEA_EN = 0
			for word in words:
				
				if word in frequencies:
					pC2 += math.log((frequencies[word][0]))
					pIKEA_EN += math.log((frequencies[word][1]))
					pIKEA_IT += math.log((frequencies[word][2]))

				else:
					pC2 += math.log(0.5)
					pIKEA_EN += math.log(0.5)
					pIKEA_IT += math.log(0.5)
			
			b = [pC2+math.log(priors[0]),pIKEA_EN+math.log(priors[1]),pIKEA_IT+math.log(priors[2])]
			
			

			proposal = a[b.index(max(b))]
			f.write(ID+ "\t" + proposal + "\n")


	f.close()


if __name__ == '__main__':
	if sys.argv[1] == "stemmed_validate":
		validate(stemmed_docs, "NB.stemmed.val.q")
	elif sys.argv[1] == "tokenised_validate":
		validate(tokenised_docs, "NB.tokenised.val.q")
	elif sys.argv[1] == "tokenised_test":
		test(tokenised_docs_final, "NB.tokenised.test")
	if sys.argv[1] == "stemmed_test":
		test(stemmed_docs_final, "NB.stemmed.test")


