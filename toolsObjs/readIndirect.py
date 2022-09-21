import PyPDF2
import os
import pandas as pd

class ReadIndirect:

	#these are the private variables used for the class
	#-----------------------
	__terminal = None #this is the terminal of the software

	#these questions are what is searched for in the pdf software
	#this will essentially break the document into the import data, which is saved
	#into an array
	__questions = {"The material was presented clearly": [], 
"Instructor was genuinely interested in educating the students.": [], 
"The assignments, quizzes, and tests were fair and covered the material emphasized": [], 
"Instructor was well prepared in class meetings.": [], 
"Instructor was available to answer questions.": [], 
"Instructor covered the material listed in the syllabus": [], 
"Instructor's overall performance in this course was excellent.": []}

	__lastBreak = "Ranking Summary"

	__dirFolder = ""

	__saveFolder = ""

	__finalCSV = ""

	__totalValues = []

	def __init__(self, term, dirFolder, saveFolder, finalCSV):

		"""
		This is the parameters of the class
		-----------------------------------
		term --> This is the terminal
		dirFolder --> This is the directory folder that has all the indirect folders
		saveFolder --> This is the final save folder
		finalCSV --> This is the name of the csv where the final data will be saved
		"""

		self.__terminal = term

		self.__dirFolder = dirFolder

		self.__saveFolder = saveFolder

		self.__finalCSV = finalCSV

		self.startReading()

		self.writeLine()


	def startReading(self):
		for pdfs in os.listdir(self.__dirFolder):
			self.__terminal.enterLine("Reading --> " + pdfs)
			self.__terminal.idle_task()

			pdfFile = pdfFile = open(os.path.join(self.__dirFolder, pdfs), "rb")
			pdf = PyPDF2.PdfFileReader(pdfFile)

			#--------------------
			#This is will get the
			#important info
			#--------------------
			pageInfo = pdf.getPage(0).extractText()
			pageInfo = pageInfo.split("\n")
			totalStudents = pageInfo[-4]
			studentsTaken = pageInfo[-3]

			clss = ""
			section = ""
			for page in pageInfo:
				found = False
				spacePage = page.split(" ")
				for items in spacePage:
					if items.find("-") != -1:
						splt = items.split("-")
						clss = splt[0]
						if int(clss) >= 600:
							clss = str(int(clss) - 200)
						section = splt[1]
						found = True
						break

				if found:
					break

			content = pdf.getPage(1).extractText()
			keys = list(self.__questions.keys())
			for i in range(len(self.__questions.keys())):
				pos1 = content.find(keys[i])
				try:
					pos2 = content.find(keys[i + 1])
				except:
					pos2 = content.find(self.__lastBreak)

				text = content[pos1 + len(keys[i]):pos2]

				arr = text.split("\n")
				for item in arr:
					if item.find("Overall") != -1:
						self.__questions[keys[i]] = item.split(" ")
						break

				if i == 3:
					content = pdf.getPage(2).extractText()

			sumList = [0] * 6

			checkTaken = False
			for keys in self.__questions.keys():
				arr = self.__questions[keys]
				overall = float(arr[1])
				if overall != float(studentsTaken):
					checkTaken = True
					break
				newValues = list()
				for i in range(2, 8):
					val = int(float(arr[i][:-1]))
					digit = val * overall / 100.
					newValues.append(float("{:.0f}".format(digit)))
				self.__questions[keys] = newValues
				for i in range(len(newValues)):
					sumList[i] += newValues[i]

			#this makes sure the data matches
			if checkTaken:
				continue

			sumList = [float("{:.0f}".format(sm)) for sm in sumList]

			arrs = list()
			arrs.append("CS" + clss)
			arrs.append(section)
			arrs.append(totalStudents)
			arrs.append(studentsTaken)
			arrs.append(int(studentsTaken) * 7)

			for i in range(len(sumList)):
				arrs.append(sumList[i])

			arrs.append(sumList[0] + sumList[1])

			average = 0
			v = 5
			for i in sumList:
				average += v*float(i)
				v -= 1

			average /= 7 * int(overall)
			arrs.append("{:.2f}".format(average))

			self.__totalValues.append(arrs)

			#This is resetting the keys of the questions dictionary
			for keys in self.__questions.keys():
				self.__questions[keys] = []

	def writeLine(self):
		self.__terminal.enterLine("Writing the data for this file to the final csv")
		self.__terminal.idle_task()

		df = pd.DataFrame(self.__totalValues, columns=["Class", "Section", "Total", "Taken", "Total Elements", "SA", "A", "N", "D", "SD", "N/A", "SA+A", "Average"])
		df = df.sort_values(by=["Class", "Section"])

		self.__terminal.enterLine(self.__saveFolder + "/" + self.__finalCSV + ".csv")
		self.__terminal.enterLine("Done")

		df.to_csv(self.__saveFolder + "/" + self.__finalCSV + ".csv")