import json
from tkinter import *
from toolsObjs.emailList import EmailList
from toolsObjs.auditFolder import AuditFolder
from toolsObjs.createFolder import CreateFolder
from toolsObjs.readIndirect import ReadIndirect
from toolsObjs.parseIndirect import ParseIndirect
import os

class ActionMethods:

	"""
	-----------------
	This is just to remove the clutter from the bodyframes class,
	these are essentially all the event driven methods that are triggered
	by button presses.
	-----------------
	"""

	__terminal = None #this is this methods copy of the terminal. It's the same terminal, just a copy

	__radio = 1

	def setTerminal(self, terminal):
		#save an instance of the current terminal in use
		self.__terminal = terminal

	def terminalDestroy(self):
		#destroy the instance of the current terminal
		self.__terminal.destroy()

	def retRadio(self):
		return self.__radio

	def changeRadio(self, val):
		self.__radio = val

	def finalObjectsAddEnv(self, frame, row, cv, parent, name, obj, path, prt):

		dividingLabel = Label(frame, text="--------------", bg="#323232", fg="#ffffff", width=11)
		dividingLabel.grid(sticky=W, row=row, column=0)

		dividingLabel = Label(frame, text="--------------", bg="#323232", fg="#ffffff", width=11)
		dividingLabel.grid(sticky=W, row=row, column=1)

		dividingLabel = Label(frame, text="--------------", bg="#323232", fg="#ffffff", width=11)
		dividingLabel.grid(sticky=W, row=row, column=2)

		row += 1

		#this will add back the entry boxes

		entryBlock = Entry(frame, bg="#ffffff", fg="#bebebe", width=9, highlightthickness=0, relief=FLAT)
		if prt == "Subfolders":
			entryBlock.insert(0, "Class Fldr")
		else:
			entryBlock.insert(0, "Class Name")
		entryBlock.grid(sticky=W, row=row, column=0, pady=(2, 6), padx=(10, 0))
		entryBlock.config(insertbackground="#000000")

		entryBlock.bind("<Button-1>", lambda event, e=entryBlock: self.entryClick(event, e))

		entryBoxOutcome = Entry(frame, bg="#ffffff", fg="#bebebe", width=10, highlightthickness=0, relief=FLAT)
		if prt == "Subfolders":
			entryBoxOutcome.insert(0, "Subfolder")
		else:
			entryBoxOutcome.insert(0, "Outcome")
		entryBoxOutcome.grid(sticky=W, row=row, column=1, pady=(2, 6), padx=(5, 0))
		entryBoxOutcome.config(insertbackground="#000000")

		entryBoxOutcome.bind("<Button-1>", lambda event, e=entryBoxOutcome: self.entryClick(event, e))

		addButton = Button(frame, text="add", command=lambda: self.addToEnv(path, entryBlock, entryBoxOutcome, cv, parent, name, frame, obj), width=6)
		addButton.grid(sticky=W, row=row, column=2, pady=(0, 6), padx=(6, 0))

		#add the data back to the settings.json file

		cv.update_idletasks()
		cv.configure(scrollregion=parent.bbox("all"))

	#This will add data to the json file that holds the settings
	def addToEnv(self, path, e1, e2, cv, parent, name, frame, obj):

		fl = open(os.path.join(path, "settings.json"), "r")
		data = json.load(fl)

		if obj == "Classes":
			
			flag = True

			#1. This will test to see if the first entry box is filled or not
			if len(e1.get().strip()) == 0 or e1.get().strip() == "Class Name":
				flag = False

			#2. this will see if the outcomes are correct, meaning, are they whole numbers
			outcomes = []
			if len(e2.get().strip()) > 1:
				for outcome in e2.get().split(","):
					outcome = outcome.strip()
					try:
						int(outcome)
					except:
						self.__terminal.enterLine("Please make sure the outcomes are whole numbers")
						flag = False
						break

					if flag and (int(outcome) >= 1 and int(outcome) <= 6):
						outcomes.append(int(outcome))
					else:
						self.__terminal.enterLine("Please choose an outcome in the range of 1 - 6")
						flag = False
			else:
				try:
					int(e2.get().strip())
				except:
					self.__terminal.enterLine("Please make sure the outcome is a whole numbers")
					flag = False

				if flag and (int(e2.get().strip()) >= 1 and int(e2.get().strip()) <= 6):
					outcomes.append(int(e2.get().strip()))
				else:
					self.__terminal.enterLine("Please choose an outcome in the range of 1 - 6")
					flag = False
			
			#3. this will add the content to the page
			if flag:
				rowNumber = frame.grid_size()[1]
				rowNumber -= 2

				frame.grid_slaves(rowNumber, 0)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 1)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 2)[-1].grid_remove()

				columnZeroLabel = Label(frame, bg="#323232", fg="#ffffff", text="+ " + e1.get().strip() + " --> ", name="label" + e1.get().strip(), width=11)
				columnZeroLabel.grid(sticky=W, row=rowNumber, column=0, pady=(2,2))
				
				columnOneLabel = Label(frame, bg="#323232", fg="#ffffff", text=e2.get().strip(), name="out" + e1.get().strip(), width=11)
				columnOneLabel.grid(sticky=W, row=rowNumber, column=1, pady=(2,2))

				opButton = Button(frame, text="delete", name="but"+e1.get().strip(), command=lambda name=e1.get().strip(): self.removeFromEnv(e1.get().strip(), frame, cv, parent, "Classes", path, ""), width=7)
				opButton.grid(sticky=W, row=rowNumber, column=2, pady=(2, 2))

				rowNumber += 1

				frame.grid_slaves(rowNumber, 0)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 1)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 2)[-1].grid_remove()

				#added everything to the json file
				data["Classes"][e1.get().strip()] =  outcomes

				jsonObj = json.dumps(data, indent=4)

				with open(os.path.join(path, "settings.json"), "w") as file:
					file.write(jsonObj)

				#call the final elements to be added
				self.finalObjectsAddEnv(frame, rowNumber, cv, parent, name, obj, path, obj)
		elif obj == "Subfolders":
			flag = True
			subfolder = True

			#1. This will test to see if the first entry box is filled or not
			if len(e1.get().strip()) == 0 or e1.get().strip() == "Class Fldr":
				flag = False

			if len(e2.get().strip()) == 0 or e2.get().strip() == "Subfolder":
				subfolder = False

			if flag:
				alreadyExists = False
				for c in frame.winfo_children():
					if str(type(c)) == "<class 'tkinter.Label'>":
						if str(c).find(e1.get().strip()) != -1:
							alreadyExists = True
							c.grid_forget()
					elif str(type(c)) == "<class 'tkinter.Button'>":
						if str(c).find(e1.get().strip()) != -1:
							c.grid_forget()

				children = data["Subfolders"][e1.get().strip()] if alreadyExists else []
				for ch in children:
					for c in frame.winfo_children():
						if str(type(c)) == "<class 'tkinter.Label'>":
							if str(c).find(ch) != -1:
								c.grid_forget()
						elif str(type(c)) == "<class 'tkinter.Button'>":
							if str(c).find(ch) != -1:
								c.grid_forget()

				rowNumber = frame.grid_size()[1]
				rowNumber -= 2

				frame.grid_slaves(rowNumber, 0)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 1)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 2)[-1].grid_remove()

				columnZeroLabel = Label(frame, bg="#323232", fg="#ffffff", text=e1.get().strip(), name="label" + e1.get().strip(), width=11)
				columnZeroLabel.grid(sticky=W, row=rowNumber, column=0, pady=(2,2))

				opButton = Button(frame, text="delete", name="but"+e1.get().strip(), command=lambda name=e1.get().strip(): self.removeFromEnv(e1.get().strip(), frame, cv, parent, "Subfolders", path, ""), width=7)
				opButton.grid(sticky=W, row=rowNumber, column=2, pady=(2, 2))

				rowNumber += 1

				frame.grid_slaves(rowNumber, 0)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 1)[-1].grid_remove()
				frame.grid_slaves(rowNumber, 2)[-1].grid_remove()

				if alreadyExists:
					children = data["Subfolders"][e1.get().strip()]

					for ch in children:
						columnOneLabel = Label(frame, bg="#323232", fg="#ffffff", text=ch, name="label" + ch, width=11)
						columnOneLabel.grid(sticky=W, row=rowNumber, column=1, pady=(2,2))

						opButton = Button(frame, text="delete", name="but"+ch, command=lambda name=ch: self.removeFromEnv(name, frame, cv, parent, "Subfolders", path, e1.get().strip()), width=7)
						opButton.grid(sticky=W, row=rowNumber, column=2, pady=(2, 2))
						rowNumber += 1

				if subfolder:	
					columnOneLabel = Label(frame, bg="#323232", fg="#ffffff", text=e2.get().strip(), name="label" + e2.get().strip(), width=11)
					columnOneLabel.grid(sticky=W, row=rowNumber, column=1, pady=(2,2))

					opButton = Button(frame, text="delete", name="but"+e2.get().strip(), command=lambda name=e2.get().strip(): self.removeFromEnv(name, frame, cv, parent, "Subfolders", path, e1.get().strip()), width=7)
					opButton.grid(sticky=W, row=rowNumber, column=2, pady=(2, 2))

					rowNumber += 1

				try:
					data["Subfolders"][e1.get().strip()].append(e2.get().strip())
				except:
					data["Subfolders"][e1.get().strip()] = [e2.get().strip()]

				jsonObj = json.dumps(data, indent=4)

				with open(os.path.join(path, "settings.json"), "w") as file:
					file.write(jsonObj)

				self.finalObjectsAddEnv(frame, rowNumber, cv, parent, name, obj, path, obj)

	def removeFromEnv(self, name, frame, cv, parent, envKey, path, ptName):
		#open the data file again
		fl = open(os.path.join(path, "settings.json"), "r")
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

		if envKey == "Subfolders":
			if ptName != "":
				data[envKey][ptName].remove(name)
			else:
				children = data[envKey][name]
				for ch in children:
					for c in frame.winfo_children():
						if str(type(c)) == "<class 'tkinter.Label'>":
							if str(c).find(ch) != -1:
								c.grid_forget()
						elif str(type(c)) == "<class 'tkinter.Button'>":
							if str(c).find(ch) != -1:
								c.grid_forget()
				del data[envKey][name]
		else:
			del data[envKey][name]

		#save the data
		jsonObj = json.dumps(data, indent=4)

		with open(os.path.join(path, "settings.json"), "w") as file:
			file.write(jsonObj)

		#update the way the page looks
		cv.update_idletasks()
		cv.configure(scrollregion=parent.bbox("all"))
	
	#1) EMAIL LIST
	#this one is specific to the "Email List" tag, this will start the tool
	def emailList(self, filenames, checkBoxes, directory, dropDown, settingsP):
		"""
		Parameter Definition
		+ filenames --> this is the dictionary that holds the files used
		+ checkBoxes --> these are the headers of the columns that are used by the tool
		+ directory --> this is the dictionary that holds the directories used
		+ dropDown --> these are the dropdown values that define what columns are used by the tools
		+ settingsP --> this is the path string that holds the settings file
		"""

		#----------------------------------------
		#First Step

		startTool = True #this flag will symbolize whether to start the tool or not
		args = list() #these are the arguments pushed to the class when the tool is initialized

		#This will check to see the filenames provided to get the tool running
		if len(filenames.keys()) == 1:

			#1) This will see if the schedule file is provided
			if filenames["0"] == "":
				self.__terminal.enterLine("Please provide a class schedule file.")
				startTool = False
			else:
				#save this value
				args.append(filenames["0"])

				#if the file is provided, we have to see what 
				#checkboxes were picked by the user
				#We can look at the checkboxes selected here
				allZero = True
				checkB = list()
				for keys in checkBoxes["scheduleFileName"].keys():

					#iterate through all the checkboxes to see the set values
					if checkBoxes["scheduleFileName"][keys].get() != 0:
						checkB.append(keys)
						allZero = False

				if allZero:
					#if all the checkboxes are no selected, throw an error
					self.__terminal.enterLine("Please select at least one column to use from the provided file to start the tool")
					startTool = False
				else:
					#args.append(checkB)
					if len(checkB) < 4:
						#we need to have at least two checkboxes picked to start the tool, 
						#otherwise, this error is throw
						self.__terminal.enterLine("Please select the correct number of columns in the order listed.")
						startTool = False
					else:
						args.append(checkB)
		else:
			#this will be triggered when the filename 
			self.__terminal.enterLine("Please provide a class schedule file.")
			startTool = False

		#----------------------------------------
		#Second Step

		#check to see if save directory is provided
		if len(directory.keys()) != 0:

			#1) check if value of the save directory
			if directory["0"] == "":
				self.__terminal.enterLine("Please provide a save directory.")
				startTool = False
			else:
				args.append(directory["0"])
		else:
			#this is triggered if the save directory isn't provided
			self.__terminal.enterLine("You need to provide a save directory to start the tool.")
			startTool = False

		#----------------------------------------
		#Third Step

		#this will see the columns chosen by the user
		columnDict = {"Professor": [], "Email": [], "Class #": [], "Section #": []}

		ind = 0
		for key in columnDict.keys():
			if key == "Professor" or key == "Class #" or key == "Section #":
				if dropDown[ind].get() == "----":
					self.__terminal.enterLine("Make sure a columne is chosen for at least the Professors, Class #, and Section #")
					startTool = False
					break
			columnDict[key].append(dropDown[ind].get())
			ind += 1

		#----------------------------------------
		#Final Step, start tool

		#start the tool if possible
		if startTool:
			print(args)
			el = EmailList(args[1], args[0], args[2], self.__terminal, columnDict, settingsP)
			el.createFile()


		self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++++")

	#2) CREATE ABET CABINET
	#this tool will trigger the "Create ABET Cabinet" folder
	def createFolder(self, e, filenames, checkBoxes, directory, dropDown, settingsPath):
		"""
		Parameter Definition
		+ e --> this is the entrybox associated with the tool
		+ filenames --> this is the dictionary that holds the files used
		+ checkBoxes --> these are the headers of the columns that are used by the tool
		+ directory --> this is the dictionary that holds the directories used
		+ dropDown --> these are the dropdown values that define what columns are used by the tools
		+ settingsPath --> this is the path string that holds the settings file
		"""

		startTool = True #this flag will symbolize whether to start the tool or not
		args = list() #these are the arguments pushed to the class when the tool is initialized

		#----------------------------------------
		#First Step

		#A schedule file needs to be provided to start the tool
		if len(filenames.keys()) != 0:

			#1) Check if the file is provided
			if filenames["0"] == "":
				self.__terminal.enterLine("Please provide a class schedule file.")
				startTool = False
			else:
				args.append(filenames["0"])

				#if the file is provided, we have to see what 
				#checkboxes were picked by the user
				#We can look at the checkboxes selected here
				allZero = True
				checkB = list()
				for keys in checkBoxes["scheduleFileName"].keys():
					
					#iterate through all the checkboxes to see the set values
					if checkBoxes["scheduleFileName"][keys].get() != 0:
						checkB.append(keys)
						allZero = False
				
				if allZero:
					#if all the checkboxes are no selected, throw an error
					self.__terminal.enterLine("Please select at least one column to use from the provided file to start the tool")
					startTool = False
				else:
					#args.append(checkB)
					if len(checkB) < 2:
						print(checkB)
						#we need to have at least two checkboxes picked to start the tool, 
						#otherwise, this error is throw
						self.__terminal.enterLine("Please select the correct number of columns in the order listed.")
						startTool = False
					else:
						args.append(checkB)

		else:
			#this is thrown if no file is picked
			self.__terminal.enterLine("You need to provide a schedule file to start the tool.")
			startTool = False

		#----------------------------------------
		#Second Step

		#See what the final folder will be named
		if e.get().strip() == "Enter a folder name here" or e.get().strip() == "":
			self.__terminal.enterLine("Enter a folder name to start using the tool.")
			startTool = False
		else:
			args.append(e.get().strip())

		#----------------------------------------
		#Third Step

		#this directory will be where the final roster is saved
		if len(directory.keys()) != 0:

			#1) Check the first key
			if directory["0"] == "":
				self.__terminal.enterLine("Please provide a save directory.")
				startTool = False
			else:
				args.append(directory["0"])
		else:
			self.__terminal.enterLine("You need to provide a save directory to start the tool.")
			startTool = False

		#----------------------------------------
		#Fourth Step

		#See what columns were picked by the user
		columnDict = {"Class #": [], "Section #": []}

		ind = 0
		for key in columnDict.keys():
			if dropDown[ind].get() == "----":
				self.__terminal.enterLine("Make sure a column is chosen for both Class #, and Section #")
				startTool = False
				break
			columnDict[key].append(dropDown[ind].get())
			ind += 1

		#----------------------------------------
		#Final Step, start tool

		if startTool:
			#start the tool
			inst = CreateFolder(self.__terminal, args, columnDict, settingsPath)
			inst.createCabinet()
		else:
			self.__terminal.enterLine("This tool will not start")

		self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")

	#4) AUDIT FOLDER
	#this tool will trigger the "Audit folder" tool
	def auditFolder(self, direct, email, entry, ce, se, ea, emind, addy, pss, content, settingsP):
		startTool = True #this is a flag to start the tool
		args = [] #this is the arguments that are passed to the tool

		if emind.get() == 1:
			if len(email.keys()) == 1:
				if email["0"] == "":
					self.__terminal.enterLine("Enter the email list file created earlier.")
					self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")
					return
				else:
					args.append(email["0"])
			else:
				self.__terminal.enterLine("Enter the email list file created earlier.")
				self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")
				return 

			emailStuff = [addy.get(), pss.get(), content.get("1.0", END)]
			audit = AuditFolder(None, None, None, None, None, None, None, self.__terminal, args[0], emind.get(), emailStuff, settingsP)
			self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")
			return

		#this will check to see if the two directories have been chosen
		if len(direct.keys()) == 2:
			if direct["0"] == "":
				self.__terminal.enterLine("Missing the path to the directory with the assessment.")
				startTool = False
			else:
				args.append(direct["0"])

			if direct["1"] == "":
				self.__terminal.enterLine("Missing the path to the directory for the final saved audit.")
				startTool = False
			else:
				args.append(direct["1"])
		else:
			self.__terminal.enterLine("Please include both directories for this tool to work")

		#This will get the text written in the entry block
		if entry.get().strip() == "Enter a folder name here" or entry.get().strip() == "":
			self.__terminal.enterLine("Please enter the name of the final save file.")
			startTool = False
		else:
			args.append(entry.get().strip())

		#parse through which check marks have been made
		if ce.get() == 1:
			args.append("True")
		else:
			args.append("False")

		if se.get() == 1:
			args.append("True")
		else:
			args.append("False")

		if ea.get() == 1:
			args.append("True")
		else:
			args.append("False") 

		#Parse through which folder to check
		if self.__radio == 1:
			args.append("All")
		elif self.__radio == 2:
			args.append("Syllabus")
		elif self.__radio == 3:
			args.append("Handouts")
		elif self.__radio == 4:
			args.append("Assignments")
		elif self.__radio == 5:
			args.append("Exams")
		elif self.__radio == 6:
			args.append("Outcome")

		if len(email.keys()) == 1:
			if email["0"] == "":
				self.__terminal.enterLine("Enter the email list file created earlier.")
				startTool = False
			else:
				args.append(email["0"])
		else:
			self.__terminal.enterLine("Enter the email list file created earlier.")
			startTool = False

		print(args)

		#This will start the tool
		if startTool:

			audit = AuditFolder(args[0], args[1], args[2], args[3], args[4], args[5], args[6], self.__terminal, args[7], settingsP)
			lst, tree, gp = audit.start()
			self.__terminal.enterLine("Starting to build tree ...")
			self.__terminal.idle_task()
			tree = audit.buildTree(lst, tree, gp, gp)
			#audit.addedStuff()
			self.__terminal.enterLine("Starting to parse the tree ...")
			self.__terminal.idle_task()
			audit.parser(gp, tree)
			output = audit.returnOutput()
			audit.writingOutput(output)
			#self.__terminal.runProcess("tools/audit.py", args)
		else:
			print("Nope, there are issues")

		self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++++")

	#7) READ INDIRECT
	#this tool will trigger the "Read Indirect" tool
	def readIndirect(self, entry, direct):
		"""
		Parameter Definition
		+ entry --> this is the entrybox associated with the tool
		+ direct --> this is the dictionary that holds the directories used
		"""

		startTool = True #this flag will symbolize whether to start the tool or not
		args = list() #these are the arguments pushed to the class when the tool is initialized

		#----------------------------------------
		#First Step

		#there are two directories expected to get this thing going
		#we need to see if both are initialized, and grab their values
		if len(direct.keys()) == 2:

			#1) First Directory Check
			if direct["0"] == "":
				self.__terminal.enterLine("Please include the directory with the indirect assessment files")
				startTool = False
			else:
				args.append(direct["0"])

			#2) Second Directory Check
			if direct["1"] == "":
				self.__terminal.enterLine("Please include the save directory for the final data")
				startTool = False
			else:
				args.append(direct["1"])
		else:
			#this is triggered when one, or none of the directories are set
			startTool = False
			self.__terminal.enterLine("Please enter both directories to start the tool")

		#----------------------------------------
		#Second Step

		#this will check the value for the name chosen for the saved data
		if entry.get().strip() == "Enter a file name here" or entry.get().strip() == "":
			self.__terminal.enterLine("Please provide a name for the final data file.")
			startTool = False
		else:
			args.append(entry.get().strip())

		#----------------------------------------
		#Final step, start tool

		if startTool:
			#if everything is set, then we can call the tool
			self.__terminal.enterLine("Starting the tool ... ")
			readInd = ReadIndirect(args[0], args[1], args[2], self.__terminal)
			readInd.readTool()
			self.__terminal.enterLine("Done")
		else:
			self.__terminal.enterLine("Tool will not start.")

		self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")

	#8) PARSE INDIRECT
	#this command will trigger the "Parse Indirect" tool
	def parseIndirect(self, files, direct, settingsP):
		"""
		Parameter Definition
		+ files --> this is the dictionary that holds the files used
		+ direct --> this is the dictionary that holds the directories used
		+ settingsP --> this is the path string that holds the settings file
		"""

		startTool = True #this flag will symbolize whether to start the tool or not
		args = list() #these are the arguments pushed to the class when the tool is initialized

		#----------------------------------------
		#First Step

		#For this tool, we need the file that was generated by the readIndirect tool
		#so we need to check if the file has been set, and if so, get the value
		if len(files.keys()) != 0:

			#1) The only check for the file, so this still needs
			#to be run, because the tool will set "" as the file value
			#if the file dialog is closed without choosing a file
			if files["0"] == "":
				self.__terminal.enterLine("Please enter the file that holds the indirect data.")
				startTool = False
			else:
				args.append(files["0"])
		else:
			#this is run if no file has been set
			self.__terminal.enterLine("Please enter the file that holds the indirect data.")
			startTool = False

		#----------------------------------------
		#Second Step

		#A final save directory is also expected, so we will check for this here
		if len(direct.keys()) != 0:

			#1) There is only one check, which is the save directory for the 
			#parsed files
			if direct["0"] == "":
				self.__terminal.enterLine("Please enter the save directory")
				startTool = False
			else:
				args.append(direct["0"])
		else:
			self.__terminal.enterLine("Please enter the save directory")
			startTool = False

		#----------------------------------------
		#Final step, start tool

		if startTool:
			#If everything is working, then we can just start the tool here
			self.__terminal.enterLine("Starting the tool ... ")
			parseInd = ParseIndirect(args[0], args[1], self.__terminal, settingsP)
			parseInd.startReading()
			parseInd.createResult()
			self.__terminal.enterLine("Done")
		else:
			self.__terminal.enterLine("Tool will not Start.")

		self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")
