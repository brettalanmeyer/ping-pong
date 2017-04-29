from flask_login import UserMixin

class AdminModel(UserMixin):

	def __init__(self):
		self.id = 0
