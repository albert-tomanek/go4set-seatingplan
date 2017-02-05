class Furnature:
	width  = 0
	height = 0
	x = 0
	y = 0

	tag = None

class Table(Furnature):
	def __init__(self, tag, name="", width=120, height=80, x=0, y=0):
		self.tag = tag
		self.width  = width
		self.height = height
		self.x = x
		self.y = y

		self.name = name
		self.name_text_id = None

	def draw(self, canvas):
		# Draw ourselves on the canvas
		my_id = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="#376eb4")
		canvas.itemconfig(my_id, tags=(self.tag))

		self.draw_name(canvas)

	def draw_name(self, canvas):
		if self.name_text_id:
			canvas.delete(self.name_text_id)

		self.name_text_id = canvas.create_text((self.x + self.width / 2), (self.y + self.height/2))
		canvas.itemconfig(self.name_text_id, text=self.name)

	def json(self):
		return { 									\
					"__type" : "Table",				\
					"__tag"  : self.tag,			\
					"x" : self.x,					\
					"y" : self.y,					\
					"width"  : self.width,			\
					"height" : self.height,			\
					"name" : self.name				\
				}
class Chair(Furnature):
	def __init__(self, tag, x=0, y=0, pupil=None):
		self.tag = tag
		self.width  = 47	# Measurments are in centimetres
		self.height = 47	# https://goo.gl/c0tCEt
		self.x = x
		self.y = y

		self.pupil  = pupil

	def draw(self, canvas):
		# Draw ourselves on the canvas, and keep our ID
		my_id = canvas.create_oval(self.x, self.y, (self.x + self.width), (self.y + self.height), fill="#dd0000")
		canvas.itemconfig(my_id, tags=(self.tag))

	def json(self):
		return {
					"__type" : "Chair",
					"__tag"  : self.tag,
					"pupil"  : self.pupil.tag,
					"x" : self.x,
					"y" : self.y
				}
