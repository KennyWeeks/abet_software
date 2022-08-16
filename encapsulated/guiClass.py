from tkinter import *
from tkinter import Text
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw
import re
from encapsulated.menuBar import Menu
from encapsulated.bodyFrames import BodyFrame
"""from imageClass import TitleButtons
from menuBar import Menu
from testBox import LiveTerminal
from bodyFrames import BodyFrame"""

class Application:

	#this is the main root
	__root = Tk() #I want to this be private, so only the class can access it

	#this is the body frame that will interface with the tools, I need to save this for later changes
	__frame = None

	#This is the current tool set being used. the tool set is for the specific part of the abet (Direct Assessment, Exit Interview, Indirect Assessment)
	__currentLabel = None

	#this is the current tool being worked with
	__current = 0

	#__settings = None

	#these are some of the variables that will be used
	#this is specifically the photos for the minimize and close buttons
	#the reason they need to be variables is because they lose their scope
	#if they are not present as a variable in the class.

	#close button
	#__closePhoto = TitleButtons("close.png", (15, 15)).makePhoto()

	#minimize button
	#__miniPhoto = TitleButtons("mini.png", (15, 15)).makePhoto()

	#--------------------------------
	#These will be functions that are called by different objects on the application
	"""def saveOff(self, e, x):
					e.widget.offset = (e.x + x, e.y)
			
				def moveApp(self, e):
					self.__root.geometry(f'+{e.x_root-e.widget.offset[0]}+{e.y_root-e.widget.offset[1]}')
			
				def close(self, e):
					self.__root.quit()
			
				def mini(self, e):
					self.__root.update_idletasks()
					self.__root.overrideredirect(False)
					self.__root.state("iconic")"""

	#--------------------------------
	#these are the methods that will be called by the class during creation
	def __init__(self):
		self.__root.geometry("500x400") #declare the geometry for the application
		self.__root.title("")
		self.__root.resizable(0, 0)
		#photo = PhotoImage(file="imgs/logo.png")
		#self.__root.iconphoto(False, photo)

	def makeTitle(self):
		#this bar will hold the settings button, as well as what tool is 
		#currently in use
		titleBar = Frame(self.__root, bg="#323232")
		titleBar.place(x=0, y=0, width=500, height=40)

		#----------------------
		#This is the title background frame
		#-- this frame will hold the title of the application
		#----------------------
		titleFrame = Frame(titleBar, bg="#ff0000")
		titleFrame.place(x=0, y=0, width=150, height=40)

		#----------------------
		#This is the title label
		#----------------------
		titleLabel = Label(titleBar, bg="#ff0000", fg="#ffffff", text="ABET TOOLS")
		titleLabel.place(x=10, y=0, height=40)

		#----------------------
		#This is the current tool set
		#----------------------
		currentLabel = Label(titleBar, bg="#323232", fg="#ffffff", text="DIRECT ASSESSMENT")
		currentLabel.place(x=160, y=0, height=40)

		self.__currentLabel = currentLabel #this is for visuals

		#settingsBut = Button(titleBar, text="settings", command=lambda: self.__settings.openSettings())
		#settingsBut.place(x=400, y=6)

	def createBody(self):
		#this creates the body frame that will be displayed.
		self.__frame = BodyFrame(self.__root, self.__current)

	def placeMenu(self):
		menu = Menu(self.__root, self.__frame, self.__currentLabel) #initialize the block holding the menu

		menu.items(self.__current) #but the menu options into that block

	#def displaySettings(self):
	#	self.__settings = SettingsPage(self.__root)

	def display(self):
		self.__root.mainloop() #display the application
