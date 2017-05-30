from BaseTest import BaseTest

class TestErrorController(BaseTest):

	def test_404_url(self):
		self.office()
		rv = self.app.get("/non-existant-url")
		assert rv.status == self.notFound

	def test_400(self):
		self.office()
		rv = self.app.get("/errors/bad-request")
		assert rv.status == self.badRequest

	def test_404(self):
		self.office()
		rv = self.app.get("/errors/not-found")
		assert rv.status == self.notFound

	def test_500(self):
		self.office()
		rv = self.app.get("/errors/server-error")
		assert rv.status == self.internalServerError
