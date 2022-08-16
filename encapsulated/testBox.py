from tkinter import *
from tkinter import Text
import subprocess

class LiveTerminal:

	__parent = None
	__terminal = None
	__lineNum = 1
	__process = None
	__saveToList = False
	__remainingOutput = list()

	def runProcess(self, file, args):
		command = "python3 " + file + " " + args
		process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
		self.__process = process
		while True:
			line = process.stdout.readline()
			stng = line.decode("utf-8")

			if not line:
				break

			self.__terminal.insert(str(float(self.__lineNum)), "+" + stng.strip() + "\n")
			self.__terminal.see("insert")
			self.__parent.update_idletasks()
			self.__lineNum += 1

	def __init__(self, root):
		self.__terminal = Text(root, bg="#ffffff", fg="#000000", height=8, highlightthickness=0, cursor="arrow", wrap=WORD)
		self.__terminal.bind("<Key>", lambda event: "break")
		self.__terminal.place(x=0, y=255, width=350)
		self.__parent = root

	def enterLine(self, string):
		self.__terminal.insert(str(float(self.__lineNum)), "+" + string + "\n")
		self.__terminal.see("insert")
		self.__lineNum += 1

	def keystroke(self, e, line):
		print(line)
		if e.keysym == "BackSpace":
			if self.__terminal.index(INSERT) == str(line-1) + ".2":
				return "break"
		elif e.keysym == "Return":
			retVal = self.__terminal.get(str(float(line-1)), END).strip()
			retVal = retVal[2:] + "\n"
			
	def randomButtons(self):
		button = Button(self.__parent, text="Press me", command=self.testProcess)
		button.place(x=180, y=150)

		delete = Button(self.__parent, text="Delete line", command=self.deleteLine)
		delete.place(x=180, y=190)

	def destroy(self):
		self.__terminal.destroy()

	def idle_task(self):
		self.__terminal.update_idletasks()