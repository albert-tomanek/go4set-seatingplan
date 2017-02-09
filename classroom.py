#!/usr/bin/python3

import json
import csv
import os
import sys

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from pupil import Pupil
import widgets
import furnature

ABOUT_TEXT = """\
SeatingPlan was written for Go4Set 2017
in Python by Albert Tomanek.
Special thanks to my team members:
 - Ryan Irving
 - Sam Kelly
 - Kirill Kapista
 - Oscar Sparrowhawk
 - Maya Vasut
And our mentor:
 - Luke
"""

def canvas_get(canvas, x, y):
	#import pdb; pdb.set_trace()

	things = canvas.find_overlapping(x, y, x+1, y+1)	# Returns a tuple of the IDs of all the objects at the given pixel

	if things != ():
		if canvas.type(things[-1]) == "text":
			return canvas.gettags(things[-2])[0]
		else:
			return canvas.gettags(things[-1])[0]	# There'll only ever be one thing per tag anyway

class Classroom(Frame):
	def __init__(self, root, closefunct=None):
		super(Classroom, self).__init__(root)	# Initialise the superclass

		# Create instance variables
		self.closefunct = closefunct
		self.contents   = {}				# The dictionary with the tables' IDs and their classes.
		self.pupils     = {}

		self.dnd_tag = None	# The ID of the object we're dragging and dropping
		self.dnd_object  = None
		self.dnd_start_x = None
		self.dnd_start_y = None

		# Create the canvas

		def rclick_menu(event):
			thing = canvas_get(self.canvas, event.x, event.y)
			menu  = Menu(self, tearoff=0)

			def delete_thing(x, y):
				thing_tag = canvas_get(self.canvas, event.x, event.y)
				self.remove(thing_tag)

			def rename_table(x, y):
				table = self.contents[canvas_get(self.canvas, event.x, event.y)]

				dialog = Toplevel(master=self.canvas)
				dialog.title("Rename Table")

				nameLabel = Label(dialog, text="Name:")
				nameEntry = Entry(dialog)
				nameLabel.grid(column=0, row=0, padx=10, pady=10, sticky=W)
				nameEntry.grid(column=1, row=0, padx=10, pady=10, sticky=W)

				nameEntry.insert(0, table.name)

				def ok(*args):
					table.name = nameEntry.get()
					table.draw_name(self.canvas)

					dialog.destroy()

				def cancel(*args):
					diaPlog.destroy()

				buttonFrame  = Frame(dialog)
				buttonFrame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
				okButton     = Button(buttonFrame, text="Ok", command=ok)
				cancelButton = Button(buttonFrame, text="Cancel", command=cancel)
				okButton.grid(column=1, row=0, padx=10)
				cancelButton.grid(column=0, row=0, padx=10)

				dialog.bind("<Return>", ok)

			menu.add_command(label="Add table", command=lambda: self.add_table(x=event.x, y=event.y))
			menu.add_command(label="Add chair", command=lambda: self.add_chair(x=event.x, y=event.y))

			if thing:
				if type(self.things()[thing]) == furnature.Table:
					menu.add_separator()
					menu.add_command(label="Rename", command=lambda: rename_table(event.x, event.y))

				if type(self.things()[thing]) != Pupil:
					menu.add_separator()
					menu.add_command(label="Delete", command=lambda: delete_thing(event.x, event.y))

			menu.tk_popup(event.x_root, event.y_root)		# _root => x and y of it in the whole roow window
			menu.grab_release()		# Else it wouldn't close until you clicked one of its buttons.

		def dnd_bdown(event):
			# Temporarily store the positions
			self.dnd_tag = canvas_get(self.canvas, event.x, event.y)

			if self.dnd_tag:
				self.dnd_object = self.things()[self.dnd_tag]		# It may be either a piece of furnature, or a pupil representation
				self.dnd_start_x = event.x
				self.dnd_start_y = event.y

		def dnd_move(event):
			# If we're *actually dragging sth*
			if self.dnd_tag:
				chair = self.chair_at(event.x, event.y)

				if type(self.dnd_object) == Pupil and chair != None:
					# If we're dragging a pupil and there's a chair under it...

					pupil = self.dnd_object

					move_x = (chair.x + chair.width / 2)  - (pupil.x + pupil.width / 2)
					move_y = (chair.y + chair.height / 2) - (pupil.y + pupil.height / 2)

					# Move the pupil to the middle of the chair
					self.canvas.move(self.dnd_tag, move_x, move_y)		# .move doesn't want to know to WHERE it moves, it wants to know how much it should move BY.
					self.canvas.move(self.dnd_object.name_text_id, move_x, move_y)	# Move the text too

					chair.pupil_tag = pupil.tag
				elif chair == None and self.chair_at(self.dnd_start_x, self.dnd_start_y) != None:
					# Here we put the code that removes a pupil from a chair

					self.chair_at(self.dnd_start_x, self.dnd_start_y).pupil_tag = None
				else:
					# If the object we're dragging isn't a pupil and there isn't a chair under us...

					# Move the object
					self.canvas.move(self.dnd_tag, event.x-self.dnd_start_x, event.y-self.dnd_start_y)		# .move doesn't want to know to WHERE it moves, it wants to know how much it should move BY.

					# Move the text if it is a table or pupil
					if type(self.dnd_object) == furnature.Table or type(self.dnd_object) == Pupil:
						self.canvas.move(self.dnd_object.name_text_id, event.x-self.dnd_start_x, event.y-self.dnd_start_y)	# Move the text too

				# update the object's x and y
				self.dnd_object.x = self.canvas.coords(self.dnd_tag)[0]		# Canvas.coords() returns: [tl_x, tl_y, br_x, br_y]
				self.dnd_object.y = self.canvas.coords(self.dnd_tag)[1]

				# Update the start X and Y
				self.dnd_start_x = event.x
				self.dnd_start_y = event.y

		def dnd_bup(event):
			if self.dnd_tag:
				self.dnd_tag = None
				self.dnd_object  = None
				self.dnd_start_x = None
				self.dnd_start_y = None

		self.canvas = Canvas(self, width=800, height=600, bg="#ffffff", borderwidth=1, relief=SUNKEN)
		self.canvas.grid(column=0, row=0, padx=5, pady=5)

		self.canvas.bind("<Button-1>", dnd_bdown)
		self.canvas.bind("<B1-Motion>", dnd_move)
		self.canvas.bind("<ButtonRelease-1>", dnd_bup)
		self.canvas.bind("<Button-3>", rclick_menu)

		# The frame of controls below the classroom
		self.ctrlframe = Frame(self)
		self.ctrlframe.grid(column=0, row=1, padx=5, pady=5, sticky=W)

		self.closeButton = Button(self.ctrlframe, text="Close", command=self.close)
		self.closeButton.grid(column=0, row=0, padx=10)

		self.nameLabel = Label(self.ctrlframe, text="Classroom Name:")
		self.nameLabel.grid(column=1, row=0, padx=10, sticky=E)
		self.nameBox = Entry(self.ctrlframe)
		self.nameBox.grid(column=2, row=0, padx=10)

	## Other methods ##

	def things(self):
		return {**self.contents, **self.pupils}
	def chairs(self):
		return [thing for thing in self.contents if type(thing) == objects.Chair]

	def objects_at(self, x, y):
		# Returns a list of objects at the given pixel

		# This is a list of tags/IDs. Each thing in the classroom will only ever have ONE tag
		things = []
		for num_id in self.canvas.find_overlapping(x, y, x+1, y+1):
			if self.canvas.gettags(num_id):
				things.append(self.canvas.gettags(num_id)[0])

		ret    = []

		for thing in things:
			if self.canvas.type(thing[0]) != "text" and thing in self.contents.keys():
				ret.append(thing)
		return ret

	def chair_at(self, x, y):
		# Returns a chair if there is one beneath the cursor
		if self.objects_at(x, y) != None:

			# Get us a list of all the chairs we are above
			underlying_chairs = [self.contents[thing] for thing in self.objects_at(x, y) if type(self.contents[thing]) == furnature.Chair]

			if underlying_chairs:
				return underlying_chairs[0]
			else:
				return None
		else:
			return None

	def add_table(self, x=0, y=0):
		# What to do when the 'Add Table' button is pressed

		dialog = Toplevel(master=self.canvas)
		dialog.title("Table properties")

		widthLabel = Label(dialog, text="Width (cm):")
		widthEntry = widgets.NumEntry(dialog, default=200, step=5, min_val=50, max_val=500)
		widthLabel.grid(column=0, row=0, padx=10, pady=10, sticky=W)
		widthEntry.grid(column=1, row=0, padx=10, pady=10, sticky=W)

		heightLabel = Label(dialog, text="Length (cm):")
		heightEntry = widgets.NumEntry(dialog, default=120, step=5, min_val=50, max_val=500)
		heightLabel.grid(column=0, row=1, padx=10, pady=10, sticky=W)
		heightEntry.grid(column=1, row=1, padx=10, pady=10, sticky=W)

		nameLabel = Label(dialog, text="Name:")
		nameEntry = Entry(dialog)
		nameLabel.grid(column=0, row=2, padx=10, pady=10, sticky=W)
		nameEntry.grid(column=1, row=2, padx=10, pady=10, sticky=W)

		def ok(*args):
			table = furnature.Table(self.new_tag(), name=nameEntry.get(), width=int(widthEntry.get()), height=int(heightEntry.get()), x=x, y=y)
			table.draw(self.canvas)
			self.contents[table.tag] = table
			dialog.destroy()

		def cancel(*args):
			dialog.destroy()

		buttonFrame  = Frame(dialog)
		buttonFrame.grid(column=0, row=3, columnspan=2, padx=10, pady=10)
		okButton     = Button(buttonFrame, text="Ok", command=ok)
		cancelButton = Button(buttonFrame, text="Cancel", command=cancel)
		okButton.grid(column=1, row=0, padx=10)
		cancelButton.grid(column=0, row=0, padx=10)

		dialog.bind("<Return>", ok)

	def add_chair(self, x=0, y=0):
		chair = furnature.Chair(self.new_tag(), x=x, y=y)
		chair.draw(self.canvas)
		self.contents[chair.tag] = chair

	def add_pupil(self, after=None):
		# What to do when the 'Add Table' button is pressed

		dialog = Toplevel(master=self.canvas)
		dialog.title("Add Pupil")

		nameLabel = Label(dialog, text="Name:")
		nameEntry = Entry(dialog)
		nameLabel.grid(column=0, row=0, padx=10, pady=10, sticky=W)
		nameEntry.grid(column=1, row=0, padx=10, pady=10, sticky=W)

		def ok(*args):
			pupil = Pupil(self.new_pupil_tag(), name=nameEntry.get())
			self.pupils[pupil.tag] = pupil
			dialog.destroy()

			pupil.draw(self.canvas)

			if after:
				after()

		def cancel(*args):
			dialog.destroy()

		buttonFrame  = Frame(dialog)
		buttonFrame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
		okButton     = Button(buttonFrame, text="Ok", command=ok)
		cancelButton = Button(buttonFrame, text="Cancel", command=cancel)
		okButton.grid(column=1, row=0, padx=10)
		cancelButton.grid(column=0, row=0, padx=10)

		dialog.bind("<Return>", ok)

	def remove(self, tag):
		rm_thing = self.contents[tag]

		if type(rm_thing) == furnature.Table:
			# Remove the title if it's a table
			self.canvas.delete(rm_thing.name_text_id)

		self.canvas.delete(tag)
		self.contents.pop(tag)		# Not the best way, but oh well...

	def new_tag(self):
		i = 1
		tag = ""

		while True:
			tag = "OBJECT_" + str(i)

			if tag not in self.contents.keys():
				return tag
			else:
				i += 1

	def new_pupil_tag(self):
		i = 1
		tag = ""

		while True:
			tag = "PUPIL_" + str(i)

			if tag not in self.pupils.keys():
				return tag
			else:
				i += 1

	def rename(self, name):
		self.nameBox.delete(0, END)
		self.nameBox.insert(0, name)

	def reset(self):
		self.canvas.delete(ALL)
		self.nameBox.delete(0, END)
		self.contents = {}
		self.pupils   = {}

	def load(self, loc=None):
		self.reset()

		# Load the classroom data from a file
		if loc:
			with open(loc, "r") as f:
				data = json.load(f)
				self.nameBox.insert(0, data["name"])

				# Load the classroom's contents
				for furnature_node in data["contents"]:
					if furnature_node["__type"] == "Table":
						table = furnature.Table(furnature_node["__tag"])
						table.name  = furnature_node["name"]
						table.width = furnature_node["width"]
						table.height = furnature_node["height"]
						table.x = furnature_node["x"]
						table.y = furnature_node["y"]

						table.draw(self.canvas)

						self.contents[furnature_node["__tag"]] = table
					if furnature_node["__type"] == "Chair":

						chair = furnature.Chair(furnature_node["__tag"])
						chair.x = furnature_node["x"]
						chair.y = furnature_node["y"]
						chair.pupil_tag = furnature_node["pupil"]

						chair.draw(self.canvas)

						self.contents[furnature_node["__tag"]] = chair

						pupil_node = next((pupil_node for pupil_node in data["pupils"] if pupil_node["__tag"] == chair.pupil_tag), None)	# Get the pupil with the chair's tag if one exists, else return None.

						# Put a pupil on the chair if there is one
						if pupil_node:
							pupil = Pupil(pupil_node["__tag"])
							pupil.name = pupil_node["name"]
							pupil.present = pupil_node["present"]

							self.pupils[pupil.tag] = pupil

							# Calculate where to draw the pupil
							pupil.x = (chair.x + chair.width / 2)  - (pupil.width / 2)
							pupil.y = (chair.y + chair.height / 2) - (pupil.height / 2)

							pupil.draw(self.canvas)

	def save(self, loc=None):
		# Save the classroom to JSON file
		if loc:
			with open(loc, 'w') as f:
				out = 	{
							"name"     : (self.nameBox.get() if self.nameBox.get() != "" else loc.split(os.sep)[-1]),
							"contents" : [content.json() for content in self.contents.values()],
							"pupils"   : [pupil.json() for pupil in self.pupils.values()]
						}

				json.dump(out, f)

				if self.nameBox.get() == "":
					self.nameBox.delete(0, END)
					self.nameBox.insert(0, loc.split(os.sep)[-1])

	def export_presence(self, loc):
		with open(loc, "w") as f:
			writer = csv.writer(f)
			writer.writerow( ("Name", "Present") )

			for pupil in self.pupils.values():
				writer.writerow( (pupil.name, str(int(pupil.present))) )

	def close(self):
		if self.closefunct:
			self.closefunct()
		self.destroy()

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
		def export_presence():
			loc = filedialog.asksaveasfilename(title="Export pupil presence", filetypes=[('CSV files','*.csv'), ('All files','*.*')])
			if loc:
				self.current_classroom().export_presence(loc=loc)

		self.menubar  = Menu(self.root)
		self.root.config(menu=self.menubar)

		self.filemenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade (label="File", menu=self.filemenu)
		self.filemenu.add_command(label="New", command=self.new_classroom)
		self.filemenu.add_command(label="Open", command=open_classroom)
		self.filemenu.add_command(label="Save As", command=save_classroom)
		self.filemenu.add_command(label="Export Presence", command=export_presence)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Quit", command=self.root.destroy)

		self.helpmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade (label="Help", menu=self.helpmenu)
		self.helpmenu.add_command(label="About", command=lambda: widgets.TextLoadWindow(self.root, text=ABOUT_TEXT, title="About"))

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

		self.pupilsFrame = LabelFrame(self.ctrlframe, text="Pupils")
		self.pupilsFrame.grid(column=0, row=2, padx=5, pady=5, columnspan=2, sticky=S)

		self.addPupilButton = Button(self.pupilsFrame, text="Add pupil", command=lambda: self.current_classroom().add_pupil(after=self.update_pupils))
		self.addPupilButton.grid(column=0, row=0, padx=5, pady=5, sticky=W)

		def togglePresent():
			for selected in self.pupilsTree.selection():
				pupil = self.current_classroom().pupils[selected]
				pupil.present = not pupil.present
			self.update_pupils (oldselecttags = self.pupilsTree.selection())

		self.togglePresentButton = Button(self.pupilsFrame, text="Toggle Presence", command=togglePresent)
		self.togglePresentButton.grid(column=1, row=0, padx=5, pady=5, sticky=W)

		self.pupilsTree = ttk.Treeview(self.pupilsFrame)
		self.pupilsTree.grid(column=0, row=1, padx=5, pady=5, columnspan=2)

		self.pupilsTree["columns"] = ("here")
		self.pupilsTree.column("here", width=50)	# This is just used for the API
		self.pupilsTree.heading("here", text="Here")

		# When an element is right-clicked
		def ptree_rclick_menu(event):
			pupil_tag = self.pupilsTree.identify_row(event.y)	# This actually returns the item's tag, and not its index

			if pupil_tag:
				pupil = self.current_classroom().pupils[pupil_tag]
				menu  = Menu(self.ctrlframe, tearoff=0)

				def renamePupil(pupil):
					dialog = Toplevel(master=self.current_classroom().canvas)
					dialog.title("Rename Pupil")

					nameLabel = Label(dialog, text="Name:")
					nameEntry = Entry(dialog)
					nameLabel.grid(column=0, row=0, padx=10, pady=10, sticky=W)
					nameEntry.grid(column=1, row=0, padx=10, pady=10, sticky=W)

					nameEntry.insert(0, pupil.name)

					def ok(*args):
						pupil.name = nameEntry.get()
						self.update_pupils()

						dialog.destroy()

					def cancel(*args):
						dialog.destroy()

					buttonFrame  = Frame(dialog)
					buttonFrame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
					okButton     = Button(buttonFrame, text="Ok", command=ok)
					cancelButton = Button(buttonFrame, text="Cancel", command=cancel)
					okButton.grid(column=1, row=0, padx=10)
					cancelButton.grid(column=0, row=0, padx=10)

					dialog.bind("<Return>", ok)
				def removePupil(pupil):
					self.current_classroom().pupils.pop(pupil_tag)
					self.update_pupils()

				menu.add_command(label="Rename", command=lambda: renamePupil(pupil))
				menu.add_command(label="Remove", command=lambda: removePupil(pupil))

				menu.tk_popup(event.x_root, event.y_root)		# _root => x and y of it in the whole roow window
				menu.grab_release()		# Else it wouldn't close until you clicked one of its buttons.

		self.pupilsTree.bind("<Button-3>", ptree_rclick_menu)

		# When the tab is changed...
		self.tabs.bind("<<NotebookTabChanged>>", lambda event: self.update_pupils())

		# Load files if any were given
		for loc in files:
			self.load_classroom(loc)

		self.root.mainloop()

	def update_pupils(self, oldselecttags=[]):
		# Clear the tree
		for pupil_tag in self.pupilsTree.get_children():
			self.pupilsTree.delete(pupil_tag)
			self.current_classroom().canvas.delete(pupil_tag)
			self.current_classroom().canvas.delete(pupil_tag + "_TEXT")

		classroom = self.current_classroom()

		for tag, pupil in classroom.pupils.items():
			self.pupilsTree.insert("", 0, iid=tag, text=pupil.name, values=("Yes" if pupil.present else "No"))
			pupil.draw(self.current_classroom().canvas)

			# Select the pupil if they were previously selected
			if tag in oldselecttags:
				self.pupilsTree.selection_add(tag)

	def new_classroom(self):
		classroom = Classroom(self.root, closefunct=lambda: self.classrooms.remove(classroom))
		self.classrooms.append(classroom)
		self.tabs.add(classroom, text="New classroom")

	def load_classroom(self, loc):
		classroom = Classroom(self.root, closefunct=lambda: self.classrooms.remove(classroom))
		classroom.load(loc)
		self.classrooms.append(classroom)
		self.tabs.add(classroom, text=classroom.nameBox.get())

	def current_classroom(self):
		return self.classrooms[self.tabs.index("current")]

if __name__ == '__main__':
	import traceback, sys, pdb
	try:
		SeatingPlan(files=sys.argv[1:])
	except Exception:
		type, value, tb = sys.exc_info()
		traceback.print_exc()
		pdb.post_mortem(tb)

#import pdb; pdb.set_trace()
