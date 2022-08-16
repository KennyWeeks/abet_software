"""
This will just hold all the methods from the bodyframes that I'm not currently editing
"""
#3) DOWNLOAD FOLDER
#this tool will trigger the "Download Current Folder" tool
def downloadFolder(self, e):
if e.get().strip() == "Enter a folder name here" or e.get().strip() == "":
self.__terminal.enterLine("Enter a folder name to start using the tool.")
else:
args = e.get().strip() + ", " + str(self.__shared.get())
self.__terminal.runProcess("tools/downloadFolder.py", args)

#4) AUDIT FOLDER
#this tool will trigger the "Audit folder" tool
def auditFolder(self, e, ce, se, ea):
self.__terminal.enterLine("---------------------")
startTool = True #this is a flag to start the tool
args = "" #this is the arguments that are passed to the tool

#this will check to see if the two directories have been chosen
if self.__directory["0"] == "":
self.__terminal.enterLine("Missing the path to the directory with the assessment.")
else:
args += self.__directory["0"] + "/, "

if self.__directory["1"] == "":
self.__terminal.enterLine("Missing the path to the directory for the final saved audit.")
else:
args += self.__directory["1"] + ", "

#This will get the text written in the entry block
if e.get().strip() == "Enter a folder name here" or e.get().strip() == "":
self.__terminal.enterLine("Please enter the name of the final save file.")
startTool = False
else:
args += e.get().strip() + ", "

#parse through which check marks have been made
if ce.get() == 1:
args += "True, "
else:
args += "False, "

if se.get() == 1:
args += "True, "
else:
args += "False, "

if ea.get() == 1:
args += "True, "
else:
args += "False, " 

#Parse through which folder to check
if self.__auditFolders == 1:
args += "All"
elif self.__auditFolders == 2:
args += "Syllabus"
elif self.__auditFolders == 3:
args += "Handouts"
elif self.__auditFolders == 4:
args += "Assignments"
elif self.__auditFolders == 5:
args += "Exams"
elif self.__auditFolders == 6:
args += "Outcome"


#This will start the tool
if startTool:
self.__terminal.enterLine("Starting tool")
self.__terminal.runProcess("tools/audit.py", args)
else:
print("Nope, there are issues")

#7) READ INDIRECT
#This will call the function to start the indirect assessment stuff
def readIndirect(self, e):
startTool = True
args = ""
if len(self.__directory.keys()) == 2:
	if self.__directory["0"] == "":
		self.__terminal.enterLine("Please select the indirect folder.")
		startTool = False
	else:
		args += self.__directory["0"] + ", "

	if self.__directory["1"] == "":
		self.__terminal.enterLine("Please select the destination folder.")
		startTool = False
	else:
		args += self.__directory["1"] + ", "
else:
	self.__terminal.enterLine("Please provide both folders to use tool")
	startTool = False

if e.get().strip() == "Enter a folder name here" or e.get().strip() == "":
	self.__terminal.enterLine("Please enter the name of the final save file.")
	startTool = False
else:
	args += e.get().strip()

if startTool:
	print(args)
	#self.__terminal.runProcess("tools/readIndirect.py", args)

#8) PARSE INDIRECT
#this will trigger the software to parse the indirect assessment data
def parseIndirect(self):
startTool = True
args = ""

#
if len(self.__filenames.keys()) == 1:
	if self.__filenames["0"] == "":
		self.__terminal.enterLine("Please enter a csv file for data.")
		startTool = False
	else:
		args += self.__filenames["0"] + ", "
else:
	self.__terminal.enterLine("Please enter a csv file for data.")
	startTool = False

#
if len(self.__directory.keys()) == 1:
	if self.__directory["0"] == "":
		self.__terminal.enterLine("Please enter a directory to save the parsed results.")
		startTool = False
	else:
		args += self.__directory["0"] + ", "
else:
	self.__terminal.enterLine("Please enter a directory to save the parsed results.")
	startTool = False

#
if startTool:
	print(args)
	#self.__terminal.runProcess("tools/parseindirect.py", args)

def checkName(self, event, entryBox):
#same thing as above, because everything is very mechanical, when the user clicks the entry box, and if they choose
#to not enter anything, the default text will appear, but that's not automatic, I needed to code that 
if entryBox.get() == " ":
	entryBox.config(fg="#bebebe")
	entryBox.insert(0, "Enter a folder name here")

#this will save folders selected by different tools in the application
def getFoldersCorrect(self, name, i):
directory = fd.askdirectory()
if len(directory) == 0:
	for c in self.__styleFrame.winfo_children():
		if str(type(c)) == "<class 'tkinter.Label'>":
			if str(c).find(name) != -1:
				c.config(text="")
	self.__directory[i] = ""
else:
	pos = [m.start() for m in re.finditer("/", directory)]
	direct = directory[pos[-1]+1:]
	label = Label(self.__styleFrame, text=direct, name=name)
	label.place(x=x, y=y)
	self.__root.focus_set()
	self.__directory[i] = directory

def checkRadio(self, selected):
self.__auditFolders = selected;


#3) DOWNLOAD CURRENT FOLDER
def DownloadCabinet(self):
	self.__terminal.enterLine("- Progess terminal for Downloading Cabinet -->")
	self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++")

	#this will prompt the user to 
	selectFolderDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	selectFolderDesc.insert('1.0', "--> Enter the name of the folder you want to download from Google Drive here")
	selectFolderDesc.config(state=DISABLED)
	selectFolderDesc.place(x=10, y=10)

	#This is the entry box
	entryBox = Entry(self.__styleFrame, bg="#ffffff", fg="#bebebe", highlightthickness=0)
	entryBox.insert(0, "Enter a folder name here")
	entryBox.place(x=8, y=41, width=200)

	#This is just something I want to add so the default text is removed when the user focuses on the box
	entryBox.bind("<Button-1>", lambda event, e=entryBox: self.entryClick(event, e))

	#This will prompt the user to determine if the folder is shared with them, or in their main directory
	selectSharedDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	selectSharedDesc.insert('1.0', "--> Has this folder been shared with you? If so, check the box below. Otherwise, leave it unchecked.")
	selectSharedDesc.config(state=DISABLED)
	selectSharedDesc.place(x=10, y=70)

	#this needs to be done so the variable is active for the checkbox to use
	self.__shared = IntVar()

	#this is the check box that will be used to find if the folder was shared or not
	checkBox = Checkbutton(self.__styleFrame, text="Shared Item", variable=self.__shared, onvalue=1, offvalue=0)
	checkBox.place(x=5, y=110)

	#This will prompt the user to download the folder
	downloadDesc = Text(self.__styleFrame, bg="#323232", width=40, height=5, wrap=WORD, highlightthickness=0)
	downloadDesc.insert('1.0', "--> Press the button below to begin downloading the folder from drive.")
	downloadDesc.config(state=DISABLED)
	downloadDesc.place(x=10, y=135)

	download = Button(self.__styleFrame, text="Download Folder", command=lambda e=entryBox: self.downloadFolder(e))
	download.place(x=5, y=165)

#4) AUDIT FOLDER
def AuditCabinet(self):
	self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++")
	self.__terminal.enterLine("- Progess terminal for the Audit -->")
	self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++")

	canvas = Canvas(self.__styleFrame, highlightthickness=0)
	canvas.pack(side=LEFT, fill=BOTH, expand=1)

	scrollBar = ttk.Scrollbar(self.__styleFrame, orient=VERTICAL, command=canvas.yview)
	scrollBar.pack(side=RIGHT, fill=Y)

	canvas.configure(yscrollcommand=scrollBar.set)
	canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

	bodyFrame = Frame(canvas)

	canvas.create_window((0, 0), window=bodyFrame, anchor="nw")

	r=1
	#--------------
	#This is where I will start adding the parts of the tool.
	#-------------
	selectDirectDesc = Label(bodyFrame, text="--> Select the directory to audit", bg="#323232", fg="#ffffff")
	selectDirectDesc.grid(sticky=W, row=1, column=0, padx=5, pady=5)

	openFolder = Button(bodyFrame, text="Open Directory", command=lambda bf=bodyFrame: self.getFolderForGrid(bf, 135, 35, "openFolder", "0"))
	openFolder.grid(sticky=W, row=2, column=0, padx=5)

	"""beginAuditDesc = Label(bodyFrame, text="--> Once you've downloaded the current ABET Folder, you can perform an audit to see if the folder is up to date.", bg="#323232", fg="#ffffff", wraplength=300, justify=LEFT)
	beginAuditDesc.grid(sticky=W, row=3, column=0, padx=5, pady=5)"""

	selectParamsForAudit = Label(bodyFrame, text="--> Before you start the audit, you can select which subfolder the program will audit, as well as how much of each subfolder is filled.", bg="#323232", fg="#ffffff", wraplength=300, justify=LEFT)
	selectParamsForAudit.grid(sticky=W, row=3, column=0, padx=5, pady=5)

	divider = Label(bodyFrame, text="------------------------------------", bg="#323232", fg="#ffffff", wraplength=300, justify=LEFT)
	divider.grid(sticky=W, row=4, column=0, padx=5)

	titleRadio = Label(bodyFrame, text="-- Select which subfolder to audit --", bg="#323232", fg="#ffffff", justify=LEFT)
	titleRadio.grid(sticky=W, row=5, column=0, padx=5)

	#---------------
	#Subfolder check
	allCheckBox = Radiobutton(bodyFrame, text="Audit all subfolders", variable=self.__auditFolders, value=1, command=lambda :self.checkRadio(1))
	allCheckBox.select()
	allCheckBox.grid(sticky=W, row=6, column=0, padx=5, pady=5)

	sylCheckBox = Radiobutton(bodyFrame, text="Audit only Syllabus ", variable=self.__auditFolders, value=2, command=lambda: self.checkRadio(2))
	sylCheckBox.grid(sticky=W, row=7, column=0, padx=5, pady=5)

	handCheckBox = Radiobutton(bodyFrame, text="Audit only Handouts", variable=self.__auditFolders, value=3, command=lambda: self.checkRadio(3))
	handCheckBox.grid(sticky=W, row=8, column=0, padx=5, pady=5)

	assCheckBox = Radiobutton(bodyFrame, text="Audit only Assignments", variable=self.__auditFolders, value=4, command=lambda: self.checkRadio(4))
	assCheckBox.grid(sticky=W, row=9, column=0, padx=5, pady=5)

	examsCheckBox = Radiobutton(bodyFrame, text="Audit only Exams", variable=self.__auditFolders, value=5, command=lambda: self.checkRadio(5))
	examsCheckBox.grid(sticky=W, row=10, column=0, padx=5, pady=5)

	outCheckBox = Radiobutton(bodyFrame, text="Audit only Outcome", variable=self.__auditFolders, value=6, command=lambda: self.checkRadio(6))
	outCheckBox.grid(sticky=W, row=11, column=0, padx=5, pady=5)

	divider = Label(bodyFrame, text="------------------------------------", bg="#323232", fg="#ffffff", wraplength=300, justify=LEFT)
	divider.grid(sticky=W, row=12, column=0, padx=5)

	titleCheck = Label(bodyFrame, text="-- Select how the audit works --", bg="#323232", fg="#ffffff", justify=LEFT)
	titleCheck.grid(sticky=W, row=13, column=0, padx=5)

	countEmptyV = IntVar()
	showEmptyV = IntVar()
	emailAuditV = IntVar()

	countEmpty = Checkbutton(bodyFrame, text="Count empty folders", variable=countEmptyV, onvalue=1, offvalue=0)
	countEmpty.grid(sticky=W, row=14, column=0, pady=5, padx=5)

	showFinalEmpty = Checkbutton(bodyFrame, text="Show empty subfolders in final audit", variable=showEmptyV, onvalue=1, offvalue=0)
	showFinalEmpty.grid(sticky=W, row=15, column=0, pady=5, padx=5)

	emailAudit = Checkbutton(bodyFrame, text="Email Audit", variable=emailAuditV, onvalue=1, offvalue=0)
	emailAudit.grid(sticky=W, row=16, column=0, pady=5, padx=5)

	divider = Label(bodyFrame, text="------------------------------------", bg="#323232", fg="#ffffff", wraplength=300, justify=LEFT)
	divider.grid(sticky=W, row=17, column=0, padx=5)

	nameAudit = Label(bodyFrame, text="--> Name the final audit file (*.txt)", bg="#323232", fg="#ffffff", justify=LEFT)
	nameAudit.grid(sticky=W, row=18, column=0, padx=5, pady=5)

	entryBox = Entry(bodyFrame, bg="#ffffff", fg="#000000", highlightthickness=0)
	#entryBox.insert(0, "Enter a folder name here")
	entryBox.grid(sticky=W, row=19, column=0, padx=9, pady=5)
	entryBox.config(insertbackground="#000000")

	selectSaveDir = Label(bodyFrame, text="--> Select the directory to save the audit", bg="#323232", fg="#ffffff")
	selectSaveDir.grid(sticky=W, row=20, column=0, padx=5, pady=5)

	openFolder = Button(bodyFrame, text="Open Directory", command=lambda bf=bodyFrame: self.getFolderForGrid(bf, 135, 640, "saveAudit", "1"))
	openFolder.grid(sticky=W, row=21, column=0, padx=5)

	startAudit = Label(bodyFrame, text="--> Start the audit", bg="#323232", fg="#ffffff")
	startAudit.grid(sticky=W, row=22, column=0, padx=5, pady=5)

	strAuditB = Button(bodyFrame, text="Start Audit", command=lambda e=entryBox, ce=countEmptyV, se=showEmptyV, ea=emailAuditV: self.auditFolder(e, ce, se, ea))
	strAuditB.grid(sticky=W, row=23, column=0, padx=5)

	lbl = Label(bodyFrame)
	lbl.grid(sticky=W, row=24, column=0, pady=5)

#5) PARSE OUTCOME
def ParseAudit(self):
	self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++")
	self.__terminal.enterLine("- Progess terminal for Parsing Audit Data -->")
	self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++")

	#this will prompt the user to 
	selectFolderDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	selectFolderDesc.insert('1.0', "--> Select the ABET Folder you would like to audit.")
	selectFolderDesc.config(state=DISABLED)
	selectFolderDesc.place(x=10, y=10)

	selectFile = Button(self.__styleFrame, text="Open Directory", command=lambda x=-150, y=65, i=0: self.getFolders(x, y))
	selectFile.place(x=5, y=35)

	nameFinalFileDesc = Text(self.__styleFrame, bg="#323232", width=40, height=5, wrap=WORD, highlightthickness=0)
	nameFinalFileDesc.insert("1.0", "--> Name the file that will hold the parsed outcome assessment. (*.txt)")
	nameFinalFileDesc.config(state=DISABLED)
	nameFinalFileDesc.place(x=10, y=65)




	#This is the entry box
	entryBox = Entry(self.__styleFrame, bg="#ffffff", fg="#bebebe", highlightthickness=0)
	entryBox.insert(0, "Enter a folder name here")
	entryBox.place(x=8, y=96, width=200)
	entryBox.focus_set()

	#This is just something I want to add so the default text is removed when the user focuses on the box
	entryBox.bind("<Button-1>", lambda event, e=entryBox: self.entryClick(event, e))


	emptyOrIncorrectOutcome = Text(self.__styleFrame, bg="#323232", width=40, height=5, wrap=WORD, highlightthickness=0)
	emptyOrIncorrectOutcome.insert("1.0", "--> Generate a file with empty or incorrect outcomes (*_empty_inc.txt)")
	emptyOrIncorrectOutcome.config(state=DISABLED)
	emptyOrIncorrectOutcome.place(x=10, y=125)	

	#this is the check box that will be used to find if the folder was shared or not
	checkBox = Checkbutton(self.__styleFrame, text="List Empty/Incorrect", variable=self.__emptyIncorrect, onvalue=1, offvalue=0)
	checkBox.place(x=5, y=152)

	startToolDesc = Text(self.__styleFrame, bg="#323232", width=40, height=1, wrap=WORD, highlightthickness=0)
	startToolDesc.insert("1.0", "--> Start Tool")
	startToolDesc.config(state=DISABLED)
	startToolDesc.place(x=10, y=177)

	startTool = Button(self.__styleFrame, text="Start Tool")
	startTool.place(x=5, y=190)

#7) READ INDIRECT
def ReadIndirect(self):
	self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++++")
	self.__terminal.enterLine("- Progess terminal to Read Indirect Reports -->")
	self.__terminal.enterLine("+++++++++++++++++++++++++++++++++++++++++++++++++")

	#This is where the user will select the location of the indirect assessment results
	selectFileDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	selectFileDesc.insert('1.0', "--> Select the directory where the indirect assessments are stored.")
	selectFileDesc.config(state=DISABLED)
	selectFileDesc.place(x=10, y=10)

	selectFile = Button(self.__styleFrame, text="Select Indirect Folder", command=lambda x=175, y=40: self.getFoldersCorrect(x, y, "selInd", "0"))
	selectFile.place(x=5, y=36)

	#This is where the user will save their results
	saveFileDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	saveFileDesc.insert('1.0', "--> Select where to save the results pulled from the indirect assessments.")
	saveFileDesc.config(state=DISABLED)
	saveFileDesc.place(x=10, y=68)

	saveFile = Button(self.__styleFrame, text="Select Destination", command=lambda x=155, y=98: self.getFoldersCorrect(x, y, "selDest", "1"))
	saveFile.place(x=5, y=94)

	#This is where the user will name the file
	fileNameDesc = Text(self.__styleFrame, bg="#323232", width=40, height=4, wrap=WORD, highlightthickness=0)
	fileNameDesc.insert('1.0', "--> Name the file here. (*.csv)")
	fileNameDesc.config(state=DISABLED)
	fileNameDesc.place(x=10, y=124)

	entryBox = Entry(self.__styleFrame, bg="#ffffff", fg="#bebebe", highlightthickness=0)
	entryBox.insert(0, "Enter a folder name here")
	entryBox.place(x=8, y=142, width=200)
	entryBox.config(insertbackground="#000000")

	#This is just something I want to add so the default text is removed when the user focuses on the box
	entryBox.bind("<Button-1>", lambda event, e=entryBox: self.entryClick(event, e))

	#This will prompt the user to start the tool
	startToolDesc = Text(self.__styleFrame, bg="#323232", width=40, height=4, wrap=WORD, highlightthickness=0)
	startToolDesc.insert('1.0', "--> Start reading and grabbing data from the indirect assessment")
	startToolDesc.config(state=DISABLED)
	startToolDesc.place(x=10, y=168)

	startReader = Button(self.__styleFrame, text="Start Reader", command=lambda e=entryBox: self.readIndirect(e))
	startReader.place(x=5, y=194)

#8) PARSE INDIRECT
def ParseIndirect(self):
	self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++++")
	self.__terminal.enterLine("- Progess terminal for Parsing Indirect Data -->")
	self.__terminal.enterLine("++++++++++++++++++++++++++++++++++++++++++++++++")

	#This will allow the user to select the indirect csv file so that it can be used for the parsing
	selectFileDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	selectFileDesc.insert('1.0', "--> Select the file where the indirect assessments results were stored.")
	selectFileDesc.config(state=DISABLED)
	selectFileDesc.place(x=10, y=10)

	selectFile = Button(self.__styleFrame, text="Select CSV file", command=lambda x=135, y=40: self.getFile(x, y, "selCsv", "0"))
	selectFile.place(x=5, y=36)

	#This is where the user will save their results
	saveFileDesc = Text(self.__styleFrame, bg="#323232", width=40, height=10, wrap=WORD, highlightthickness=0)
	saveFileDesc.insert('1.0', "--> Select where the parsed results will be saved.")
	saveFileDesc.config(state=DISABLED)
	saveFileDesc.place(x=10, y=68)

	saveFile = Button(self.__styleFrame, text="Select Destination", command=lambda x=156, y=98: self.getFoldersCorrect(x, y, "selDest", "0"))
	saveFile.place(x=5, y=94)

	#This will prompt the user to start the tool
	fileNameDesc = Text(self.__styleFrame, bg="#323232", width=40, height=4, wrap=WORD, highlightthickness=0)
	fileNameDesc.insert('1.0', "--> Begin the parser.")
	fileNameDesc.config(state=DISABLED)
	fileNameDesc.place(x=10, y=124)

	selectFile = Button(self.__styleFrame, text="Start Parser", command=self.parseIndirect)
	selectFile.place(x=5, y=138)
