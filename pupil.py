class Pupil:
	def __init__(self, tag, x=0, y=0, name="", scanner_id=None, present=False):
		self.name = str(name)
		self.present = present

		self.tag = tag
		self.scanner_id = scanner_id

		self.width  = 40
		self.height = 15
		self.x = x
		self.y = y

		self.name_text_id = None

	def draw(self, canvas):
		# Draw ourselves on the canvas
		canvas_repr_id = canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill="#e5d8c3")
		canvas.itemconfig(canvas_repr_id, tags=(self.tag))
		canvas.tag_raise(self.tag)	# So we're always above chairs and tables

		self.draw_name(canvas)

	def draw_name(self, canvas):
		if self.name_text_id:
			canvas.delete(self.name_text_id)

		self.name_text_id = canvas.create_text(self.x + (self.width / 2), self.y + (self.height/2))
		canvas.itemconfig(self.name_text_id, tag=(self.tag + "_TEXT"), text=self.name)

	def get_id(self):
		# This is not going to work unles the tag is of format 'PUPIL_%d'
		return int(self.tag.split('_')[-1])

	def json(self):
		return {
					"__type"  : "Pupil",
					"__tag"   : self.tag,
					"__scanner_id" : self.scanner_id,
					"name"    : self.name,
					"present" : self.present
				}
