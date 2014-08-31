from __future__ import print_function
import sys, re,math 
import SimilarityMetric as sm
import FeatureExtractor as fe
from collections import Counter

q1 = "./t4e.corpora.stemmed/0.ig1/ig1.corpus.stemmed.train.questions.txt"
a2 = "./t4e.corpora.stemmed/0.ig1/ig1.corpus.stemmed.train.answers.txt"
qapairs = "./t4e.corpora.stemmed/train.stemmed.QApairs"

qdocs = [q1]
adocs = [a2] #1st one for training
names = ["ig1.train.stemmed"]
WORDS = re.compile(r'\w+')

def accuracy(name):
	i = 0
	f = open(name + "stringsim","w")
	g = open(name + "mineditdist","w")
	h = open(name + "cosinesim","w")

	for doc in qdocs:

	#create a dictionary "a" of answers with ID as key and (rating,answersentence,questionID) as value
		adicts = {}
		with open(adocs[i],"r") as myfile:
			for line in myfile:
				elements = line.split("\t")
				sentence = elements[5].replace("<s>","").replace("</s>","").replace(",","").replace("?","").replace(".","")
				adicts[elements[0]]= (elements[6][:-1],sentence,elements[1]) # rating, answer, question

		adict = {}
		with open(adocs[i],"r") as myfile:
				for line in myfile:
					elements = line.split("\t")
					sentence = elements[5].replace("<s>","").replace("</s>","").replace(",","").replace("?","").replace(".","")
					adict[elements[0]]= WORDS.findall(sentence) # rating, answer, question
					

	#create a dictionary of answer question pairs
		qadict = {}

		with open(qapairs,"r") as mefile:
			while i <= 10:
				for line in mefile:
					elements = line[:-1].split("\t")
					aID = elements[0]
					qID = elements[1]
					if qID in qadict:
						qadict[qID] += [aID]
					else:
						qadict[qID] = [aID]
					i+=1



		questions = {} #dictionary of questions

		# f.write(names[i] + "\n")

		with open(doc,"r") as myfile:
			for line in myfile:
				elements = line.split("\t")
				questions[elements[0]] = WORDS.findall(elements[4].replace("</s>","").replace("<s>","")) # list of tuples (questionID,question)
		no_of_questions = len(questions.keys())


		totalSS = 0 # sum of string similarities
		countSS = 0 # number of correct answers
		sspointfive = 0 #number of string similarities higher than
		loop = 0
		#calculate the string similarities of correct answers
		print("number of questions for string similarity of " + str(no_of_questions) + ": ")
		for a in questions:

			solutions = sm.string_similarity(questions[a],adict)
			for possibleAns in qadict[a]:
				
				if possibleAns in solutions:
					spA = solutions[possibleAns]
					f.write(str(spA) + " ")
					totalSS += spA
					countSS+= 1
					if spA >= 0.4:
						sspointfive+=1
				else:
					print ("not found " + possibleAns + " for " + a)

			f.write("\n")

			loop +=1
			if loop % 10 == 0:
				print( (str(loop)), end='\r') 
		f.write ("average: " + str(float(totalSS)/countSS) + "\n bigger than 0.4: " + str(float(sspointfive)/countSS))
		f.close()
		print("string similarity evaluated")


		totalMED = 0 # sum of minimum edit distances
		countMED = 0 # number of correct answers
		MEDpointfive = 0 #number of string similarities higher than
		loop = 0
		#calculate min edit distance of correct answers
		print("number of questions for minimum edit distance of: " + str(no_of_questions) + ": ")
		for a in questions:

			solutionm = sm.min_edit_distance(questions[a],adict)
			for possibleAns in qadict[a]:
				
				if possibleAns in solutionm:
					spA = solutionm[possibleAns]
					g.write(str(spA) + " ")
					totalMED += spA
					countMED+= 1
					if spA <= 0.8:
						MEDpointfive+=1
				else:
					print ("not found " + possibleAns + " for " + a)

			g.write("\n")
			loop += 1
			if loop % 10 == 0:
				print((str(loop)), end='\r') 
		g.write ("average: " + str(float(totalMED)/countMED) + "\n smaller than 0.16: " + str(float(MEDpointfive)/countMED))
		g.close()
		print("minimum edit distance evaluated")

		totalCOS = 0 # sum of cosine similarities
		countCOS = 0 # number of correct answers
		COSpointfive = 0 #number of cosine similarities higher than
		r = 0
		#calculate min edit distance of correct answers
		print("number of questions for cosine similarity calculated of " + str(no_of_questions) + ": ")


		FreqDist = {}
		Nwords = 0
		for w in adict:
			sentence = adict[w]
			for word in sentence:
				if word in FreqDist:
					FreqDist[word] = FreqDist[word] + 1
					Nwords += 1
				else:
					FreqDist[word] = 1
					Nwords += 1

		AnsVec = {}
		for answer in adict:   
	# 	#answer vector 'av'
			av =[]
			acounter = Counter(adict[answer])
			for w in sorted(FreqDist.keys()):
				if w in acounter:
					av+=[acounter[w]*math.log(Nwords/(FreqDist[w]/acounter[w]))]
				else:
					av += [0]
			AnsVec[answer] = av



		for a in questions:

			solutionc = sm.cosine_similarity(questions[a],AnsVec,FreqDist)
			for possibleAns in qadict[a]:
				
				if possibleAns in solutionc:
					spA = solutionc[possibleAns]
					h.write(str(spA) + " ")
					totalCOS += spA
					countCOS+= 1
					if spA >= 0.25:
						COSpointfive+=1
				else:
					print ("not found " + possibleAns + " for " + a)

			h.write("\n")
			r +=1
			print((str(r)),end ="\r")

		h.write ("average: " + str(float(totalCOS)/countCOS) + "\n bigger than 0.25: " + str(float(COSpointfive)/countCOS))
		
		h.close()
		print("cosine similarity evaluated")

def falsey(name):
	i = 0
	f = open(name + "stringsim","w")
	g = open(name + "mineditdist","w")
	h = open(name + "cosinesim","w")

	for doc in qdocs:

	#create a dictionary "a" of answers with ID as key and (rating,answersentence,questionID) as value
		# adicts = {}
		# with open(adocs[i],"r") as myfile:
		# 	for line in myfile:
		# 		elements = line.split("\t")
		# 		sentence = elements[5].replace("<s>","").replace("</s>","").replace(",","").replace("?","").replace(".","")
		# 		adicts[elements[0]]= (elements[6][:-1],sentence,elements[1]) # rating, answer, question

		adict = {}
		with open(adocs[0],"r") as myfile:
				for line in myfile:
					elements = line.split("\t")
					sentence = elements[5].replace("<s>","").replace("</s>","").replace(",","").replace("?","").replace(".","")
					adict[elements[0]]= WORDS.findall(sentence) # ID , answer
					

	#create a dictionary of answer question pairs
		qadict = {}

		with open(qapairs,"r") as mefile:
			for line in mefile:
				elements = line[:-1].split("\t")
				aID = elements[0]
				qID = elements[1]
				if qID in qadict:
					qadict[qID] += [aID]
				else:
					qadict[qID] = [aID]



		questions = {} #dictionary of questions

		# f.write(names[i] + "\n")

		with open(doc,"r") as myfile:
			for line in myfile:
				elements = line.split("\t")
				questions[elements[0]] = WORDS.findall(elements[4].replace("</s>","").replace("<s>","")) # list of tuples (questionID,question)
		no_of_questions = len(questions.keys())

		"""
		totalSS = 0 # sum of string similarities
		countSS = 0 # number of correct answers
		sspointfive = 0 #number of string similarities higher than
		r = 0
		#calculate the string similarities of correct answers
		print("number of questions for string similarity of " + str(no_of_questions) + ": ")
		for a in questions:
			f.write(a)
			solutions = sm.string_similarity(questions[a],adict)
			for sol in solutions:
				f.write("," + sol + " " + str(round(solutions[sol],4)))
			f.write("\n")
			r+=1
			print((str(r)),end ="\r")
			
		f.close()
		print("string similarity evaluated")


		totalMED = 0 # sum of minimum edit distances
		countMED = 0 # number of correct answers
		MEDpointfive = 0 #number of string similarities higher than
		r = 0
		#calculate min edit distance of correct answers
		print("number of questions for minimum edit distance of: " + str(no_of_questions) + ": ")
		for a in questions:
			g.write(a)
			solutionm = sm.min_edit_distance(questions[a],adict)
			for sol in solutionm:
				g.write("," + sol + " " + str(round(solutionm[sol],4)))
			g.write("\n")
			r+=1
			print((str(r)),end ="\r")

		g.close()
		print("minimum edit distance evaluated")

		"""

		totalCOS = 0 # sum of cosine similarities
		countCOS = 0 # number of correct answers
		COSpointfive = 0 #number of cosine similarities higher than
		r = 0
		#calculate min edit distance of correct answers
		print("number of questions for cosine similarity calculated of " + str(no_of_questions) + ": ")

		# counts the frequencies of every word in the form FreqDist0[word] = frequency
		FreqDist0 = {}
		
		Nwords = 0 #Number of words in total
		for w in adict:
			sentence = adict[w]
			for word in sentence:
				if word in FreqDist0:
					FreqDist0[word] = FreqDist0[word] + 1
					Nwords += 1
				else:
					FreqDist0[word] = 1
					Nwords += 1


		Nans = len(adict.keys())
		
		FreqDist = {}
		for w in FreqDist0:
			included = 0
			for a in adict:
				if w in adict[a]:
					included += 1
			FreqDist[w]= math.log(float(Nans)/included)


		AnsVec = {}
		for answer in adict:   
		#answer vector 'av'
			av =[]
			acounter = Counter(adict[answer])
			for w in sorted(FreqDist0.keys()):
				if w in acounter:
					av+= [acounter[w]*FreqDist[w]]
				else:
					av += [0]
			AnsVec[answer] = av



		for a in questions:
			h.write(a)
			solutionc = sm.cosine_similarity(questions[a],AnsVec,FreqDist)
			for sol in solutionc:
				h.write("," + sol + " " + str(round(solutionc[sol],4)))

			h.write("\n")
			r+=1
			print((str(r)),end ="\r")
		
		h.close()
		print("cosine similarity evaluated")

if __name__ == '__main__':
    falsey(sys.argv[1])





#if a in sm.string_similarity(b,adict):
				#f.write(a + "found using string_similarity")
			# else:
			# 	f.write("string similarity doesn't  ")
			# if a in sm.min_edit_distance(b,adict):
			# 	f.write("min_edit_distance has it   ")
			# else:
			# # 	f.write("min_edit_distance doesn't  ")
			# #for c,d,e in sm.cosine_similarity(b,adict):
			# 	if e ==a:
			# 		f.write("cosine_similarity has it  %s %s" % (c,d))
				
			
		#f.write("\n\n")