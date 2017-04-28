from BaseTest import BaseTest

class TestMainController(BaseTest):

	def test_main(self):
		rv = self.app.get("/")
		assert rv.status == self.ok

	def test_favicon(self):
		rv = self.app.get("/favicon.ico")
		assert rv.status == self.ok
