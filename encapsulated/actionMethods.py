import json
from tkinter import *
from toolsObjs.emailList import EmailList

class ActionMethods:

	__terminal = None #this is this methods copy of the terminal. It's the same terminal, just a copy

	def setTerminal(self, terminal):
		self.__terminal = terminal

	def terminalDestroy(self):
		self.__terminal.destroy()

	#This will add data to the json file that holds the settings
	def addToEnv(self, data, e1, e2, cv, parent, name, frame):

		fl = open("encapsulated/settings.json", "r")
		data = json.load(fl)

		if e2 != None:
			#this is if we are chaning the outcome assessment
			#-----------------------------------------------
			line = [] #this is the line of data

			#if there is a nonempty second entry box, we can see if there are more than
			#one outcome for the class
			for vals in e2.get().strip().split(","):
				val = None #this is an individual outcome value
				try:
					val = int(vals.strip()) #we see if it's an int
				except:
					#if it's not an integer, then we warn the user, and break from this call
					self.__terminal.enterLine("Outcome Value provided is not an integer.")
					break

				line.append(val) #append to the line variable above


			data["Classes"][e1.get().strip()] = line #add to the settings.json file

		else:
			#if we are just concerned with adding subfolders, then we don't have 
			#a second entrybox, we'll just add the data to the subfolder as is
			data["Subfolders"].append(e1.get().strip())

		rowNumber = frame.grid_size()[1]
		rowNumber -= 2

		sfLabel = Label(frame, bg="#323232", fg="#ffffff", text="+ " + e1.get().strip() + " --> ", name="label" + e1.get().strip())
		sfLabel.grid(sticky=W, row=rowNumber, column=1, padx=10, pady=5)

		opButton = Button(frame, text="del", name="but"+e1.get().strip(), command=lambda name=e1.get().strip(): self.removeFromEnv(name, frame, cv, parent, "Subfolders"))
		opButton.grid(sticky=W, row=rowNumber, column=2, pady=5, padx=10)

		rowNumber += 1

		#this will start moving stuff down, but we need to remove the objects that are already there
		for c in frame.winfo_children():
			if str(type(c)) == "<class 'tkinter.Label'>":
				if str(c).find("dividingLine") != -1:
					c.grid_forget()
			elif str(type(c)) == "<class 'tkinter.Button'>":
				if str(c).find(name) != -1:
					c.grid_forget()
			elif str(type(c)) == "<class 'tkinter.Entry'>":
				if str(c).find(name) != -1:
					c.grid_forget()

		#add the dividing lines again
		dividingLabel = Label(frame, text="----------", bg="#323232", fg="#ffffff", name="dividingLine1")
		dividingLabel.grid(sticky=W, row=rowNumber, column=1, padx=10)

		dividingLabel = Label(frame, text="---------", bg="#323232", fg="#ffffff", name="dividingLine2")
		dividingLabel.grid(sticky=W, row=rowNumber, column=2, padx=10)

		rowNumber += 1

		#add back the entry box and the add button so this thing starts working again
		entryBoxFolder = Entry(frame, bg="#ffffff", fg="#bebebe", width=10, highlightthickness=0, relief=FLAT, name="addButtonSubEntry")
		entryBoxFolder.insert(0, "Class Name")
		entryBoxFolder.grid(sticky=W, row=rowNumber, column=1, padx=10, pady=5)
		entryBoxFolder.config(insertbackground="#000000")

		addButton = Button(frame, text="add", name="addButtonSub", command=lambda: self.addToEnv(data, entryBoxFolder, None, cv, parent, "addButtonSub", frame))
		addButton.grid(sticky=W, row=rowNumber, column=2, pady=5, padx=10)

		#update the size of the canvas and body frame, so the scrollbar fits
		cv.update_idletasks()
		cv.configure(scrollregion=parent.bbox("all"))

		#actually sve the data that has been added
		jsonObj = json.dumps(data, indent=4)

		with open("encapsulated/settings.json", "w") as file:
			file.write(jsonObj)

	def removeFromEnv(self, name, frame, cv, parent, envKey):

		#open the data file again
		fl = open("encapsulated/settings.json", "r")
		data = json.load(fl)

		#Start removing the labels and button associated with what is being removed
		for c in frame.winfo_children():
			if str(type(c)) == "<class 'tkinter.Label'>":
				if str(c).find(name) != -1:
					c.grid_forget()
			elif str(type(c)) == "<class 'tkinter.Button'>":
				if str(c).find(name) != -1:
					c.grid_forget()

		#del data[envKey][name]

		if str(type(data[envKey])) == "<class 'list'>":
			data[envKey].remove(name) #remove from subfolders
		else:
			del data[envKey][name] #remove from class dictionary

		print(data[envKey])

		#save the data
		jsonObj = json.dumps(data, indent=4)

		with open("encapsulated/settings.json", "w") as file:
			file.write(jsonObj)

		#update the way the page looks
		cv.update_idletasks()
		cv.configure(scrollregion=parent.bbox("all"))
	
	#1) EMAIL LIST
	#this one is specific to the "Email List" tag, this will start the tool
	def emailList(self, filenames, checkBoxes, directory):
		startTool = True #this will be used to determine whether to start the tool or not, it is a unique bool for each frame
		args = [] #these are the arguments pushed to the tool

		if len(filenames.keys()) == 1:
			if filenames["0"] == "":
				self.__terminal.enterLine("Please provide a class schedule file.")
				startTool = False
			else:
				args.append(filenames["0"])

				#this will append what was selected in the checkboxes
				allZero = True
				checkB = list()
				for keys in checkBoxes["scheduleFileName"].keys():
					if checkBoxes["scheduleFileName"][keys].get() != 0:
						checkB.append(keys)
						allZero = False

				if allZero:
					self.__terminal.enterLine("Please select the correct number of columns in the order listed.")
					startTool = False
				else:
					if len(checkB) != 3:
						self.__terminal.enterLine("Please select the correct number of columns in the order listed.")
						startTool = False
					else:
						args.append(checkB)
		else:
			self.__terminal.enterLine("Please provide a class schedule file.")
			startTool = False

		if len(directory.keys()) != 0:
			if directory["0"] == "":
				self.__terminal.enterLine("Please provide a save directory.")
				startTool = False
			else:
				args.append(directory["0"])
		else:
			self.__terminal.enterLine("You need to provide a save directory to start the tool.")
			startTool = False

		#start the tool if possible
		if startTool:
			print(args)
			el = EmailList(args[1], args[0], args[2], self.__terminal)
			el.createFile()


		self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++++")


