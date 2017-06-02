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

	def test_feedbackSendNull(self):
		self.office()
		rv = self.app.post("/feedback", data = {})
		assert rv.status == self.badRequest

	def test_feedbackSendEmpty(self):
		self.office()
		rv = self.app.post("/feedback", data = { "name": "", "email": "", "message": "" })
		assert rv.status == self.badRequest

	def test_feedbackSend(self):
		self.office()

		rv = self.app.post("/feedback", data = {
			"name": "Don Bot",
			"email": "",
			"message": "This is a test message."
		}, follow_redirects = True)

		assert rv.status == self.ok

	def test_favicon(self):
		rv = self.app.get("/favicon.ico")
		assert rv.status == self.ok
