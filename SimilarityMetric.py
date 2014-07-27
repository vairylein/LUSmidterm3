import re, math, nltk
import FeatureExtractor
from collections import Counter

WORDS = re.compile(r'\w+')

def string_similarity(q, answers):
	#split question into words remove artefacts
	qs = WORDS.findall(q.replace("</s>","").replace("<s>",""))
	qlength = len(qs)

	#create a dictionary "a" of answers with sentences as key and (line number,rating) as value
	a = {}
	l= 0
	with open(answers,"r") as myfile:
		for line in myfile:
			elements = line.split("\t")
			sentence = elements[5].replace("<s>","").replace("</s>","").replace(",","").replace("?","").replace(".","")
			a[sentence]= (elements[6][:-1],elements[0],elements[1]) # rating, answer, question
			l+=1

	#create a list of string similarity values
	N = []
	values=[]
	for answer in a:
		n= 0
		for word in qs:
			if word in answer.split():
				n+=1
		N+=[(float(n)/qlength*100,answer)]
		values += [(float(n)/qlength*100)]
	best10 = []
	for (num,ans) in N:
		if num <= sorted(values)[10]:
			best10 += a[ans]

	return best10
	#return N



def min_edit_distance(q, answers):

	#split question into words remove artefacts
	qs = WORDS.findall(q.replace("</s>","").replace("<s>",""))
	qlength = len(qs)

	#create a dictionary "a" of answers with sentences as key and (line number,rating) as value
	a = {}
	l= 0
	with open(answers,"r") as myfile:
		for line in myfile:
			elements = line.split("\t")
			sentence = elements[5].replace("<s>","").replace("</s>","")
			a[sentence]= (elements[6][:-1],elements[1],elements[2]) # rating, answer, question

	#create a list of MED values
	N = []
	values = []
	for answer in a:
		n = nltk.metrics.edit_distance(qs,WORDS.findall(answer))
		N+= [(n,answer)]
		values += [n]

	best10 = []
	for (num,ans) in N:
		if num <= sorted(values)[10]:
			best10 += a[ans]

	return best10
	#return N

#cosine similarity on pure token frequency
def cosine_similarity(q, answers):

	#split question into words remove artefacts
	qs = WORDS.findall(q.replace("</s>","").replace("<s>",""))
	qlength = len(qs)

	#create a dictionary "a" of answers with sentences as key and (line number,rating) as value
	a = {}
	
	with open(answers,"r") as myfile:
		for line in myfile:
			elements = line.split("\t")
			sentence = elements[5].replace("<s>","").replace("</s>","")
			a[sentence]= (elements[6][:-1],elements[1],elements[2]) # rating, answer, question

	allwords = []
	for w in a.keys():
		allwords += WORDS.findall(w)

	fd = Counter(allwords)
	
	#question vector
	qv =[]
	qcounter = Counter(qs)
	for w in sorted(fd.keys()):
		if w in qcounter.keys():
			qv+=[qcounter[w]*FeatureExtractor.idf(w,qcounter[w],fd)]

		else:
			qv += [0]



	#question vector 'qv'
	N = []
	for answer in a:
		#av = Counter(WORDS.findall(answer))    #answer vector 'av'
		av =[]
		acounter = Counter(answer.split())
		for w in sorted(fd.keys()):
			if w in acounter.keys():
				av+=[acounter[w]*FeatureExtractor.idf(w,acounter[w],fd)]
			else:
				av += [0]
		#print intersection
		numerator = sum([qv[x]*av[x] for x in range(len(av))])

		sum1 = sum([qv[x]**2 for x in range(len(av))])
		sum2 = sum([av[x]**2 for x in range(len(av))])
		denominator = math.sqrt(sum1) * math.sqrt(sum2)


		if not denominator:
			N+= [(0.0,answer)]
		else:
			N+= [((float(numerator)/denominator),answer)]
			if (float(numerator)/denominator)>0.2:
				print ((float(numerator)/denominator),answer)
	best10 = []
	for (num,ans) in N:
		if num <= sorted(values)[10]:
			best10 += a[ans]

	return best10
	#return N


