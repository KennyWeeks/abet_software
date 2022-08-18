from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from encapsulated.imageClass import TitleButtons

class MenuBar:

	__current = 0
	__currentLabel = None #label text of currently used tool
	__menuBar = None #frame holding the menubar
	__tags = None #these are the tags that hold each tool title
	__frames = None #these are the individual, clickable menu items
	__labels = None #these are the individual, clickable menu labels
	__bodyFrame = None #this is the current bodyframe displayed
	__currentLabel = None #this is what type of tool is being used

	__photo = None

	#---------------------------------
	#These are event driven methods, like when an item is click or hovered over
	#---------------------------------
	def hoverIn(self, event, frame, label):
		if str(label.config("text")[-1]) != self.__curentLabel:
			frame.config(bg="#444444")
			label.config(bg="#444444")

	def hoverOut(self, event, frame, label):
		if str(label.config("text")[-1]) != self.__curentLabel:
			frame.config(bg="#222222")
			label.config(bg="#222222")

	def changeTool(self, event, frame, label):
		index = self.__tags.index(str(label.config("text")[-1]))

		if index != self.__current:
			#set new frame
			if index != 7:
				frame.config(bg="#444444")
				label.config(bg="#444444")

			if self.__current != 7:
				#reset old frame
				self.__frames[self.__current].config(bg="#222222")
				self.__labels[self.__current].config(bg="#222222")

			#set the current stuff here
			self.__current = index
			self.__curentLabel = self.__tags[index]

			#this will just show what section is currently being worked on
			if index >= 0 and index <= 3:
				self.__currentLabel.config(text="DIRECT ASSESSMENT")
			elif index >= 5 and index < 7:
				self.__currentLabel.config(text="INDIRECT ASSESSMENT")
			elif index == 4:
				self.__currentLabel.config(text="EXIT INTERVIEW")
			else:
				self.__currentLabel.config(text="SETTINGS")

			#change the body frame
			self.__bodyFrame.changeFrame(index)


	#---------------------------------
	#these are class methods, used to create items on the interface
	#---------------------------------
	def __init__(self, root, bodyFrame, currentLabel, photo):
		self.__menuBar = Frame(root, bg="#444400")
		self.__menuBar.place(x=0, y=40, width=150, height=360)
		self.__bodyFrame = bodyFrame
		self.__currentLabel = currentLabel
		self.__photo = photo

	def items(self, current):
		self.__current = current #save the current tool being used
		#this is the section for the direct assessment
		#---------------------------------------------
		#this is the red title bar
		directSection = Frame(self.__menuBar, bg="#ff2e2e")
		directSection.place(x=0, y=0, width=150, height=40)

		directLabel = Label(directSection, bg="#ff2e2e", text="DIRECT")
		directLabel.place(x=10, y=0, height=40)

		#these are the menu options for the direct assessment
		self.__tags = ["Email List", "ABET Cabinet", "Audit Folder", "Parse Direct", "Interview Results", "Read Results", "Parse Results", "Settings"]
		#self.__tags = ["Email List", "ABET Cabinet", "Interview Results", "Read Results", "Parse Results", "Audit"]

		self.__curentLabel = self.__tags[current] #save the current label we are using

		#this is used for the click change event
		self.__frames = list()
		self.__labels = list()

		y = 40 #this is the starting y position
		for t in range(4):
			color = "#222222"
			if t == current:
				color = "#444444"
			#This is the menu option panel
			menuFrame = Frame(self.__menuBar, bg=color, width=150, height=30)
			menuFrame.place(x=0, y=y)

			#this is the menu label
			label = Label(menuFrame, fg="#ffffff", text=self.__tags[t], bg=color)
			label.place(x=10, y=0, height=25)

			#save the created frame and label
			self.__frames.append(menuFrame)
			self.__labels.append(label)

			#bind a hover in event for when the mouse enters the menu item
			menuFrame.bind("<Enter>", lambda event, f=menuFrame, l=label: self.hoverIn(event, f, l))
			label.bind("<Enter>", lambda event, f=menuFrame, l=label: self.hoverIn(event, f, l))

			#I don't want to hover in event to persist once the mouse leaves
			menuFrame.bind("<Leave>", lambda event, f=menuFrame, l=label: self.hoverOut(event, f, l))
			label.bind("<Leave>", lambda event, f=menuFrame, l=label: self.hoverOut(event, f, l))

			#this is the event bind that will change the tool being used
			menuFrame.bind("<Button-1>", lambda event, f=menuFrame, l=label: self.changeTool(event, f, l))
			label.bind("<Button-1>", lambda event, f=menuFrame, l=label: self.changeTool(event, f, l))

			#this is the menu tag position
			y+=30

		exitSection = Frame(self.__menuBar, bg="#ff2e2e")
		exitSection.place(x=0, y=y, width=150, height=40)

		exitLabel = Label(exitSection, bg="#ff2e2e", text="EXIT INT.")
		exitLabel.place(x=10, y=0, height=40)

		y+=40

		#this is the menu option panel
		menuFrame = Frame(self.__menuBar, bg="#222222")
		menuFrame.place(x=0, y=y, width=150, height=30)

		#this is the menu label
		label = Label(menuFrame, bg="#222222", fg="#ffffff", text="Interview Results")
		label.place(x=10, y=0, height=25)

		#save the newly created frame and label
		self.__frames.append(menuFrame)
		self.__labels.append(label)

		#bind a hover in event for when the mouse enters the menu item
		menuFrame.bind("<Enter>", lambda event, f=menuFrame, l=label: self.hoverIn(event, f, l))
		label.bind("<Enter>", lambda event, f=menuFrame, l=label: self.hoverIn(event, f, l))

		#I don't want to hover in event to persist once the mouse leaves
		menuFrame.bind("<Leave>", lambda event, f=menuFrame, l=label: self.hoverOut(event, f, l))
		label.bind("<Leave>", lambda event, f=menuFrame, l=label: self.hoverOut(event, f, l))

		#this is the event bind that will change the tool being used
		menuFrame.bind("<Button-1>", lambda event, f=menuFrame, l=label: self.changeTool(event, f, l))
		label.bind("<Button-1>", lambda event, f=menuFrame, l=label: self.changeTool(event, f, l))

		y+=30
		
		indSection = Frame(self.__menuBar, bg="#ff2e2e")
		indSection.place(x=0, y=y, width=150, height=40)

		exitLabel = Label(indSection, bg="#ff2e2e", text="INDIRECT")
		exitLabel.place(x=10, y=0, height=40)

		y+=40

		for t in range(5, 7):
			color = "#222222"
			if t == current:
				color = "#444444"
			#This is the menu option panel
			menuFrame = Frame(self.__menuBar, bg=color, width=150, height=30)
			menuFrame.place(x=0, y=y)

			#this is the menu label
			label = Label(menuFrame, fg="#ffffff", text=self.__tags[t], bg=color)
			label.place(x=10, y=0, height=25)

			#save the created frames and labels here
			self.__frames.append(menuFrame)
			self.__labels.append(label)

			#bind a hover in event for when the mouse enters the menu item
			menuFrame.bind("<Enter>", lambda event, f=menuFrame, l=label: self.hoverIn(event, f, l))
			label.bind("<Enter>", lambda event, f=menuFrame, l=label: self.hoverIn(event, f, l))

			#I don't want to hover in event to persist once the mouse leaves
			menuFrame.bind("<Leave>", lambda event, f=menuFrame, l=label: self.hoverOut(event, f, l))
			label.bind("<Leave>", lambda event, f=menuFrame, l=label: self.hoverOut(event, f, l))

			#this is the event bind that will change the tool being used
			menuFrame.bind("<Button-1>", lambda event, f=menuFrame, l=label: self.changeTool(event, f, l))
			label.bind("<Button-1>", lambda event, f=menuFrame, l=label: self.changeTool(event, f, l))

			#this is the menu tag position
			y+=30

		color = "#ff2e2e"
		settingsAndOtherToolsFrame = Frame(self.__menuBar, bg=color, width=150, height=30)
		settingsAndOtherToolsFrame.place(x=0, y=y)

		settingsLabel = Label(settingsAndOtherToolsFrame, fg="#ffffff", text="Settings", bg=color)
		settingsLabel.place(x=10, y=0, height=25)

		settingsAndOtherToolsFrame.bind("<Button-1>", lambda event, f=settingsAndOtherToolsFrame, l=settingsLabel: self.changeTool(event, f, l))
		settingsLabel.bind("<Button-1>", lambda event, f=settingsAndOtherToolsFrame, l=settingsLabel: self.changeTool(event, f, l))

		canvas = Canvas(settingsAndOtherToolsFrame, width=30, height=30, bg="#ff2e2e", highlightthickness=0)
		canvas.place(x=120, y=0)
		button = canvas.create_image((5, 5), anchor=NW, image=self.__photo)
		canvas.tag_bind(button, "<Button-1>", lambda event, f=settingsAndOtherToolsFrame, l=settingsLabel: self.changeTool(event, f, l))
		#canvas.tag_bind(button, "<Button-1>", lambda event, f=settingsAndOtherToolsFrame, l=settingsLabel: self.changeTool(event, f, l))
		#print(photo)



		

