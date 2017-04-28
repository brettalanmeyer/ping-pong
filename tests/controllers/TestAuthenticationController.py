from BaseTest import BaseTest

class TestAuthenticationController(BaseTest):

	def test_authenticate(self):
		rv = self.authenticate()
		assert rv.status == self.ok

	def test_login(self):
		rv = self.app.get("/login")
		assert rv.status == self.ok

	def test_login_fail(self):
		rv = self.app.post("/login")
		assert rv.status == self.unauthorized

	def test_logout(self):
		rv = self.app.get("/login")
		assert rv.status == self.ok
