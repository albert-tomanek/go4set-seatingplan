from tkinter import *

class NumEntry(Frame):
	def __init__(self, parent, default=None, step=1, max_val=10000, min_val=0):
		super(NumEntry, self).__init__(parent)		# Initialise the superclass
		self.step  = int(step)
		self.max_val   = int(max_val)
		self.min_val   = int(min_val)

		self.entry = Entry(self)
		self.entry.insert(0, str(default) if default else "")
		self.entry.grid(column=0, row=0, padx=5)

		self.incrementButton = Button(self, text="+", command=self.increment)
		self.incrementButton.grid(column=1, row=0, padx=5)

		self.decrementButton = Button(self, text="-", command=self.decrement)
		self.decrementButton.grid(column=2, row=0, padx=5)


	def increment(self):
		current = int(self.entry.get())

		# Make sure we don't go over the max. value
		if (current + self.step > self.max_val):
			return

		current += self.step
		self.entry.delete(0, END)
		self.entry.insert(0, str(current))

	def decrement(self):
		current = int(self.entry.get())

		# Make sure we don't go under the min. value
		if (current - self.step < self.min_val):
			return

		current -= self.step
		self.entry.delete(0, END)
		self.entry.insert(0, str(current))

	def get(self):
		return int(self.entry.get())
