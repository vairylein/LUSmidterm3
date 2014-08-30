import sys
import SimilarityMetric as sm
q1 = "./t4e.corpora.stemmed/0.ig1/ig1.corpus.stemmed.train.questions.txt"
a2 = "./t4e.corpora.stemmed/0.ig1/ig1.corpus.stemmed.train.answers.txt"

qdocs = [q1]
adocs = [a2]
names = ["ig1.train.stemmed"]

def accuracy(name):
	i = 0
	f= open(name,"w")

	for doc in qdocs:

	#create a dictionary "a" of answers with sentences as key and (line number,rating) as value
		adict = {}
		l= 0
		with open(adocs[i],"r") as myfile:
			for line in myfile:
				elements = line.split("\t")
				sentence = elements[5].replace("<s>","").replace("</s>","").replace(",","").replace("?","").replace(".","")
				adict[sentence]= (elements[6][:-1],elements[0],elements[1]) # rating, answer, question
				l+=1

		questions = []
		f.write(name[i] + "\n")
		with open(doc,"r") as myfile:
			for line in myfile:
				elements = line.split("\t")
				questions += [(elements[0],elements[4])]
		for a,b in questions:
			# if a in sm.string_similarity(b,adict):
			# 	f.write("string_similarity has it   ")
			# else:
			# 	f.write("string similarity doesn't  ")
			# if a in sm.min_edit_distance(b,adict):
			# 	f.write("min_edit_distance has it   ")
			# else:
			# 	f.write("min_edit_distance doesn't  ")
			for c,d,e in sm.cosine_similarity(b,adict):
				if e ==a:
					f.write("cosine_similarity has it  %s %s" % (c,d))
				
			
			f.write("\n\n")

		i+=1
	f.close()
if __name__ == '__main__':
    accuracy(sys.argv[1])