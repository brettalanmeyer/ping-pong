from BaseTest import BaseTest

class TestAuthenticationController(BaseTest):

	def test_authenticate(self):
		self.office()
		rv = self.authenticate()
		assert rv.status == self.ok

	def test_login(self):
		self.office()
		rv = self.app.get("/login")
		assert rv.status == self.ok

	def test_login_fail(self):
		self.office()
		rv = self.app.post("/login")
		assert rv.status == self.unauthorized

	def test_logout(self):
		self.office()
		rv = self.app.get("/logout")
		assert rv.status == self.unauthorized

	def test_logout(self):
		self.office()
		self.authenticate()
		rv = self.app.get("/logout", follow_redirects = True)
		assert rv.status == self.ok
