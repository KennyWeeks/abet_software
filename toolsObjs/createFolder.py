import numpy as np
import pandas as pd
import os
import sys
import time
import json

class CreateFolder:

	#these will be some of the variables that will interface with the gui
	__terminal = None

	__CLASSES = []

	#these variables will be be to create the folder
	__saveDest = None

	__folderName = None

	__classFile = None

	__headers = None

	__settings = None

	def addCabinetStructure(self, path):
		for fldrs in self.__settings["Subfolders"].keys():
			os.mkdir(path + "/" + fldrs)
			for sbfldrs in self.__settings["Subfolders"][fldrs]:
				os.mkdir(path + "/" + fldrs + "/" + sbfldrs)

	def __init__(self, terminal, args, settingsP):
		self.__terminal = terminal

		self.__terminal.enterLine("Starting the tool ....")

		#start assigning the variables here, from the args parameter
		self.__classFile = args[0]

		self.__headers = args[1]

		self.__folderName = args[2]

		self.__saveDest = args[3]

		#open up the settings, and get the info needed to get this thing running
		fl = open(os.path.join(settingsP, "settings.json"), "r")
		data = json.load(fl)

		for keys in data["Classes"].keys():
			print(keys)
			self.__CLASSES.append(keys[2:])

		self.__settings = data

	def createCabinet(self):
		self.__terminal.enterLine("Opening the provided file ...")
		rosterArr = pd.read_excel(self.__classFile)

		#get the index of the columns selected by the user
		indexes = list() #these are the index of the column selected by the user
		for ind in self.__headers:
			c = 0
			for col in rosterArr.columns:
				if col == ind:
					indexes.append(c)
					break

				c+= 1

		#start building the cabinet here
		self.__terminal.enterLine("Parsing file for data associated with headers selected ...")
		rosterArr = rosterArr.to_numpy()

		cabinetFolders = list()

		#for the items in the classses variable
		for c in self.__CLASSES:

			#and for the columns in the roster
			for clss in rosterArr:

				#and for the user chosen index to get this thing running
				for i in indexes:
					item = list()
					#see if the classes defined match any of the classes in the file
					if c == str(clss[i]).strip():
						for j in indexes:
							item.append(clss[j]) #save all the data associated with the indexes chosen
						cabinetFolders.append(item) #save this for later
						break
		
		self.__terminal.enterLine("Making the home directory ...")
		try:
			os.mkdir(self.__saveDest + "/" + self.__folderName + "/")
		except:
			self.__terminal.enterLine("This folder name: " + self.__folderName + ", already exists in this location: " + self.__saveDest)
			return

		self.__terminal.enterLine("Making the children folders ...")
		for cf in cabinetFolders:
			home = self.__saveDest + "/" + self.__folderName + "/"

			folder = "cs" #this is for the class folder

			#build the folders and the individual section folders here
			for item in cf:
				folder += str(item).strip()
				try:
					os.mkdir(home + folder)
				except:
					pass
				folder += "/"

			home += folder

			self.__terminal.enterLine("Working on " + folder)
			self.addCabinetStructure(home)
			self.__terminal.enterLine("++++++++++++++++++++++")

		self.__terminal.enterLine("Finnished")


