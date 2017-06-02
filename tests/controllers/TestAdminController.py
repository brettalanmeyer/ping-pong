from BaseTest import BaseTest
from flask_login import login_user
from pingpong.models.AdminModel import AdminModel

class TestAdminController(BaseTest):

	def test_adminUnauthenticated(self):
		self.office()
		rv = self.app.get("/admin")
		assert rv.status == self.found

	def test_adminAuthenticated(self):
		self.office()
		self.authenticate()
		rv = self.app.get("/admin")
		assert rv.status == self.ok

	def test_adminSendMessageInvalid(self):
		self.office()
		self.authenticate()
		rv = self.app.post("/admin/send-message", data = { "message": "This is my message" }, follow_redirects = True)
		assert rv.status == self.ok

	def test_adminSendMessage(self):
		office = self.office()
		self.authenticate()
		rv = self.app.post("/admin/send-message", data = { "message": "This is my message", "officeId": [office["id"]] }, follow_redirects = True)
		assert rv.status == self.ok
