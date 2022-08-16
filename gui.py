"""from guiClass import Application

app = Application()

#app.placeTerminal()

app.makeTitle()

app.placeBodyFrames()

app.placeMenu()

app.display()"""

from encapsulated.guiClass import Application
import os
import subprocess

p = subprocess.Popen(["python -m pip list --format=freeze"], shell=True, stdout=subprocess.PIPE)
out, err = p.communicate()
p.kill()

"""
For start up [First time]
--Check List
--numpy
--pandas
--textract
--tkinter
--pickle

--Also, some of the google suite

[Any Other Time]
--Ask if they want to update python
"""

#[numpy, pandas, textract, tkinter, pickle]
installed = [0, 0, 0, 0, 0]
modules = out.decode().split("\n")
for m in modules:
	if m.split("==")[0] == "numpy":
		installed[0] = 1
	elif m.split("==")[0] == "pandas":
		installed[1] = 1
	elif m.split("==")[0] == "textract":
		installed[2] = 1
	elif m.split("==")[0] == "tk":
		installed[3] = 1
	elif m.split("==")[0] == "pickleshare":
		installed[4] = 1

print(installed)

app = Application()

#this will make the titlebar, which holds the settings, 
#and informs the user what tool is being used
app.makeTitle()

app.createBody()

app.placeMenu()

app.display()