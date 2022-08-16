import re
import pandas as pd
import numpy as np

class ExitInt:

	__terminal = None

	__dataFile = None

	__headers = None

	__saveDest = None

	__fileName = None

	def __init__(self, terminal, args):
		self.__terminal = terminal

		self.__terminal.enterLine("Starting tool ...")

		self.__dataFile = args[0]

		self.__headers = args[1]

		self.__fileName = args[2]

		self.__saveDest = args[3]

	def startParsingData(self):
		self.__terminal.enterLine("Opening the provided file ...")
		exitData = pd.read_excel(self.__dataFile)

		outcome = list()

		indexes = list()

		for hvals in self.__headers:
			outcome.append([0,0,0,0])
			c = 0
			for col in exitData.columns:
				if col == hvals:
					indexes.append(c)
					break

				c+=1

		self.__terminal.enterLine("Parsing file for data associated with headers selected ...")
		exitData = exitData.to_numpy()

		valuesNeeded = list()

		empty = [float('nan')] * len(exitData[0])

		for line in exitData:
			if str(line[1]) != 'nan':
				savedVals = list()
				for i in indexes:
					savedVals.append(line[i])

				valuesNeeded.append(savedVals)


		self.__terminal.enterLine("Start making data distribution ...")
		for data in valuesNeeded[21:40]:
			for i in range(0, len(self.__headers)):
				val = data[i]
				if str(val) == "very well":
					outcome[i][0] += 1
				elif str(val) == "pretty well":
					outcome[i][1] += 1
				elif str(val) == "somewhat":
					outcome[i][2] += 1
				elif str(val) == 'nan' or str(val) == 'not at all':
					outcome[i][3] += 1

		self.__terminal.enterLine("Saving parsed data now ...")

		df = pd.DataFrame(outcome, ["SLO 1", "SLO 2", "SLO 3", "SLO 4", "SLO 5", "SLO 6"], ["Very Well", "Pretty Well", "Somewhat", "N/A"])
		df.to_csv(self.__saveDest + "/" + self.__fileName + ".csv")



