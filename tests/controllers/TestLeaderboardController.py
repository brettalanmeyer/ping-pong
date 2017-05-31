from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService

playerService = PlayerService()

class TestLeaderboardController(BaseTest):

	def createPlayer(self, officeId):
		return playerService.create(officeId, { "name": "Orange Joe" })

	def test_leaderboard(self):
		self.office()
		rv = self.app.get("/leaderboard", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardJson(self):
		self.office()
		rv = self.app.get("/leaderboard.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardJsonSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardJsonSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardJsonSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardJsonSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardJsonSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardSingles(self):
		self.office()
		rv = self.app.get("/leaderboard/singles", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard/singles?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard/singles?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard/singles?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard/singles?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardSinglesSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard/singles?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardSinglesJson(self):
		self.office()
		rv = self.app.get("/leaderboard/singles.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesJsonSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard/singles.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesJsonSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard/singles.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesJsonSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard/singles.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardSinglesJsonSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard/singles.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardSinglesJsonSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard/singles.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardDoubles(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardDoublesSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardDoublesJson(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesJsonSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesJsonSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesJsonSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardDoublesJsonSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardDoublesJsonSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard/doubles.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardNines(self):
		self.office()
		rv = self.app.get("/leaderboard/nines", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard/nines?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard/nines?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard/nines?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard/nines?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardNinesSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard/nines?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardNinesJson(self):
		self.office()
		rv = self.app.get("/leaderboard/nines.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesJsonSeason0(self):
		self.office()
		rv = self.app.get("/leaderboard/nines.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesJsonSeason1(self):
		self.office()
		rv = self.app.get("/leaderboard/nines.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesJsonSeason2(self):
		self.office()
		rv = self.app.get("/leaderboard/nines.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboardNinesJsonSeasonInvalid(self):
		self.office()
		rv = self.app.get("/leaderboard/nines.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardNinesJsonSeasonInvalidAgain(self):
		self.office()
		rv = self.app.get("/leaderboard/nines.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboardPlayerNotFound(self):
		self.office()
		rv = self.app.get("/leaderboard/players/")
		assert rv.status == self.notFound

	def test_leaderboardPlayer(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}".format(player.id))
			assert rv.status == self.ok

	def test_leaderboardPlayerJson(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}.json".format(player.id))
			assert rv.status == self.ok

	def test_leaderboardPlayerSeason0(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}?season=0".format(player.id))
			assert rv.status == self.ok

	def test_leaderboardPlayerSeason1(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}?season=1".format(player.id))
			assert rv.status == self.ok

	def test_leaderboardPlayerSeason2(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}?season=2".format(player.id))
			assert rv.status == self.ok

	def test_leaderboardPlayerSEASON_Invalid(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}?season=-1".format(player.id))
			assert rv.status == self.notFound

	def test_leaderboardPlayerSEASON_InvalidAgain(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.get("/leaderboard/players/{}?season=10000".format(player.id))
			assert rv.status == self.notFound
