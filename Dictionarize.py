from __future__ import print_function
import sys


qapairs = "./t4e.corpora.stemmed/train.stemmed.QApairs"

def put(name, value, greatorless):

	with open("valuesstringsim","r") as myfile:
		solutions0 = myfile.readlines()
	f = open(name + "stringsim", "w")

	with open("valuesmineditdist","r") as myfile:
		solutions1 = myfile.readlines()
	g = open(name + "mineditdist", "w")

	with open("idfcosinesim","r") as myfile:
		solutions2 = myfile.readlines()
	h = open(name + "cosinesim", "w")

	label = ["stringsim", "mineditdist", "cosinesim"]

	values = []
	for v in value.split(","):
		values += [float(v)]

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

	i = 0
	r = 0
	for solution in [solutions0,solutions1,solutions2]:
		print(greatorless[i])
		print ("processing " + label[i] + "of 319 for " + str(values[i]))
		sumcorrect = 0
		sumincorrect = 0
		for sol in solution:

			dic = {}
			solcomma = sol[:-1].split(",")
			questionID = solcomma[0]
			answerIDs = qadict[questionID]
			for sols in solcomma[1:]:
				elements = sols.split(" ")
				dic[elements[0]] = float(elements[1])

			correct = 0
			incorrect = 0
			for d in dic:
				if greatorless[i] == 'g':
					if dic[d] >= values[i]:
						if d in answerIDs:
							correct += 1
						else:
							incorrect += 1
				elif greatorless[i] == "l":
					if dic[d] <= values[i]:
						if d in answerIDs:
							correct += 1
						else:
							incorrect += 1

			r+=1

			print((str(r)),end="\r")

			if i == 0:
				f.write(str(correct) + "\t" + str(incorrect) + "\t" + str(incorrect+correct) + "\n")
			elif i == 1:
				g.write(str(correct) + "\t" + str(incorrect) + "\t" + str(incorrect+correct)  + "\n")
			elif i == 2:
				h.write(str(correct) + "\t" + str(incorrect) + "\t" + str(incorrect+correct)  + "\n")

			sumcorrect += correct
			sumincorrect += incorrect

		if i == 0:
			f.write(str(sumcorrect) + "\t" + str(sumincorrect) + "\t" + str(sumincorrect+sumcorrect)  + "\n")
			print(str(sumcorrect) + " " + str(sumincorrect) + " " + str(sumincorrect+sumcorrect)  + "\n")
		elif i == 1:
			g.write(str(sumcorrect) + "\t" + str(sumincorrect) + "\t" + str(sumincorrect+sumcorrect)  + "\n")
			print(str(sumcorrect) + " " + str(sumincorrect) + " " + str(sumincorrect+sumcorrect)  + "\n")
		elif i == 2:
			h.write(str(sumcorrect) + "\t" + str(sumincorrect) + "\t" + str(sumincorrect+sumcorrect)  + "\n")
			print(str(sumcorrect) + " " + str(sumincorrect) + " " + str(sumincorrect+sumcorrect)  + "\n")

		i+=1

if __name__ == '__main__':
    put(sys.argv[1],sys.argv[2], sys.argv[3])
