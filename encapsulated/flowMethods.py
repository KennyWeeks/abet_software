
#These are flow methods that allow certain parts of the software to
#activate
class FlowMethods:

	"""def get_file_path(self):
		if getattr(sys, 'frozen', False):
			path = sys._MEIPASS
		else:
			path = "."

		return path"""

	def getFile(self, name, i, frame, bf, cv, dp):
		"""
		-Parameter Desc
		-self --> the class instance
		-name --> name of label to list final file
		-i --> key used to save the file to __filenames dictionary
		-frame --> where the headers are placed if the file is an .xlsx or .csv
		-bf --> bodyframe of the available data
		-cv --> canvas that displays application
		-dp --> drop down frame
		-check --> get the checkboxes
		"""

		filename = fd.askopenfilename() #ask the user for the file
		if len(filename) == 0:
			self.deleteChildren(True, bf, name, frame, cv)
			self.__checkBoxes[name] = dict() #reset the dictionary
			self.__filenames[i] = "" #even if nothing is provided, I want the dictionary to start getting filed
		else:
			#this is if there is no file selected, add the label so the user can see there file selected
			splitText = os.path.splitext(filename)
			print(splitText[1])
			if splitText[1] != ".xlsx" and splitText[1] != ".csv":
				self.__terminal.enterLine("File needs to be .xlsx or .csv")
				return

			#this will run if everything works
			pos = [m.start() for m in re.finditer("/", filename)]
			file = filename[pos[-1]+1:]
			for c in bf.winfo_children():
				if str(type(c)) == "<class 'tkinter.Label'>":
					if str(c).find(name) != -1:
						c.config(text="+-----------> " + file)
			self.__root.focus_set()
			self.__filenames[str(i)] = filename #save the file name
			
			#if I need to list headers, i will, otherwise, no frame is provided
			if frame != None:
				self.getHeaderOfFiles(filename, frame, bf, cv, name, dp)

	def deleteChildren(self, empty, parent, name, frame, cv):
		"""
		Parameter description
		parent --> this is the body object that needs to have things deleted from it
		name --> this is the name of the specific child that will have it's contents deleted
		frame --> this will mostly be used for deleting headers and the checkboxes associated with them generated by the app
		cv --> this is associated with the frame, if provided, we need to resize the canvas
		"""
		for c in parent.winfo_children():
			if str(type(c)) == "<class 'tkinter.Label'>":
				if str(c).find(name) != -1 and empty:
					c.config(text="+-----------> No File Selected") #clear this specific label

				#remove frame children
				if frame != None:
					for frC in frame.winfo_children():
						frC.grid_forget()

						cv.update_idletasks()
						cv.configure(scrollregion=parent.bbox("all"))

					frame.config(height=0) #set everything back to 0
					cv.update_idletasks()
					cv.configure(scrollregion=parent.bbox("all"))

					if empty:
						noCheckBox = Label(frame, text="+-----------> No Headers Available", bg="#323232", fg="#ffffff")
						noCheckBox.grid(sticky=W, row=0, column=0)

						cv.update_idletasks()
						cv.configure(scrollregion=parent.bbox("all"))
