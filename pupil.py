class Pupil:
	def __init__(self, name="", present=False):
		self.name = str(name)
		self.present = present

	def json(self):
		return {
					"__type"  : "Pupil",
					"name"    : self.name,
					"present" : self.present
				}
