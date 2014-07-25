

def string_similarity(q, answers):

	#create a dictionary "a" of answers with sentences as key and rating as value
	a = {}
	with open(answers,"r") as myfile:
		for line in myfile:
			elements = line.split("\t")
			sentence = elements[5].replace("<s>","").replace("</s>","")
			a[sentence]= elements[6][:-1]

	#create a list of string similarity values
	for answer in a:
		n= 0
		for word in q:
			if word in a:
				n+=1
	return n/100


def min_edit_distance(q, answers):

	#create a dictionary "a" of answers with sentences as key and rating as value
	a = {}
	with open(answers,"r") as myfile:
		for line in myfile:
			elements = line.split("\t")
			sentence = elements[5].replace("<s>","").replace("</s>","")
			a[sentence]= elements[6][:-1]


def cosine_similarity(q, answers):

	#create a dictionary "a" of answers with sentences as key and rating as value
	a = {}
	with open(answers,"r") as myfile:
		for line in myfile:
			elements = line.split("\t")
			sentence = elements[5].replace("<s>","").replace("</s>","")
			a[sentence]= elements[6][:-1]


