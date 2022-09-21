import json
from tkinter import *
from toolsObjs.emailList import EmailList
from toolsObjs.auditFolder import AuditFolder
from toolsObjs.createFolder import CreateFolder
import os

class ActionMethods:

	__terminal = None #this is this methods copy of the terminal. It's the same terminal, just a copy

	__radio = 1

	def setTerminal(self, terminal):
		self.__terminal = terminal

	def terminalDestroy(self):
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
					if len(checkB) != 4:
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

		columnDict = {"Professor": [], "Email": [], "Class #": [], "Section #": []}

		ind = 0
		for key in columnDict.keys():
			columnDict[key].append(dropDown[ind].get())
			ind += 1

		#start the tool if possible
		if startTool:
			print(args)
			el = EmailList(args[1], args[0], args[2], self.__terminal, columnDict, settingsP)
			el.createFile()


		self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++++")

	#2) CREATE ABET CABINET
	#this tool will trigger the "Create ABET Cabinet" folder
	def createFolder(self, e, filenames, checkBoxes, directory, settingsPath):
		startTool = True
		args = list()

		#check if the schedule is provided
		if len(filenames.keys()) != 0:
			if filenames["0"] == "":
				self.__terminal.enterLine("Please provide a class schedule file.")
				startTool = False
			else:
				args.append(filenames["0"])
				#We can look at the checkboxes selected here
				allZero = True
				checkB = list()
				for keys in checkBoxes["scheduleFileName"].keys():
					if checkBoxes["scheduleFileName"][keys].get() != 0:
						checkB.append(keys)
						allZero = False
				
				if allZero:
					self.__terminal.enterLine("Please select at least one column to use from the provided file to start the tool")
					startTool = False
				else:
					args.append(checkB)

		else:
			self.__terminal.enterLine("You need to provide a schedule file to start the tool.")
			startTool = False

		#check if the name is provided
		if e.get().strip() == "Enter a folder name here" or e.get().strip() == "":
			self.__terminal.enterLine("Enter a folder name to start using the tool.")
			startTool = False
		else:
			args.append(e.get().strip())

		if len(directory.keys()) != 0:
			if directory["0"] == "":
				self.__terminal.enterLine("Please provide a save directory.")
				startTool = False
			else:
				args.append(directory["0"])
		else:
			self.__terminal.enterLine("You need to provide a save directory to start the tool.")
			startTool = False

		#check if the tool can be started
		if startTool:
			#self.__terminal.enterLine(args)
			inst = CreateFolder(self.__terminal, args, settingsPath)
			inst.createCabinet()
			#self.__terminal.runProcess("tools/createFolder.py", args)

		self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++")

	#4) AUDIT FOLDER
	#this tool will trigger the "Audit folder" tool
	def auditFolder(self, direct, email, entry, ce, se, ea, settingsP):
		startTool = True #this is a flag to start the tool
		args = [] #this is the arguments that are passed to the tool

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

