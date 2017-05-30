from BaseTest import BaseTest

class TestMainController(BaseTest):

	def test_main(self):
		self.office()
		rv = self.app.get("/")
		assert rv.status == self.ok

	def test_rules(self):
		self.office()
		rv = self.app.get("/rules")
		assert rv.status == self.ok

	def test_changes(self):
		self.office()
		rv = self.app.get("/changes")
		assert rv.status == self.ok

	def test_feedback(self):
		self.office()
		rv = self.app.get("/feedback")
		assert rv.status == self.ok

	def test_favicon(self):
		rv = self.app.get("/favicon.ico")
		assert rv.status == self.ok
