from BaseTest import BaseTest

class TestButtons(BaseTest):

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