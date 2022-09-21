import pandas as pd
import numpy as np
import os
import csv
import sys
from statistics import median
import json

#vals = sys.argv[1].split(",")
#vals = [v.strip() for v in vals]

class ParseIndirect:
	#this will hold the final parsed and converted data
	__percentageOutcome = list()

	#this is the dictionary that will hold the filterd data by outcome type
	__individualOutcomes = {"1": [], "2": [], "3": [], "4": [], "5": [], "6":[]}

	#this will hold the destination of the result.csv file that holds the numerical data of the parsed indirect files
	__numericalDataLocation = ""

	#this will hold the save destionation
	__saveDestination = ""

	#this is the header list for the column names
	__headers = None

	__terminal = None

	__settings = None

	__outcomeClassesList = [[], [], [], [], [], []]

	def __init__(self, resultFile, saveDestination, terminal, settingsP):
		self.__numericalDataLocation = resultFile
		self.__saveDestination = saveDestination
		self.__terminal = terminal

		fl = open(os.path.join(settingsP, "settings.json"), "r")
		data = json.load(fl)

		for keys in data["Classes"].keys():
			for out in data["Classes"][keys]:
				val = int(out)
				self.__outcomeClassesList[out-1].append(keys)

		self.__settings = data

	def startReading(self):
		with open(self.__numericalDataLocation) as file:
			reader = csv.reader(file, delimiter=",")
			for line in reader:
				if line[1] == 'Class':
					self.__headers = line[1:]
					self.__headers.append("Median")
				else:
					self.__terminal.enterLine("Parsing --> " + line[1] + "/" + line[2])
					self.__terminal.idle_task()
					items = list() #this will hold the data needed for parsing
					medianData = list()
					for i in range(1, 6):
						items.append(line[i]) #this is adding the info we already have, but needs to be in this report


					medianData.append(line[1])
					medianData.append(line[2])
					resp = float(line[5]) #this is the total number of responses

					#this will generate the percentage values
					for i in range(6,12):
						items.append('{:.2f}'.format((float(line[i])*100)/resp))
						medianData.append(line[i])

					items.append('{:.2f}'.format(float(items[5])+float(items[6])))
					items.append(line[-1])

					med = self.findMedian(medianData) #this is the median value
					items.append(med)

					self.__percentageOutcome.append(items)

					#---------------
					individualLine = list()

					if line[1] in self.__outcomeClassesList[0]:
						#outcome 1
						individualLine.append(1)
						[individualLine.append(line[i]) for i in range(5, 12)]
						individualLine.append(med)
						self.__individualOutcomes["1"].append(individualLine)

					individualLine = list()

					if line[1] in self.__outcomeClassesList[1]:
						#outcome 2
						individualLine.append(2)
						[individualLine.append(line[i]) for i in range(5, 12)]
						individualLine.append(med)
						self.__individualOutcomes["2"].append(individualLine)

					individualLine = list()

					if line[1] in self.__outcomeClassesList[2]:
						#Outcome 3
						individualLine.append(3)
						[individualLine.append(line[i]) for i in range(5, 12)]
						individualLine.append(med)
						self.__individualOutcomes["3"].append(individualLine)

					individualLine = list()

					if line[1] in self.__outcomeClassesList[3]:
						#Outcome 4
						individualLine.append(4)
						[individualLine.append(line[i]) for i in range(5, 12)]
						individualLine.append(med)
						self.__individualOutcomes["4"].append(individualLine)

					individualLine = list()

					if line[1] in self.__outcomeClassesList[4]:
						#Outcome 5
						individualLine.append(5)
						[individualLine.append(line[i]) for i in range(5, 12)]
						individualLine.append(med)
						self.__individualOutcomes["5"].append(individualLine)

					individualLine = list()

					if line[1] in self.__outcomeClassesList[5]:
						individualLine.append(6)
						[individualLine.append(line[i]) for i in range(5, 12)]
						individualLine.append(med)
						self.__individualOutcomes["6"].append(individualLine)

	def createResult(self):
		print(self.__individualOutcomes)
		df = pd.DataFrame(self.__percentageOutcome, columns=self.__headers)
		df = df.sort_values(by=['Class', 'Section'])
		df.to_csv(self.__saveDestination + "/percentages.csv")

		#this will create individual files for the different outcome types
		for outcome in self.__individualOutcomes.keys():
			self.__terminal.enterLine("Creating the individual outcome file for: " + outcome)
			finalCalc = ["Total", 0, 0, 0, 0, 0, 0, 0]
			print(self.__individualOutcomes[outcome])
			for line in self.__individualOutcomes[outcome]:
				for i in range(1, 8):
					finalCalc[i] += float(line[i])

			self.__individualOutcomes[outcome].append(finalCalc)

			print(finalCalc)

			lastLine = ["Percentages", ""]
			for i in range(2, 8):
				lastLine.append('{:.2f}'.format(finalCalc[i]*100/finalCalc[1]))

			self.__individualOutcomes[outcome].append(lastLine)

			df = pd.DataFrame(self.__individualOutcomes[outcome], columns=["Outcome", "No. of Responses", "E", "G", "N", "F", "P", "N/A", "Median"])
			df.to_csv(self.__saveDestination + "/outcome" + outcome + ".csv")

	def findMedian(self, data):
		volumeData = list()
		start = 5
		for i in data[2:]:
			for j in range(int(float(i))):
				volumeData.append(start)

			#------------This is just some value tracking stuff
			start -= 1


		med = int(median(volumeData))

		if med == 5:
			return "E"
		elif med == 4:
			return "G"
		elif med == 3:
			return "N"
		elif med == 2:
			return "F"
		elif med == 1:
			return "P"
		else:
			return "N/A"

