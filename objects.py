import json

class Table:
	def __init__(self, width=120, height=80, x=0, y=0):
		self.width  = width
		self.height = height
		self.x = x
		self.y = y

	def draw(self, canvas):
		# Draw ourselves on the canvas, and keep our ID
		return canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="#376eb4")

	def __repr__(self):
		return { 									\
					"__type" : "Table",				\
					"x" : self.x,					\
					"y" : self.y,					\
					"width"  : self.width,			\
					"height" : self.height			\
				}

class Pupil:
	def __init__(self, name):
		self.name = name

	def draw(self, canvas):
		pass
