from tkinter import *
from tkinter.ttk import *
from widgets import *
import objects

def canvas_get(canvas, x, y):
	return canvas.find_overlapping(x, y, x+1, y+1)[0] if canvas.find_all() != () else None		# .find_overlapping() returns a tuple

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

		def rclick_menu(event):
			menu = Menu(self.root, tearoff=0)

			def delete_table(event):
				table = canvas_get(self.canvas, event.x, event.y)
				self.canvas.delete(table)

			menu.add_command(label="Add table", command=self.add_table)
			menu.add_command(label="Delete table", command=lambda: delete_table(event))

			menu.post(event.x_root, event.y_root)		# _root => x and y of it in the whole roow window

		def dnd_bdown(event):
			# Temporarily store the positions
			self.__dnd_id = canvas_get(self.canvas, event.x, event.y)
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

		self.canvas = Canvas(self.root, width=800, height=600, bg="#ffffff", borderwidth=1, relief=SUNKEN)
		self.canvas.grid(column=0, row=0,padx=10, pady=10)

		self.canvas.bind("<Button-1>", dnd_bdown)
		self.canvas.bind("<ButtonRelease-1>", dnd_bup)
		self.canvas.bind("<Button-3>", rclick_menu)

		## The frame with buttons ##
		self.ctrlframe = Frame(self.root)
		self.ctrlframe.grid(column=1, row=0)

		self.addTableButton = Button(self.ctrlframe, text='Add Table', command=self.add_table)
		self.addTableButton.grid(column=0, row=0, padx=10, pady=10)

		self.root.mainloop()

	def add_table(self):
		# What to do when the 'Add Table' button is pressed

		dialog = Toplevel(master=self.root)
		dialog.title("Table properties")

		widthLabel = Label(dialog, text="Width (cm):")
		widthEntry = NumEntry(dialog, default=200, step=5, min_val=50, max_val=500)
		widthLabel.grid(column=0, row=0, padx=10, pady=10)
		widthEntry.grid(column=1, row=0, padx=10, pady=10)

		heightLabel = Label(dialog, text="Length (cm):")
		heightEntry = NumEntry(dialog, default=120, step=5, min_val=50, max_val=500)
		heightLabel.grid(column=0, row=1, padx=10, pady=10)
		heightEntry.grid(column=1, row=1, padx=10, pady=10)

		def ok(*args):
			table = objects.Table(int(widthEntry.get()), int(heightEntry.get()))
			self.contents[table.draw(self.canvas, 0, 0)] = table
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


if __name__ == '__main__':
	x = Classroom()
