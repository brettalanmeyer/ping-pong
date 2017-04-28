from BaseTest import BaseTest

class TestErrorController(BaseTest):

	def test_404(self):
		rv = self.app.get("/non-existant-url")
		assert rv.status == self.notFound
