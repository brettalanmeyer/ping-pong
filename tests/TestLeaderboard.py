from BaseTest import BaseTest

class TestLeaderboard(BaseTest):

	def test_leaderboard(self):
		rv = self.app.get("/leaderboard")
		assert rv.status == self.ok

	def test_leaderboard_json(self):
		rv = self.app.get("/leaderboard.json")
		assert rv.status == self.ok

	def test_leaderboard_singles(self):
		rv = self.app.get("/leaderboard/singles", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles(self):
		rv = self.app.get("/leaderboard/doubles")
		assert rv.status == self.ok

	def test_leaderboard_nines(self):
		rv = self.app.get("/leaderboard/nines")
		assert rv.status == self.ok

	def test_leaderboard_singles_json(self):
		rv = self.app.get("/leaderboard/singles.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_json(self):
		rv = self.app.get("/leaderboard/doubles.json")
		assert rv.status == self.ok

	def test_leaderboard_nines_json(self):
		rv = self.app.get("/leaderboard/nines.json")
		assert rv.status == self.ok

	# def test_leaderboard(self):
	# 	rv = self.app.get("/leaderboard/players/<int:id>")
	# 	assert rv.status == self.ok

	# def test_leaderboard(self):
	# 	rv = self.app.get("/leaderboard/players/<int:id>.json")
	# 	assert rv.status == self.ok