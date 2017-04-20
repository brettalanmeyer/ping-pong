from BaseTest import BaseTest

class TestIsms(BaseTest):

	def test_isms(self):
		rv = self.app.get("/isms")
		assert rv.status == self.ok

	def test_isms_json(self):
		rv = self.app.get("/isms.json")
		assert rv.status == self.ok

	# def test_isms(self):
	# 	rv = self.app.get("/isms/<int:id>/edit")
	# 	assert rv.status == self.ok

	def test_isms_new(self):
		rv = self.app.get("/isms/new")
		assert rv.status == self.ok