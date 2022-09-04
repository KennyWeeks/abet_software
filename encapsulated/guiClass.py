from tkinter import *
from tkinter import Text
from tkinter import filedialog as fd
#from PIL import Image, ImageTk, ImageDraw
import re
"""from encapsulated.menuBar import MenuBar
from encapsulated.bodyFrames import BodyFrame
import sys
from encapsulated.imageClass import TitleButtons"""
"""from menuBar import Menu
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

	#__test = TitleButtons("imgs/gears.png", (20, 20)).makePhoto()

	#--------------------------------
	#these are the methods that will be called by the class during creation
	def __init__(self):
		self.__root.geometry("500x400") #declare the geometry for the application
		self.__root.title("")
		self.__root.config(bg="#323232")
		self.__root.resizable(0, 0)
		#photo = PhotoImage(file="imgs/logo_3.png")
		#self.__root.iconphoto(False, photo)

		mn = Menu(self.__root)
		self.__root.config(menu=mn)

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
		menu = MenuBar(self.__root, self.__frame, self.__currentLabel, None) #initialize the block holding the menu

		menu.items(self.__current) #but the menu options into that block

	#def displaySettings(self):
	#	self.__settings = SettingsPage(self.__root)

	def display(self):
		self.__root.mainloop() #display the application
