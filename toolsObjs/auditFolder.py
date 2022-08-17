import os
import sys
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import json

class auditFolder:

	#---------------------
	#These are the variables that will be used by the class to 
	#actually run the tool

	__globalPath = "" #this is the path to the folder that will be audited

	__count = 0 #this is how many backslashes are in the path, this is important for the code to run

	__savePath = "" #this is where the final compiled data will be saved

	__outputName = "" #this is the name of the output file

	__countEmpty = 0 #this is a flag that will be applied to the audit, 
	#and it will determine whether the audit will count how many empty 
	#subfolders there are

	__showEmpty = 0 #this is a flag that will be applied to the formatting of
	#the output. It will list the empty subfolders under the main folders

	__emailAudit = 0 #this is a flag that will tell the tool where to email
	#the audit's results

	__whatToAudit = 0 #this is another flag, it is applied to the audit. It
	#essentially just determines what folders to audit

	__auditAll = True #this is a flag associated with the other flag up top, 
	#it's just the boolean version

	__output = dict() #this is the output dictionary

	__listEmpty = []

	__settings = []

	#----
	#these are just some output stuff, because people tend to not follow rules,
	#so some of these will hold the actual audit folders, and other will hold folders
	#that are not suppose to exist

	__mainFolders = [] #this is the list of all the folders based on class name and section number

	__addedFolders = [] #this is the list of folders that were added, but are not needed

	#-----
	#this is strictly for the parser section
	__empty = 0
	__full = 0
	__notDeepest = 0
	__descent = 0

	#---------------------

	def __init__(self, gPath, sPath, name, cE, sE, eA, wA):
		#gPath --> global path
		#sPath --> save path
		#name --> output name
		#cE --> count empty
		#sE --> show empty
		#eA --> email audit
		#wA --> what to audit

		self.__globalPath = gPath + "/"
		self.__count = self.__globalPath.count("/")
		self.__savePath = sPath
		self.__outputName = name
		self.__countEmpty = cE
		self.__showEmpty = sE
		self.__emailAudit = eA
		self.__whatToAudit = wA

		if self.__whatToAudit != "All":
			self.__auditAll = False

		fl = open("../encapsulated/settings.json", "r")
		data = json.load(fl)

		for keys in data["Subfolders"].keys():
			self.__settings.append(keys)

		print(self.__settings)

	def start(self):
		lst = os.listdir(self.__globalPath)
		tree = {self.__globalPath: [list(), list(), self.__globalPath, ""]}
		return lst, tree, self.__globalPath

	def showOutput(self):
		print(self.__output)

	def returnOutput(self):
		return self.__output

	def buildTree(self, fldrs, tree, fullpath, prevFlder):
		for item in fldrs:

			#this is the path with the new stuff added to it
			newPth = fullpath + item + "/"

			if os.path.isdir(newPth):
				if fullpath.count("/") == self.__count + 1:
					self.__mainFolders.append(newPth)

					#this is where we'll start building the output dictionary
					#this conditional will run when --> globalPath/className/sectionNumber
					#this will split that path to find the className and the sectionNumber
					#and subsequently build the output dictionary

					#this is a regex expression to find the backslashes in the code
					backSlash = re.compile("/")
					listBackSlash = [m.start() for m in backSlash.finditer(newPth)]

					className = newPth[listBackSlash[-3]+1:listBackSlash[-2]]

					#these try excepts will be used to build the output dictionary, so nothing
					#is erased with each new class
					try:
						self.__output[className]
					except:
						self.__output[className] = dict()
						self.__output[className][item] = dict()

					#this will be if new sections appear, so nothing is lost, and the 
					#previously build section dictionaries are not written over
					try:
						self.__output[className][item]
					except:
						self.__output[className][item] = dict()

				#this conditional will run when you start getting to lower subfolders,
				#specifically the main ones that are used every year
				#["Syllabus", "Handouts", "Outcomes", "Assignments", "Exams"]
				#any other folders on this level will be ignored !!!!!!
				#that's final, I'm sick and tired of finding those folders
				if fullpath.count("/") == self.__count + 2:
					#this first conditional will just remove the unnecessary folders
					#if item != "Syllabus" and item != "Handouts" and item != "Assignments" and item != "Exams" and item != "Outcome":
						#the reason I use and, is because if it equals at least one of these, it's valid, but if a valid folder
						#is found, and I had used or, it will flag this conditional
					#	self.__addedFolders.append(newPth)
					#	continue
					if item not in self.__settings:
						#the reason I use and, is because if it equals at least one of these, it's valid, but if a valid folder
						#is found, and I had used or, it will flag this conditional
						self.__addedFolders.append(newPth)
						continue

					#this conditional will see how the flag has been set, and which folders to search
					if self.__auditAll:
						#this conditional is run if the tool is to audit all the main subfolders
						tree[fullpath][0].append(newPth)
						tree[newPth] = [list(), list(), item, prevFlder]
						self.buildTree(os.listdir(newPth), tree, newPth, newPth)
					else:
						if item == self.__whatToAudit:
							tree[fullpath][0].append(newPth)
							tree[newPth] = [list(), list(), item, prevFlder]
							self.buildTree(os.listdir(newPth), tree, newPth, newPth)
				else:
					tree[fullpath][0].append(newPth)
					tree[newPth] = [list(), list(), item, prevFlder]
					self.buildTree(os.listdir(newPth), tree, newPth, newPth)
			else:
				if item != ".DS_Store":
					try:
						tree[fullpath][1].append(item)
					except:
						tree[fullpath] = [list(), list()]
						tree[fullpath][1].append(item)

		return tree

	def parser(self, path, tree):
		if path.count("/") > self.__count + 3:
			self.__descent = 1

		#begin the descent
		if len(tree[path][0]) != 0:
			#if there are subfolders, we need to go deeper
			if len(tree[path][1]) != 0:
				#this conditional is run if the folders that aren't the deepest are
				#used to store data. it will be included as a subfolder, whether by mistakenly
				#putting the data there, or not. It is now grouped with the deepest
				#subfolders
				self.__full += 1
				self.__notDeepest += 1

			for pt in tree[path][0]:
				self.parser(pt, tree)

		else:
			if len(tree[path][1]) != 0:
				self.__full += 1
			else:
				self.__empty += 1
				pth = re.compile("/")
				listBackSlash = [m.start() for m in pth.finditer(path)]
				if path.count("/") > self.__count + 3:
					index = listBackSlash[self.__count + 2]
					self.__listEmpty.append(path[index+1:])


		if path.count("/") == self.__count + 3:
			pth = re.compile("/")
			listBackSlash = [m.start() for m in pth.finditer(path)]

			className = path[listBackSlash[-4]+1:listBackSlash[-3]]
			sectionNumber = path[listBackSlash[-3]+1:listBackSlash[-2]]
			folder = path[listBackSlash[-2]+1:listBackSlash[-1]]

			self.__output[className][sectionNumber][folder] = list()

			if self.__descent != 0:
				self.__output[className][sectionNumber][folder].append(str(self.__full + self.__empty) + " subfolders")
				self.__output[className][sectionNumber][folder].append(self.__full)
				self.__output[className][sectionNumber][folder].append(self.__empty)
			else:
				self.__output[className][sectionNumber][folder].append("no subfolders")
				self.__output[className][sectionNumber][folder].append(-1)
				self.__output[className][sectionNumber][folder].append(-1)

			if self.__full != 0 and self.__empty == 0:
				self.__output[className][sectionNumber][folder].append("FULL")
			elif self.__full == 0 and self.__empty != 0:
				self.__output[className][sectionNumber][folder].append("EMPTY")
			elif self.__full != 0 and self.__empty != 0:
				if self.__full >= self.__empty:
					self.__output[className][sectionNumber][folder].append("Mostly FULL")
				else:
					self.__output[className][sectionNumber][folder].append("Mostly EMPTY")

			self.__output[className][sectionNumber][folder].append(self.__listEmpty)

			self.__empty = 0
			self.__full = 0
			self.__notDeepest = 0
			self.__descent = 0
			self.__listEmpty = []

	def emailData(self, output):
		load_dotenv()
		password = os.getenv("TESTPASS")

		for emails in output.keys():
			smtpObj = self.setUpSMTP(emails)
			self.sendMail(smtpObj, output[emails])

	def setUpSMTP(contacts):
		msg = EmailMessage()
		msg["Subject"] = "Automated ABET Audit"
		msg["From"] = "weeksk2@unlv.nevada.edu"
		msg["To"] = contacts
		msg.set_content('This is something \n\t\t I guess')
		return msg

	def sendMail(self, obj, message):
		obj.set_content(message)
		with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
			smtp.login("weeksk2@unlv.nevada.edu", PASSWORD)
			smtp.send_message(obj)

	def addedStuff(self):
		print(self.__addedFolders)


audit = auditFolder("/Users/dubliciousbaby/Desktop/csspring5", "", "", 0, 0, 0, "Outcome")

lst, tree, gp = audit.start()

tree = audit.buildTree(lst, tree, gp, gp)

audit.addedStuff()

audit.parser(gp, tree)

output = audit.returnOutput()

"""for classNames in output.keys():
	print(classNames)
	for sections in output[classNames].keys():
		print("\t" + sections)
		for folders in output[classNames][sections].keys():
			print("\t\t" + folders)
			for items in output[classNames][sections][folders]:
				print("\t\t\t" + str(items))

		print("-------------------------------------")"""

