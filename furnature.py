class Furnature:
	width  = 0
	height = 0
	x = 0
	y = 0

class Table(Furnature):
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
class Chair(Furnature):
	def __init__(self, x=0, y=0):
		self.width  = 47	# Measurments are in centimetres
		self.height = 47	# https://goo.gl/c0tCEt
		self.x = x
		self.y = y

		self.pupil  = None

	def draw(self, canvas):
		# Draw ourselves on the canvas, and keep our ID
		return canvas.create_oval(self.x, self.y, (self.x + self.width), (self.y + self.height), fill="#dd0000")

	def __repr__(self):
		return {									\
					"__type" : "Chair",				\
					"x" : self.x,					\
					"y" : self.y					\
				}
