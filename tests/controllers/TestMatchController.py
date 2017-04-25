from BaseTest import BaseTest

class TestMatchController(BaseTest):

	def test_matches(self):
		rv = self.app.get("/matches")
		assert rv.status == self.ok

	def test_matches_new(self):
		rv = self.app.get("/matches/new")
		assert rv.status == self.ok

	def test_matches_page_1(self):
		rv = self.app.get("/matches?page=1")
		assert rv.status == self.ok

	def test_matches_season_0(self):
		rv = self.app.get("/matches?season=0")
		assert rv.status == self.ok

	def test_matches_season_1(self):
		rv = self.app.get("/matches?season=1")
		assert rv.status == self.ok

	def test_matches_season_bad(self):
		rv = self.app.get("/matches?season=-1")
		assert rv.status == self.notFound

	def test_matches_season_bad_again(self):
		rv = self.app.get("/matches?season=1000000")
		assert rv.status == self.notFound