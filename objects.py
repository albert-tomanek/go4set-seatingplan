class Table:
	def __init__(self, width=120, height=80):
		self.width  = width
		self.height = height

	def draw(self, canvas, x=0, y=0):
		# Draw ourselves on the canvas, and keep our ID
		return canvas.create_rectangle(x, y, x + self.width, y + self.height, fill="#376eb4")
