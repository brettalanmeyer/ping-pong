from BaseTest import BaseTest
from flask_login import login_user
from flask_login import login_user
from pingpong.models.AdminModel import AdminModel

class TestAdminController(BaseTest):

	def test_authenticate(self):
		rv = self.authenticate()
		assert rv.status == self.ok

	def test_login(self):
		rv = self.app.get("/login")
		assert rv.status == self.ok

	def test_admin_unauthenticated(self):
		rv = self.app.get("/admin")
		assert rv.status == self.found

	def test_admin_authenticated(self):
		self.authenticate()
		rv = self.app.get("/admin")
		assert rv.status == self.ok
