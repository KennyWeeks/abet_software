from encapsulated.guiClass import Application
import os


app = Application()

#this will make the titlebar, which holds the settings, 
#and informs the user what tool is being used
 
app.makeTitle()

"""app.createBody()"""

app.placeMenu()

app.display()