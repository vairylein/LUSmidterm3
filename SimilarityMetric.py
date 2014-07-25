import re, math
from nltk import metrics
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
			a[sentence]= (elements[6][:-1],l)
			l+=1

	#create a list of string similarity values
	N = []
	for answer in a:
		n= 0
		for word in qs:
			if word in WORDS.findall(answer):
				n+=1
		print n
		N+=[(float(n)/qlength*100,answer)]

	return N



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
			a[sentence]= (elements[6][:-1],l)
			l+=1

	#create a list of MED values
	N = []
	for answer in a:
		n = metrics.edit_distance(qs,WORDS.findall(answer))
		N+= [(n,answer)]

	return N

#cosine similarity on pure token frequency
def cosine_similarity(q, answers):

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
			a[sentence]= (elements[6][:-1],l)
			l+=1

	#create a list of cossim values
	
	qv = Counter(qs)#question vector 'qv'
	N = []
	for answer in a:
		av = Counter(WORDS.findall(answer))    #answer vector 'av'
		intersection = set(qv.keys()) & set(av.keys())
		print intersection
		numerator = sum([qv[x]*av[x] for x in intersection])

		sum1 = sum([qv[x]**2 for x in qv.keys()])
		sum2 = sum([av[x]**2 for x in av.keys()])
		denominator = math.sqrt(sum1) * math.sqrt(sum2)

		if not denominator:
			N+= [(0.0,answer)]
		else:
			N+= [((float(numerator)/denominator),answer)]


	return N


