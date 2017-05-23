from BaseTest import BaseTest

class TestMainController(BaseTest):

	def test_main(self):
		rv = self.app.get("/")
		assert rv.status == self.ok

	def test_rules(self):
		rv = self.app.get("/rules")
		assert rv.status == self.ok

	def test_changes(self):
		rv = self.app.get("/changes")
		assert rv.status == self.ok

	def test_feedback(self):
		rv = self.app.get("/feedback")
		assert rv.status == self.ok

	def test_favicon(self):
		rv = self.app.get("/favicon.ico")
		assert rv.status == self.ok
