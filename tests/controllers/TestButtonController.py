from BaseTest import BaseTest

class TestButtonController(BaseTest):

	colors = ["green", "red", "yellow", "blue"]

	def test_buttons(self):
		rv = self.app.get("/buttons")
		assert rv.status == self.ok

	def test_buttons_score(self):
		for color in self.colors:
			rv = self.app.post("/buttons/{}/score".format(color))
			assert rv.status == self.ok

	def test_buttons_undo(self):
		for color in self.colors:
			rv = self.app.post("/buttons/{}/undo".format(color))
			assert rv.status == self.ok

	def test_buttons_score_invalid(self):
		rv = self.app.post("/buttons/black/score")
		assert rv.status == self.badRequest

	def test_buttons_undo_invalid(self):
		rv = self.app.post("/buttons/black/undo")
		assert rv.status == self.badRequest
