import os
import re
import numpy as np
import pandas as pd
import json
import csv

class EmailList:

	__settings = []

	__columns = []

	__schedulePath = []

	__outputPath = []

	__CLASSES = []

	__terminal = None

	def __init__(self, col, sp, op, tm):

		fl = open("encapsulated/settings.json", "r")
		data = json.load(fl)

		for keys in data["Classes"].keys():
			self.__CLASSES.append(keys[2:])

		self.__settings = data

		self.__columns = col

		self.__schedulePath = sp

		self.__outputPath = op

		self.__terminal = tm

		self.__terminal.enterLine("Starting tool ...")
		self.__terminal.idle_task()

	def createFile(self):
		self.__terminal.enterLine("Opening schedule file ...")
		self.__terminal.idle_task()
		classRoster = pd.read_excel(self.__schedulePath)
		columns = list(classRoster.columns)
		classRoster = classRoster.to_numpy()

		indexOfColumnsPicked = [] #this is a list of the indexes of the columns that are picked by the user 

		self.__terminal.enterLine("Finding the index of the user selected headers ...")
		self.__terminal.idle_task()

		for col in self.__columns:
			for cols in columns:
				if col == cols:
					indexOfColumnsPicked.append(columns.index(col))
					break

		finalSetOfClasses = list()

		professorsDict = dict()

		self.__terminal.enterLine("Adding classes based on'settings' list ...")
		self.__terminal.idle_task()

		for clss in classRoster:
			for c in self.__CLASSES:
				for index in indexOfColumnsPicked:
					if str(clss[index]).strip() == c:
						finalVals = []
						for ind in indexOfColumnsPicked:
							finalVals.append(str(clss[ind]).strip())
						professorsDict[str(clss[indexOfColumnsPicked[-1]])] = []
						finalSetOfClasses.append(finalVals)
						break

		self.__terminal.enterLine("Creating professor association dictionary ...")
		self.__terminal.idle_task()

		for profs in professorsDict.keys():
			for clss in finalSetOfClasses:
				if clss[-1] == profs:
					professorsDict[profs].append("CS" + clss[0] + "/" + clss[1])

		professorsDict["No Professor Available"] = professorsDict['nan']
		del professorsDict['nan']

		#------------------------
		#This will write to the file
		headers = ["Professor Name", "Email", "Classes"]

		self.__terminal.enterLine("Writing output csv file ...")
		self.__terminal.idle_task()

		with open(self.__outputPath + "/emailfile.csv", "w") as csvfile:
			writer = csv.writer(csvfile)

			writer.writerow(headers)
			for profs in professorsDict:
				row = [profs, "", professorsDict[profs]]
				writer.writerow(row)

		self.__terminal.enterLine("Done, please add the emails to the list to use the emailing feature in the audit tool.")
		self.__terminal.idle_task()






