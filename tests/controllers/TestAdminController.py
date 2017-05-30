from BaseTest import BaseTest
from flask_login import login_user
from pingpong.models.AdminModel import AdminModel

class TestAdminController(BaseTest):

	def test_admin_unauthenticated(self):
		self.office()
		rv = self.app.get("/admin")
		assert rv.status == self.found

	def test_admin_authenticated(self):
		self.office()
		self.authenticate()
		rv = self.app.get("/admin")
		assert rv.status == self.ok
