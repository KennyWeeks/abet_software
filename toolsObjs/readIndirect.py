#import textract
import re
import math
import pandas as pd
import os
import sys
import json
"""import pdftotext

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

	__questions = ["The material was presented clearly.", 
"Instructor was genuinely interested in educating the students.", 
"The assignments, quizzes, and tests were fair and covered the material emphasized.",
"Instructor was well prepared in class meetings.", 
"Instructor was available to answer questions.", 
"Instructor covered the material listed in the syllabus.", 
"Instructor's overall performance in this course was excellent.", 
"Ranking Summary"]

	def __init__(self, indirectFolder, saveDirectory, name, terminal):
		self.__indirectFolder = indirectFolder
		self.__saveDirectory = saveDirectory
		self.__name = name
		self.__terminal = terminal

	def readTool(self):

		totalData = list()

		for files in os.listdir(self.__indirectFolder):
			individualData = list()
			with open(self.__indirectFolder + "/" + files, "rb") as f:
				try:
					pdf = pdftotext.PDF(f)
				except:
					print("Broke at this file " + files)
					continue

				self.__terminal.enterLine("Reading this file --> " + files)
				self.__terminal.idle_task()

				numOne = pdf[0].find("Course Audience:") + len("Course Audience:")
				numTwo = pdf[0].find("Responses Received:")
				total = pdf[0][numOne:numTwo].strip()

				numOne = pdf[0].find("Responses Received:") + len("Responses Received:")
				numTwo = pdf[0].find("Response Ratio:")
				number = pdf[0][numOne:numTwo].strip()

				for line in pdf[0].split(" "):
					if line.find("-") != -1:
						className = line.split("-")[0]
						section = line.split("-")[1]

						if int(className) >= 600:
							className = str(int(className) - 200)

						individualData.append("CS" + className)
						individualData.append(section)
						break

				individualData.append(total)
				individualData.append(number)
				individualData.append(7*int(number))

				values = dict()
				ind = 1
				for index in range(0, 7):
					startPos = pdf[ind].find(self.__questions[index]) + len(self.__questions[index])
					endPos = pdf[ind].find(self.__questions[index+1])
					#print(endPos)

					string = ""
					add = False
					count = 0

					for line in pdf[ind][startPos:endPos].split("\n"):
						#print(ind)
						if line.strip().find("%") != -1:
							count += 1

						if count == 6:
							add = False

						string += line + " "

					percents = []
					per = 0

					for vals in string.split(" "):
						if vals.find("%") != -1:
							percents.append(vals)
							per += 1
						if per == 6:
							break

					values[self.__questions[index]] = percents

					if endPos == -1:
						ind += 1

				totalSum = [0, 0, 0, 0, 0, 0]

				for keys in values.keys():
					#print(keys + str(values[keys]))
					numerical = []
					for per in values[keys]:
						perc = int(float(per[:-1]))
						num = float(number) * perc / 100.
						numerical.append(float("{:.0f}".format(num)))

					if len(numerical) == 0:
						break
					#print(numerical)
					#print(sum(numerical))
					for i in range(len(numerical)):
						totalSum[i] += numerical[i]

				totalSum = [float("{:.0f}".format(sm)) for sm in totalSum]
				#print("This is the total")
				#print(totalSum)
				for vals in totalSum:
					individualData.append(vals)

				individualData.append(totalSum[0] + totalSum[1])
				#print(sum(totalSum))

				#this is the weighted average
				#Find a weighted average
				average = 0
				v = 5
				for i in totalSum:
					average += v*float(i)
					v-=1

				average /= 7*int(number)

				individualData.append("{:.2f}".format(average))

				totalData.append(individualData)

		self.writeData(totalData)

   
	def writeData(self, table):
		self.__terminal.enterLine("Writing the data into the final .csv file")
		self.__terminal.idle_task()
		df = pd.DataFrame(table, columns=self.__header)
		df = df.sort_values(by=['Class', 'Section'])

		df.to_csv(self.__saveDirectory + "/" + self.__name + ".csv")
		"""