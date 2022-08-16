import textract
import re
import math
import pandas as pd
import os
import sys

#vals = sys.argv[1].split(",")
#vals = [v.strip() for v in vals]

class ReadIndirect:
	#this is the folder that holds the direct assessment reports
	__indirectFolder = None

	__saveDirectory = None

	__header = ["Class", "Section", "Total Students", "No. of Student Responses", "Total Responses", "E", "G", "N", "F", "P", "N/A", "E+G", "average"]

	#this will hold the individual data
	__data = list()

	#this is the output name
	__name = ""

	#this is the terminal
	__terminal = None

	def __init__(self, indirectFolder, saveDirectory, name, terminal):
		self.__indirectFolder = indirectFolder
		self.__saveDirectory = saveDirectory
		self.__name = name
		self.__terminal = terminal

	def startTool(self):
		files = os.listdir(self.__indirectFolder)

		for f in files:
			if f != ".DS_Store":
				self.__terminal.enterLine("Working on " + f)
				self.__terminal.idle_task()
				clss, sec, text = self.openReadPDF(self.__indirectFolder, f) #open and read the file
				allPer, stringWithPercentage = self.findPossiblePercentages(text) #find all possible percentages, and where the total student information is kept
				sentences = self.findTheData(text) #find the sentence data where the results are stored

				evaluated, categories = self.parseData(sentences) #find how many students have been evaluated, and how many the pared data

				#Find the total number of students
				total = ''
				i = len(allPer)
				correctPercentage = -1
				while i > 0:
					i -= 1

					#the string returned is where this data is stored
					if stringWithPercentage.find(evaluated+allPer[i]) != -1:
						total = stringWithPercentage[0:stringWithPercentage.find(evaluated+allPer[i])]
						correctPercentage = i #save the index of the correct percentage
						break

				if total == '':
					i = len(allPer)
					while i > 0:
						i -= 1

						if float(allPer[i]) <= 0.0:
							continue

						genTotal = 100. * float(evaluated) / float(allPer[i])

						generatedString = str(int(genTotal)) + str(evaluated) + str(allPer[i])

						if stringWithPercentage == generatedString:
							total = genTotal

				if total == '':
					self.__terminal.enterLine("--------------------")
					self.__terminal.enterLine("There is a problem with the file " + f)
					self.__terminal.enterLine("--------------------")
					continue

				if len(total) > 2:
					i = int(len(total) / 2)
					correct = False
					while i < len(total):
						tempTotal = total[0:i]
						val = total[i:]
						if str(float(int(val) / int(tempTotal) * 100)) == allPer[correctPercentage]:
							correct == True
							break
						i+=1

					if not correct:
						self.__terminal.enterLine("--------------------")
						self.__terminal.enterLine("There is a problem with the file " + f)
						self.__terminal.enterLine("--------------------")
						continue


				numerical = self.numericalData(evaluated, categories)

				self.__data.append(["CS"+clss, int(sec), total, evaluated, 7*int(evaluated)])

				sums = [numerical[k][1] for k in numerical]
				for sms in sums:
					for v in sms:
						sms[sms.index(v)] = float('{:.0f}'.format(v))
						
				s = sums[0]
				for i in range(1, len(sums)):
					res = list()
					for i1, i2 in zip(s, sums[i]):
						#sti1 = '{:.0f}'.format(i1)
						#sti2 = '{:.0f}'.format(i2)
						res.append(i1+i2)

						s = res

				for i in s:
					self.__data[-1].append('{:.2f}'.format(i))

				#Find a weighted average
				average = 0
				v = 5
				for i in s:
					average += v*float(i)
					v-=1

				average /= 7*int(evaluated)

				self.__data[-1].append(s[0]+s[1])
				self.__data[-1].append('{:.2f}'.format(average))

		df = pd.DataFrame(self.__data, columns=self.__header)
		df = df.sort_values(by=['Class', 'Section'])


		df.to_csv(self.__saveDirectory + "/" + self.__name + ".csv")
		self.__terminal.enterLine("Done")

				#c+=1
				#print("Completed ", c, "file")



	def openReadPDF(self, loc, file):
		text = textract.process(loc + "/" + file, method="pdfminer", encoding="ascii")

		#-------------------------------
		#Find the class that this is for
		#-------------------------------
		dashInd = str(text).find("-")

		clss = str(text)[dashInd-3:dashInd]
		if int(clss) >= 600:
			temp = int(clss) - 200
			clss = str(temp)
		sec = str(text)[dashInd+1:dashInd+5]

		return clss, sec, text

	def findPossiblePercentages(self, text):
		#the percentage value begins befor this string, this is the percentage symbol %
		per = str(text).find("Creation Date") - 1 
		cdi = per #this value will index backwards to the decimal point
		decimalStr = '' #this will hold the decimal value

		while(str(text)[cdi] != '.'):
			cdi -= 1

		decimalStr = str(text)[cdi:per] #save the values after the decimal point
		allPercentages = list() #now we create a list of the possible percentages writtens
		tens = cdi #this will count down the tens
		c = 0 #don't go over 3 digits in the whole numbers places

		while c < 4:
			#print(str(text)[tens:per])
			if float(str(text)[tens:cdi] + decimalStr) <= 100.0:
				allPercentages.append(str(text)[tens:cdi] + decimalStr)
			tens -= 1
			c+= 1

		boundary = str(text).find("Course Evaluations")
		checkPer = str(text)[boundary+len("Course Evaluations"):per] #this is the boundary of where the percentage and the total students are

		return allPercentages, checkPer

	def findTheData(self, text):
		categories = {"The material was presented clearly":[], 
		"Instructor was genuinely interested in educating the students.": [],
		"The assignments, quizzes, and tests were fair and covered the material emphasized.":[], 
		"Instructor was well prepared in class meetings.": [],
		"Instructor was available to answer questions.": [],
		"Instructor covered the material listed in the syllabus.": [], 
		"overall performance in this course was excellent.": []}

		#I want the find the data for the different questions (labeled categories here)
		#this is don't by just getting the keys of the dictionary above
		findSentences = list(categories.keys())
		findSentences.append("Ranking Summary")

		#This will be the data for each question, they are saved a sentences
		sentences = list()

		#This is finding where the data is for each question
		for i in range(len(findSentences)):
			if i != 7:
				s = str(text).find(findSentences[i]) #the data we need is between this first question
				e = str(text).find(findSentences[i+1]) #and this next question
				q = str(text)[s:e] #this will grab the sentence of data

				data = q[q.find("Overall") + len("Overal"): q.find("Dept")] #simplify the search, cause we only need a section of it
				sentences.append(data)

		return sentences

	def parseData(self, sentences):
		evaluated = '' #this is the number of students evaluated

		categories = {"The material was presented clearly":[], 
		"Instructor was genuinely interested in educating the students.": [],
		"The assignments, quizzes, and tests were fair and covered the material emphasized.":[], 
		"Instructor was well prepared in class meetings.": [],
		"Instructor was available to answer questions.": [],
		"Instructor covered the material listed in the syllabus.": [], 
		"overall performance in this course was excellent.": []}

		findSentences = list(categories.keys())

		#Start looking through the sentences
		for s in range(0, len(sentences)):
			substr = "%"
			pos = [_.start() for _ in re.finditer(substr, sentences[s])]
			perc = list() #This is the percentage list
			sumSoFar = 0.
			for i in range(0, len(pos)-1):
				perc.append(float(sentences[s][pos[i]:pos[i+1]][1:]))
				sumSoFar += perc[-1]

			remaining = 100.-sumSoFar #this is the percentage we haven't found so far
			if remaining < 0:
				perc.insert(0, "0.00")
			else:
				perc.insert(0, "{:.2f}".format(remaining))

			#This is how we find how many students actuall took the class
			strng = perc[0]

			j = pos[0] - len(strng)
			evaluated = sentences[s][1:j]

			categories[findSentences[s]] = perc

		return evaluated, categories

	def numericalData(self, evaluated, categories):

		for k in categories.keys():
			ls = categories[k]
			categories[k]=list()
			numerical = list()
			for p in ls:
				numerical.append(float(p)*float(evaluated)/100.)

			#append both lists to the questions definition
			categories[k].append(ls)
			categories[k].append(numerical)

		return categories

#readInd = readIndirect("/Users/dubliciousbaby/Desktop/indirect_assessment_2/", "results_testing.csv")
#readInd.startTool()

"""folder = "/Users/dubliciousbaby/Desktop/indirect_assessment_2/" #this is the folder where all the indirect files are stored

files = os.listdir(folder)

header = ["Class", "Section", "Total Students", "No. of Student Responses", "Total Responses", "E", "G", "N", "F", "P", "N/A", "E+G", "average"]
data = list()

c = 0
for f in files:
	if f != ".DS_Store":
		print("Working on " + f)
		sys.stdout.flush()
		clss, sec, text = openReadPDF(folder, f) #open and read the file
		allPer, stringWithPercentage = findPossiblePercentages(text) #find all possible percentages, and where the total student information is kept
		sentences = findTheData(text) #find the sentence data where the results are stored

		evaluated, categories = parseData(sentences) #find how many students have been evaluated, and how many the pared data

		#Find the total number of students
		total = ''
		i = len(allPer)
		correctPercentage = -1
		while i > 0:
			i -= 1

			#the string returned is where this data is stored
			if stringWithPercentage.find(evaluated+allPer[i]) != -1:
				total = stringWithPercentage[0:stringWithPercentage.find(evaluated+allPer[i])]
				correctPercentage = i #save the index of the correct percentage
				break

		if total == '':
			i = len(allPer)
			while i > 0:
				i -= 1

				if float(allPer[i]) <= 0.0:
					continue

				genTotal = 100. * float(evaluated) / float(allPer[i])

				generatedString = str(int(genTotal)) + str(evaluated) + str(allPer[i])

				if stringWithPercentage == generatedString:
					total = genTotal

		if total == '':
			print("--------------------")
			print("There is a problem with the file " + f)
			print("--------------------")
			continue

		if len(total) > 2:
			i = int(len(total) / 2)
			correct = False
			while i < len(total):
				tempTotal = total[0:i]
				val = total[i:]
				if str(float(int(val) / int(tempTotal) * 100)) == allPer[correctPercentage]:
					correct == True
					break
				i+=1

			if not correct:
				print("--------------------")
				print("There is a problem with the file " + f)
				print("--------------------")
				continue


		numerical = numericalData(evaluated, categories)

		data.append(["CS"+clss, int(sec), total, evaluated, 7*int(evaluated)])

		sums = [numerical[k][1] for k in numerical]
		for sms in sums:
			for v in sms:
				sms[sms.index(v)] = float('{:.0f}'.format(v))
				
		s = sums[0]
		for i in range(1, len(sums)):
			res = list()
			for i1, i2 in zip(s, sums[i]):
				#sti1 = '{:.0f}'.format(i1)
				#sti2 = '{:.0f}'.format(i2)
				res.append(i1+i2)

				s = res

		for i in s:
			data[-1].append('{:.2f}'.format(i))

		#Find a weighted average
		average = 0
		v = 5
		for i in s:
			average += v*float(i)
			v-=1

		average /= 7*int(evaluated)

		data[-1].append(s[0]+s[1])
		data[-1].append('{:.2f}'.format(average))

		c+=1
		#print("Completed ", c, "file")
		

df = pd.DataFrame(data, columns=header)
df = df.sort_values(by=['Class', 'Section'])


df.to_csv("/Users/dubliciousbaby/Desktop/indirect_assessment_2/results.csv")""" #save this to a csv file


