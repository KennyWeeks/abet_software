import sys
import re
import docx2txt
import os
import pandas
import numpy as np

class ParseDirect:

	__globalPath = ""

	__count = 0

	__outputName = ""

	__saveDirectory = ""

	__terminal = None

	__totalData = dict() #this is dictionary that will hold the numerical data for each independent class

	__outFldr = None

	def __init__(self, gP, oN, sD, terminal, outFolder):
		self.__globalPath = gP + "/"
		self.__count = self.__globalPath.count("/")
		self.__outputName = oN
		self.__saveDirectory = sD
		self.__terminal = terminal
		self.__outFldr = outFolder

	def returnGp(self):
		return self.__globalPath

	def returnData(self):
		return self.__totalData

	def parseTest(self, path):
		cnPath = path.split("/")
		className = cnPath[self.__count: self.__count+1]

		section = cnPath[self.__count + 1: self.__count + 2]

		#---------------
		#get the document data
		thereAreSectionNumbers = True

		documentText = docx2txt.process(path)

		sectionTitle = documentText.find("Sections Included in Data:")

		numericalTitle = documentText.find("Numerical Data:")

		sectionNumbers = documentText[sectionTitle + len("Sections Included in Data:"): numericalTitle]

		if sectionNumbers.find("Enter the section numbers of the classes that make up this report") != -1:
			thereAreSectionNumbers = False
		else:
			sectionNumbers = sectionNumbers.split(",")

			sectionNumbers = [sN.strip() for sN in sectionNumbers]

		#---------------
		#check if the section is found
		if not thereAreSectionNumbers:
			#this means the file has not been edited
			
			if len(self.__totalData[className[0]]["accounted"]) != 0:
				if section[0] in self.__totalData[className[0]]["accounted"]:
					return
				else:
					self.__totalData[className[0]]["missing"].append(section[0])
					return
			else:
				self.__totalData[className[0]]["missing"].append(section[0])
				return

		else:
			if len(self.__totalData[className[0]]["accounted"]) == 0:
				#will add a check to see if missing isn't empty
				self.__totalData[className[0]]["accounted"] = sectionNumbers
			else:
				i = 0
				while i < len(sectionNumbers):
					val = sectionNumbers[i]
					if val in self.__totalData[className[0]]["accounted"]:
						sectionNumbers.remove(val)
					else:
						i+=1
				#tempNumbers = sectionNumbers
				"""for i in tempNumbers:
					print(i)
					if i in self.__totalData[className[0]]["accounted"]:
						print(i + "found")
						sectionNumbers.remove(i)"""

				for i in sectionNumbers:
					self.__totalData[className[0]]["accounted"].append(i)

				
			#if there are already folders that are found empty, we can see if this file accounted for their data
			if len(self.__totalData[className[0]]["missing"]) != 0:
				i = 0
				while i < len(self.__totalData[className[0]]["missing"]):
					val = self.__totalData[className[0]]["missing"][i]
					if val in self.__totalData[className[0]]["accounted"]:
						self.__totalData[className[0]]["missing"].remove(val)
					else:
						i+=1

			if len(sectionNumbers) == 0:
				return

		position = [x.start() for x in re.finditer("Outcome", documentText)]

		categoryTag = [x.start() for x in re.finditer("Category", documentText)]

		eeTag = [x.start() for x in re.finditer("Exceeds Expectations", documentText)]

		stTag = [x.start() for x in re.finditer("Satisfactory", documentText)]

		beTag = [x.start() for x in re.finditer("Below Expectations", documentText)]

		unTag = [x.start() for x in re.finditer("Unsatisfactory", documentText)]

		i = 0
		for i in range(len(position)):
			outcomeType = documentText[position[i] + len("Outcome"):categoryTag[i]].strip()
			try:
				self.__totalData[className[0]]["count"][outcomeType]
			except:
				self.__totalData[className[0]]["count"][outcomeType] = list()

			#-----------------
			eeData = documentText[eeTag[i] + len("Exceeds Expectations"): stTag[i]]
			satData = documentText[stTag[i] + len("Satisfactory"): beTag[i]]
			beData = documentText[beTag[i] + len("Below Expectations"): unTag[i]]
			unsData = None
			if i + 1 >= len(position):
				unsData = documentText[unTag[i] + len("Unsatisfactory"):]
			else:
				unsData = documentText[unTag[i] + len("Unsatisfactory"): position[i+1]]

			eeData = eeData.split("\n")
			eeNData = list()
			for data in eeData:
				if data != '':
					eeNData.append(float(data))


			satData = satData.split("\n")
			satNData = list()
			for data in satData:
				if data != '':
					satNData.append(float(data))


			beData = beData.split("\n")
			beNData = list()
			for data in beData:
				if data != '':
					beNData.append(float(data))


			unsData = unsData.split("\n")
			unsNData = list()
			for data in unsData:
				if data != '':
					unsNData.append(float(data))

			total = eeNData[0] + satNData[0] + beNData[0] + unsNData[0]

			if len(self.__totalData[className[0]]["count"][outcomeType]) == 0:
				self.__totalData[className[0]]["count"][outcomeType] = [int(total), int(eeNData[0]), int(satNData[0]), int(beNData[0]), int(unsNData[0])]
			else:
				self.__totalData[className[0]]["count"][outcomeType][0] += int(total)
				self.__totalData[className[0]]["count"][outcomeType][1] += int(eeNData[0])
				self.__totalData[className[0]]["count"][outcomeType][2] += int(satNData[0])
				self.__totalData[className[0]]["count"][outcomeType][3] += int(beNData[0])
				self.__totalData[className[0]]["count"][outcomeType][4] += int(unsNData[0])

	def startReading(self, gp):
		for f in os.listdir(gp):

			newPath = gp + f 

			if os.path.isdir(newPath):
				newPath += "/"
				if newPath.count("/") == self.__count + 1:
					self.__totalData[f] = {"accounted": list(), "missing": list(), "count": dict()}

					#0 --> sections accounted for
					#1 --> sections with missing data
					#2 --> total numerical data

				if newPath.count("/") == self.__count + 3:
					if f == self.__outFldr:
						self.__terminal.enterLine("Starting the parse data for " + newPath)
						self.__terminal.idle_task()
						self.startReading(newPath)
				else:
					self.startReading(newPath)
			else:
				if f != ".DS_Store":
					if f == "Numerical_Direct_Assessment_Data.docx":
						self.parseTest(newPath)


	def makeReport(self, data):
		header = ["Courses", "All sections", "Sections Parsed", "Outcome", "No. of Responses", "EE", "S", "BE", "U", "S+EE", "EE%", "S%", "BE%", "U%", "EE+S%"]

		finalData = list()

		parseByOutcome = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": []}

		for key in data.keys():
			self.__terminal.enterLine("Creating data to the final file for " + key)
			self.__terminal.idle_task()
			className = key
			sections = data[key]["accounted"] + data[key]["missing"]
			sections = [int(x) - 1000 for x in sections]
			accountedFor = "All" if len(sections) == len(data[key]["accounted"]) else data[key]["accounted"]

			if accountedFor != "All":
				accountedFor = [int(x) - 1000 for x in accountedFor]

			if len(data[key]["count"].keys()) != 0:
				for outcome in data[key]["count"].keys():
					dataLine = [className, sections, accountedFor, outcome, data[key]["count"][outcome][0]]

					if len(parseByOutcome[outcome]) == 0:
						parseByOutcome[outcome] = data[key]["count"][outcome]
					else:
						for val in range(0, len(data[key]["count"][outcome])):
							parseByOutcome[outcome][val] += data[key]["count"][outcome][val]

					total = data[key]["count"][outcome][0] #this is the total

					for numbers in range(1, len(data[key]["count"][outcome])):
						dataLine.append(data[key]["count"][outcome][numbers])

					dataLine.append(data[key]["count"][outcome][1] + data[key]["count"][outcome][2])

					finalData.append(dataLine)

					for numbers in range(1, len(data[key]["count"][outcome])):
						dataLine.append("{:.2f}".format(data[key]["count"][outcome][numbers] * 100 / total))

					dataLine.append("{:.2f}".format(float(dataLine[-4]) + float(dataLine[-3])))

			else:
				dataLine = [className, "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"]
				finalData.append(dataLine)

		#print(finalData)

		df = pandas.DataFrame(finalData, columns=header)
		df = df.sort_values(by='Courses')

		self.__terminal.enterLine("Writing to output file --> " + self.__outputName + ".csv")
		self.__terminal.idle_task()
		df.to_csv(self.__saveDirectory  + "/" + self.__outputName + ".csv")
		self.__terminal.enterLine("Done writing to file")
		self.__terminal.idle_task()

		outcomeDivided = list()
		for key in parseByOutcome.keys():
			self.__terminal.enterLine("Adding data to the individual outcome data for outcome --> " + key)
			self.__terminal.idle_task()
			parseByOutcome[key].append(parseByOutcome[key][1] + parseByOutcome[key][2])
			parseByOutcome[key].append(key)
			outcomeDivided.append(parseByOutcome[key])


		df = pandas.DataFrame(outcomeDivided, columns=["total", "EE", "S", "BE", "U", "EE+S", "Outcome Type"])

		self.__terminal.enterLine("Writing to output file --> outcome.csv")
		self.__terminal.idle_task()
		df.to_csv(self.__saveDirectory + "/outcome.csv")
		self.__terminal.enterLine("Done writing to file")
		self.__terminal.idle_task()

		#this is a percentage version of the parser that I made earlier
		percentageOutcome = list()
		for key in parseByOutcome.keys():
			self.__terminal.enterLine("Adding a data to the individual outcome percentage file for --> " + key)
			self.__terminal.idle_task()
			outcomeList = [key]
			total = parseByOutcome[key][0]
			outcomeList.append(100)
			for i in range(1, len(parseByOutcome[key]) - 2):
				outcomeList.append("{:.2f}".format(int(parseByOutcome[key][i]) * 100 / int(total)))


			outcomeList.append("{:.2f}".format(float(outcomeList[2]) + float(outcomeList[3])))
			percentageOutcome.append(outcomeList)

		df = pandas.DataFrame(percentageOutcome, columns=["Outcome Type", "total", "EE", "S", "BE", "U", "EE+S"])

		self.__terminal.enterLine("Writing to output file --> percentage.csv")
		self.__terminal.idle_task()
		df.to_csv(self.__saveDirectory + "/percentage.csv")
		self.__terminal.enterLine("Done writing to file")
		self.__terminal.idle_task()


