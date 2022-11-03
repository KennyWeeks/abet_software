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

	__settings = None

	__columnAssociation = None

	def addCabinetStructure(self, path):
		#This will begin building the subfolders for the class/section folder combos
		for fldrs in self.__settings["Subfolders"].keys():

			#this is put in a try catch block to ensure no duplicates are found
			try:
				os.mkdir(path + "/" + fldrs)
			except:
				#warn the user that there is a duplicate at this path
				self.__terminal.enterLine("There is a repeat of this class and section --> " + path)
				self.__terminal.idle_task();
				break

			#If there are subfolders for the given folder [Assignments --> Labs, Projects, etc.]
			#build them here
			for sbfldrs in self.__settings["Subfolders"][fldrs]:
				os.mkdir(path + "/" + fldrs + "/" + sbfldrs)

	def __init__(self, terminal, args, cv, settingsP):
		#this is a reference to the terminal used in the software
		self.__terminal = terminal

		self.__terminal.enterLine("Starting the tool ....")
		self.__terminal.idle_task()

		#start assigning the variables here, from the args parameter
		self.__classFile = args[0]

		#This is the user name folder
		self.__folderName = args[1]

		#this is the save destination of the folder
		self.__saveDest = args[2]

		#these are the columns that will be used for the tool
		self.__columnAssociation = cv

		#open up the settings, and get the info needed to get this thing running
		fl = open(os.path.join(settingsP, "settings.json"), "r")
		data = json.load(fl)

		#return the classes that will be used to build the final cabinet system.
		for keys in data["Classes"].keys():
			print(keys)
			self.__CLASSES.append(keys[2:])

		self.__settings = data

	def createCabinet(self):
		self.__terminal.enterLine("Opening the provided file ...")
		self.__terminal.idle_task()

		#This will open and read the content of any of the files provided.
		fileExtension = os.path.splitext(self.__classFile)
		if fileExtension[1] == ".xlsx":
			rosterArr = pd.read_excel(self.__classFile)
		else:
			rosterArr= pd.read_csv(self.__classFile)

		#get the index of the columns selected by the user
		indexes = list() #these are the index of the column selected by the user
		columns = list(rosterArr.columns)
		for col in rosterArr.columns:
			for keys in self.__columnAssociation.keys():
				if col == self.__columnAssociation[keys][0]:
					
					self.__columnAssociation[keys].append(columns.index(col))

		#start building the cabinet here
		self.__terminal.enterLine("Parsing file for data associated with headers selected ...")
		self.__terminal.idle_task()
		rosterArr = rosterArr.to_numpy()

		cabinetFolders = list()

		#for the items in the classes variable
		for c in self.__CLASSES:

			#and for the columns in the roster
			for clss in rosterArr:

				item = list()
				if c == str(clss[self.__columnAssociation["Class #"][-1]]).strip():
					item.append(clss[self.__columnAssociation["Class #"][-1]])
					item.append(clss[self.__columnAssociation["Section #"][-1]])

					cabinetFolders.append(item)

		
		self.__terminal.enterLine("Making the home directory ...")
		self.__terminal.idle_task()
		#This try/catch block will try and build the home directory, or it will throw and error if an home directory can't be built
		try:
			os.mkdir(self.__saveDest + "/" + self.__folderName + "/")
		except:
			#If the file exists, then you can throw this error message, adn you no longer need to continue building the cabinet
			self.__terminal.enterLine("This folder name: " + self.__folderName + ", already exists in this location: " + self.__saveDest)
			self.__terminal.idle_task()
			return

		#If the folder can be built, then you can start building the child folders
		self.__terminal.enterLine("Making the children folders ...")
		self.__terminal.idle_task()


		for cf in cabinetFolders:
			#save the home destination, this needs to be here to reset after every class has been found
			home = self.__saveDest + "/" + self.__folderName + "/"

			#this is for the class folder, and it will be appended to the start of each class folder name
			folder = "cs" 

			#build the folders and the individual section folders here
			for item in cf:
				folder += str(item).strip() #add the class name, and then a second pass will add the section
				try:
					os.mkdir(home + folder) #if the folder exists, don't worry about it
				except:
					pass
				folder += "/" #add the final backslash

			#add this to the total directory
			home += folder 

			self.__terminal.enterLine("Working on " + folder)
			self.__terminal.idle_task()

			#start actually adding the content of each section folder 
			#[Syllabus, Exam, Homework, Handouts, Outcomes]
			self.addCabinetStructure(home)
			self.__terminal.enterLine("++++++++++++++++++++++")
			self.__terminal.idle_task()

		self.__terminal.enterLine("Finished")


