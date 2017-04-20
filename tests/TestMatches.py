from BaseTest import BaseTest

class TestMatches(BaseTest):

	def test_matches(self):
		rv = self.app.get("/matches")
		assert rv.status == self.ok

	# def test_matches(self):
	# 	rv = self.app.get("/matches/<int:id>")
	# 	assert rv.status == self.ok

	# def test_matches(self):
	# 	rv = self.app.get("/matches/<int:id>.json")
	# 	assert rv.status == self.ok

	# def test_matches(self):
	# 	rv = self.app.get("/matches/<int:id>/num-of-games")
	# 	assert rv.status == self.ok

	# def test_matches(self):
	# 	rv = self.app.get("/matches/<int:id>/players")
	# 	assert rv.status == self.ok

	def test_matches_new(self):
		rv = self.app.get("/matches/new")
		assert rv.status == self.ok

	def test_matches_page1(self):
		rv = self.app.get("/matches/page/1", follow_redirects = True)
		assert rv.status == self.ok

	# def test_matches(self):
	# 	rv = self.app.get("/matches/players/<int:playerId>"
	# 	assert rv.status == self.ok

	# def test_matches(self):
	# 	rv = self.app.get("/matches/players/<int:playerId>/page/<int:page>")
	# 	assert rv.status == self.ok