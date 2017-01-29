#!/usr/bin/python3

import json
import os
import sys

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import widgets
import furnature

def canvas_get(canvas, x, y):
	things = canvas.find_overlapping(x, y, x+1, y+1)	# Returns a tuple of the IDs of all the objects at the given pixel

	if things != ():
		return things[-1]

class Classroom(Frame):
	def __init__(self, root, closefunct=None):
		super(Classroom, self).__init__(root)	# Initialise the superclass

		# Create instance variables
		self.contents = {}				# The dictionary with the tkinter representations of the table
		self.pupils   = {}

		self.__dnd_id = None	# The ID of the object we're dragging and dropping
		self.__dnd_start_x = None
		self.__dnd_start_y = None

		# Create the canvas

		def rclick_menu(event):
			menu = Menu(self, tearoff=0)

			def delete_table(x, y):
				table = canvas_get(self.canvas, event.x, event.y)
				self.canvas.delete(table)

			menu.add_command(label="Add table", command=lambda: self.add_table(x=event.x, y=event.y))
			menu.add_command(label="Add chair", command=lambda: self.add_chair(x=event.x, y=event.y))
			menu.add_command(label="Delete",    command=lambda: delete_table(event.x, event.y))

			menu.tk_popup(event.x_root, event.y_root)		# _root => x and y of it in the whole roow window
			menu.grab_release()		# Else it wouldn't close until you clicked one of its buttons.

		def dnd_bdown(event):
			# Temporarily store the positions
			self.__dnd_id = canvas_get(self.canvas, event.x, event.y)
			self.__dnd_start_x = event.x
			self.__dnd_start_y = event.y

		def dnd_bup(event):
			if self.__dnd_id:
				mv_object = self.contents[self.__dnd_id]
				self.canvas.move(self.__dnd_id, event.x-self.__dnd_start_x, event.y-self.__dnd_start_y)		# .move doesn't want to know to WHERE it moves, it wants to know how much it should move BY.
				mv_object.x = self.canvas.coords(self.__dnd_id)[0]		# Canvas.coords() returns: [tl_x, tl_y, br_x, br_y]
				mv_object.y = self.canvas.coords(self.__dnd_id)[1]

				self.__dnd_id = None
				self.__dnd_start_x = None
				self.__dnd_start_y = None

		self.canvas = Canvas(self, width=800, height=600, bg="#ffffff", borderwidth=1, relief=SUNKEN)
		self.canvas.grid(column=0, row=0, padx=5, pady=5)

		self.canvas.bind("<Button-1>", dnd_bdown)
		self.canvas.bind("<ButtonRelease-1>", dnd_bup)
		self.canvas.bind("<Button-3>", rclick_menu)

		# The frame of controls below the classroom
		self.ctrlframe = Frame(self)
		self.ctrlframe.grid(column=0, row=1, padx=5, pady=5, sticky=W)

		self.closeButton = Button(self.ctrlframe, text="Close", command=self.destroy)
		self.closeButton.grid(column=0, row=0, padx=10)

		self.nameBox = Entry(self.ctrlframe)
		self.nameBox.grid(column=1, row=0, padx=10)

	## Other methods ##

	def add_table(self, x=0, y=0):
		# What to do when the 'Add Table' button is pressed

		dialog = Toplevel(master=self.canvas)
		dialog.title("Table properties")

		widthLabel = Label(dialog, text="Width (cm):")
		widthEntry = widgets.NumEntry(dialog, default=200, step=5, min_val=50, max_val=500)
		widthLabel.grid(column=0, row=0, padx=10, pady=10)
		widthEntry.grid(column=1, row=0, padx=10, pady=10)

		heightLabel = Label(dialog, text="Length (cm):")
		heightEntry = widgets.NumEntry(dialog, default=120, step=5, min_val=50, max_val=500)
		heightLabel.grid(column=0, row=1, padx=10, pady=10)
		heightEntry.grid(column=1, row=1, padx=10, pady=10)

		def ok(*args):
			table = furnature.Table(int(widthEntry.get()), int(heightEntry.get()), x=x, y=y)
			self.contents[table.draw(self.canvas)] = table
			dialog.destroy()

		def cancel(*args):
			dialog.destroy()

		buttonFrame  = Frame(dialog)
		buttonFrame.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
		okButton     = Button(buttonFrame, text="Ok", command=ok)
		cancelButton = Button(buttonFrame, text="Cancel", command=cancel)
		okButton.grid(column=1, row=0, padx=10)
		cancelButton.grid(column=0, row=0, padx=10)

		dialog.bind("<Return>", ok)

	def add_chair(self, x=0, y=0):
		chair = furnature.Chair(x=x, y=y)
		self.contents[chair.draw(self.canvas)] = chair

	def rename(self, name):
		self.nameBox.delete(0, END)
		self.nameBox.insert(0, name)

	def reset(self):
		self.canvas.delete(ALL)
		self.nameBox.delete(0, END)
		self.contents = {}

	def load(self, loc=None):
		self.reset()

		# Load the classroom data from a file
		if loc:
			with open(loc, "r") as f:
				data = json.load(f)
				self.nameBox.insert(0, data["name"])

				for thing in data["contents"]:
					if thing["__type"] == "Table":
						table = furnature.Table()
						table.width = thing["width"]
						table.height = thing["height"]
						table.x = thing["x"]
						table.y = thing["y"]

						self.contents[table.draw(self.canvas)] = table
					if thing["__type"] == "Chair":
						chair = furnature.Chair()
						chair.x = thing["x"]
						chair.y = thing["y"]

						self.contents[chair.draw(self.canvas)] = chair

	def save(self, loc=None):
		# Save the classroom to JSON file
		if loc:
			with open(loc, 'w') as f:
				out = 	{																			\
							"name" : (self.nameBox.get() if self.nameBox.get() != "" else loc.split(os.sep)[-1]),		\
							"contents" : [content.__repr__() for content in self.contents.values()]	\
						}

				json.dump(out, f)

class SeatingPlan():
	def __init__(self, files=[]):
		self.root = Tk()
		self.root.title("Seating Plan")

		# Create the menus

		def open_classroom():
			loc = filedialog.askopenfilename(title="Load classroom layout", filetypes=[('JSON files','*.json'), ('All files','*.*')])
			if loc:
				self.load_classroom(loc)
		def save_classroom():
			loc = filedialog.asksaveasfilename(title="Save classroom layout", filetypes=[('JSON files','*.json'), ('All files','*.*')])
			if loc:
				self.current_classroom().save(loc=loc)

		self.menubar  = Menu(self.root)
		self.root.config(menu=self.menubar)

		self.filemenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade (label="File", menu=self.filemenu)
		self.filemenu.add_command(label="New", command=self.new_classroom)
		self.filemenu.add_command(label="Open", command=open_classroom)
		self.filemenu.add_command(label="Save As", command=save_classroom)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Quit", command=self.root.destroy)

		## The notebook with classrooms ##

		self.tabs = ttk.Notebook(self.root)
		self.tabs.enable_traversal()						# Enable ctrl-tab and ctrl-shift-tab
		self.tabs.grid(column=0, row=0, padx=10, pady=10)

		self.classrooms = []

		if files == []:
			self.new_classroom()

		## The frame with buttons ##
		self.ctrlframe = Frame(self.root, relief=RAISED, borderwidth=1)
		self.ctrlframe.grid(column=1, row=0, padx=10, pady=10, sticky=N+S)

		def updateName():
			self.current_classroom().name = self.nameBox.get()

		self.addTableButton = Button(self.ctrlframe, text="New Table", command=lambda: self.current_classroom().add_table())
		self.addTableButton.grid(column=0, row=1, padx=10, pady=10)
		self.addChairButton = Button(self.ctrlframe, text="New Chair", command=lambda: self.current_classroom().add_chair())
		self.addChairButton.grid(column=1, row=1, padx=10, pady=10)

		# Load files if any were given
		for loc in files:
			self.load_classroom(loc)

		self.root.mainloop()

	def new_classroom(self):
		classroom = Classroom(self.root)
		self.classrooms.append(classroom)
		self.tabs.add(classroom, text="New classroom")

	def load_classroom(self, loc):
		classroom = Classroom(self.root)
		classroom.load(loc)
		self.classrooms.append(classroom)
		self.tabs.add(classroom, text=classroom.nameBox.get())

	def current_classroom(self):
		return self.classrooms[self.tabs.index("current")]

if __name__ == '__main__':
	SeatingPlan(files=sys.argv[1:])

	#import pdb; pdb.set_trace()
