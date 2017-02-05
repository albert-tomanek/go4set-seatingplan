class Pupil:
	def __init__(self, tag, name="", present=False, x=0, y=0):
		self.name = str(name)
		self.present = present

		self.tag = tag

		self.width  = 40
		self.height = 15
		self.x = x
		self.y = y

		self.canvas_repr_id = None
		self.name_text_id = None

	def draw(self, canvas):
		# Draw ourselves on the canvas
		self.canvas_repr_id = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="#e5d8c3")
		canvas.itemconfig(self.canvas_repr_id, tags=(self.tag))

		self.draw_name(canvas)

	def draw_name(self, canvas):
		if self.name_text_id:
			canvas.delete(self.name_text_id)

		self.name_text_id = canvas.create_text((self.x + self.width / 2), (self.y + self.height/2))
		canvas.itemconfig(self.name_text_id, tag=(self.tag + "_TEXT"), text=self.name)


	def json(self):
		return {
					"__type"  : "Pupil",
					"__tag"   : self.tag,
					"name"    : self.name,
					"present" : self.present
				}
