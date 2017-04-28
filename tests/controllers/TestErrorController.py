from BaseTest import BaseTest

class TestErrorController(BaseTest):

	def test_404_url(self):
		rv = self.app.get("/non-existant-url")
		assert rv.status == self.notFound

	def test_400(self):
		rv = self.app.get("/errors/bad-request")
		assert rv.status == self.badRequest

	def test_404(self):
		rv = self.app.get("/errors/not-found")
		assert rv.status == self.notFound

	def test_500(self):
		rv = self.app.get("/errors/server-error")
		assert rv.status == self.internalServerError
