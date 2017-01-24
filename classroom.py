from tkinter import *
from tkinter.ttk import *
import objects

class Classroom:
	def __init__(self):
		# Create instance variables
		self.contents = {}

		self.__dnd_id = None	# The ID of the object we're dragging and dropping
		self.__dnd_start_x = None
		self.__dnd_start_y = None

		##

		super(Classroom, self).__init__()	# Initialise the superclass
		self.root = Tk()

		def dnd_bdown(event):
			# Temporarily store the positions
			self.__dnd_id = self.canvas.find_overlapping(event.x, event.y, event.x+1, event.y+1)[0] if self.canvas.find_all() != () else None		# .find_overlapping() returns a tuple
			self.__dnd_start_x = event.x
			self.__dnd_start_y = event.y

		def dnd_bup(event):
#			import pdb; pdb.set_trace()
			if self.__dnd_id:
				object = self.contents[self.__dnd_id]
				self.canvas.move(self.__dnd_id, event.x-self.__dnd_start_x, event.y-self.__dnd_start_y)		# .move doesn't want to know to WHERE it moves, it wants to know how much it should move BY.
				self.__dnd_id = None
				self.__dnd_start_x = None
				self.__dnd_start_y = None

		self.canvas = Canvas(self.root, width=640, height=480, bg="#ffffff", borderwidth=1, relief=SUNKEN)
		self.canvas.bind("<Button-1>", dnd_bdown)
		self.canvas.bind("<ButtonRelease-1>", dnd_bup)
		self.canvas.grid(column=0, row=0,padx=10, pady=10)

		# Functions to do with buttons in the frame

		def addTableFunct():
			# What to do when the 'Add Table' button is pressed

			dialog = Toplevel()
			dialog.title("Table properties")

			widthLabel = Label(dialog, text="Width:")
			widthEntry = Entry(dialog)
			widthEntry.insert(0, "200")
			widthLabel.grid(column=0, row=0, padx=10, pady=10)
			widthEntry.grid(column=1, row=0, padx=10, pady=10)

			heightLabel = Label(dialog, text="Length:")
			heightEntry = Entry(dialog)
			heightEntry.insert(0, "120")
			heightLabel.grid(column=0, row=1, padx=10, pady=10)
			heightEntry.grid(column=1, row=1, padx=10, pady=10)

			def ok():
				table = objects.Table(int(widthEntry.get()), int(heightEntry.get()))
				self.contents[table.draw(self.canvas, 0, 0)] = table
				dialog.destroy()

			def cancel():
				dialog.destroy()

			buttonFrame  = Frame(dialog)
			buttonFrame.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
			okButton     = Button(buttonFrame, text="Ok", command=ok)
			cancelButton = Button(buttonFrame, text="Cancel", command=cancel)
			okButton.grid(column=1, row=0, padx=10)
			cancelButton.grid(column=0, row=0, padx=10)


		## The frame with buttons ##
		self.ctrlframe = Frame(self.root)
		self.ctrlframe.grid(column=1, row=0)


		self.addButton = Button(self.ctrlframe, text='Add Table', command=addTableFunct)
		self.addButton.grid(column=0, row=0, padx=10, pady=10)

		self.root.mainloop()

if __name__ == '__main__':
	x = Classroom()
