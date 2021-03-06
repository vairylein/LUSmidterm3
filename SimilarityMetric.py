from __future__ import division, print_function
import re, math, nltk
import FeatureExtractor
from collections import Counter

WORDS = re.compile(r'\w+')

def string_similarity(q, answers):
	#split question into words remove artefacts
	
	qs = list(set(q))
	qlength = len(qs)

	
	#create a list of string similarity values
	N = {}
	values=[]
	for answer in answers:
		n= 0
		for word in qs:
			if word in answers[answer]:
				n+=1
		N[answer] = (float(n)/qlength)
	
	# best10 = []
	# for (num,ans) in N:
	# 	if num <= 0.6 :

	# 		best10 += [ans]

	# return best10
	return N




def min_edit_distance(qs, answers):

	#split question into words remove artefacts
	qlength = len(qs)

	#create a list of MED values
	N = {}
	for answer in answers:
		sentenceanswer = answers[answer]
		salength= len(sentenceanswer)
		n = nltk.metrics.edit_distance(qs,sentenceanswer)
		N[answer] = n/salength
	# best10 = []
	# for (num,ans) in N:
	# 	if num <= sorted(values)[10]:
	# 		best10 += [answers[ans][2]]

	#return best10
	return N

#cosine similarity on pure token frequency
def cosine_similarity(qs, answervectors, FreqDist):

	#split question into words remove artefacts
	qlength = len(qs)

	
	
	# FreqDist = {}
	Nwords = len(FreqDist.keys())
	# for w in answers.keys():
	# 	sentence = answers[w]
	# 	for word in sentence:
	# 		if word in FreqDist:
	# 			FreqDist[word] = FreqDist[word] + 1
	# 			Nwords += 1
	# 		else:
	# 			FreqDist[word] = 1
	# 			Nwords += 1
		
	
	#question vector using idf
	qv =[]
	qcounter = Counter(qs)
	sortedFD = sorted(FreqDist.keys())
	for w in sortedFD:
		if w in qcounter:
			qv+=[qcounter[w]*FreqDist[w]]

		else:
			qv += [0]
		# if w in qcounter:
		# 	qv+=[qcounter[w]*math.log(Nwords/(FreqDist[w]/qcounter[w]))]

		# else:
		# 	qv += [0]


	N = {}
	
	for avs in answervectors:
		av = answervectors[avs]
		numerator = sum([qv[x]*av[x] for x in range(Nwords)])

		sum1 = sum([qv[x]**2 for x in range(Nwords)])
		sum2 = sum([av[x]**2 for x in range(Nwords)])
		denominator = math.sqrt(sum1) * math.sqrt(sum2)

		
		if not denominator:
			N[avs] = 0.0

		else:
			N[avs]= (float(numerator)/denominator)
		
			


	# best10 = []

	# for (num,ans) in N:
	# 	if num >= sorted(values)[-10]:
	# 		best10 += [answers[ans]]

	# return best10
	return N


