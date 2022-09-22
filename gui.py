from encapsulated.guiClass import Application
import os


app = Application()

#this will make the titlebar, which holds the settings, 
#and informs the user what tool is being used
app.makeTitle()

#this is the body of the application
app.createBody()

#this is the tool menu of the application
app.placeMenu()

#this will start the tkinter mainloop
app.display()