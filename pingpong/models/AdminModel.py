from flask_login import UserMixin

class AdminModel(UserMixin):

	def __init__(self):
		self.id = 0
		self.name = "BemAdmin"
		self.password = self.name + "_secret"

	def __repr__(self):
		return "%d/%s/%s" % (self.id, self.name, self.password)
