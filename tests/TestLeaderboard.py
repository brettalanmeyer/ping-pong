from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService

playerService = PlayerService()

class TestLeaderboard(BaseTest):

	def test_leaderboard(self):
		rv = self.app.get("/leaderboard", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_season_0(self):
		rv = self.app.get("/leaderboard?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_season_1(self):
		rv = self.app.get("/leaderboard?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_season_2(self):
		rv = self.app.get("/leaderboard?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_season_invalid(self):
		rv = self.app.get("/leaderboard?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_season_invalid_again(self):
		rv = self.app.get("/leaderboard?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_json(self):
		rv = self.app.get("/leaderboard.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_json_season_0(self):
		rv = self.app.get("/leaderboard.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_json_season_1(self):
		rv = self.app.get("/leaderboard.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_json_season_2(self):
		rv = self.app.get("/leaderboard.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_json_season_invalid(self):
		rv = self.app.get("/leaderboard.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_json_season_invalid_again(self):
		rv = self.app.get("/leaderboard.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_singles(self):
		rv = self.app.get("/leaderboard/singles", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_season_0(self):
		rv = self.app.get("/leaderboard/singles?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_season_1(self):
		rv = self.app.get("/leaderboard/singles?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_season_2(self):
		rv = self.app.get("/leaderboard/singles?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_season_invalid(self):
		rv = self.app.get("/leaderboard/singles?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_singles_season_invalid_again(self):
		rv = self.app.get("/leaderboard/singles?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_singles_json(self):
		rv = self.app.get("/leaderboard/singles.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_json_season_0(self):
		rv = self.app.get("/leaderboard/singles.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_json_season_1(self):
		rv = self.app.get("/leaderboard/singles.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_json_season_2(self):
		rv = self.app.get("/leaderboard/singles.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_singles_json_season_invalid(self):
		rv = self.app.get("/leaderboard/singles.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_singles_json_season_invalid_again(self):
		rv = self.app.get("/leaderboard/singles.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_doubles(self):
		rv = self.app.get("/leaderboard/doubles", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_season_0(self):
		rv = self.app.get("/leaderboard/doubles?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_season_1(self):
		rv = self.app.get("/leaderboard/doubles?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_season_2(self):
		rv = self.app.get("/leaderboard/doubles?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_season_invalid(self):
		rv = self.app.get("/leaderboard/doubles?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_doubles_season_invalid_again(self):
		rv = self.app.get("/leaderboard/doubles?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_doubles_json(self):
		rv = self.app.get("/leaderboard/doubles.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_json_season_0(self):
		rv = self.app.get("/leaderboard/doubles.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_json_season_1(self):
		rv = self.app.get("/leaderboard/doubles.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_json_season_2(self):
		rv = self.app.get("/leaderboard/doubles.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_doubles_json_season_invalid(self):
		rv = self.app.get("/leaderboard/doubles.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_doubles_json_season_invalid_again(self):
		rv = self.app.get("/leaderboard/doubles.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_nines(self):
		rv = self.app.get("/leaderboard/nines", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_season_0(self):
		rv = self.app.get("/leaderboard/nines?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_season_1(self):
		rv = self.app.get("/leaderboard/nines?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_season_2(self):
		rv = self.app.get("/leaderboard/nines?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_season_invalid(self):
		rv = self.app.get("/leaderboard/nines?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_nines_season_invalid_again(self):
		rv = self.app.get("/leaderboard/nines?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_nines_json(self):
		rv = self.app.get("/leaderboard/nines.json", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_json_season_0(self):
		rv = self.app.get("/leaderboard/nines.json?season=0", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_json_season_1(self):
		rv = self.app.get("/leaderboard/nines.json?season=1", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_json_season_2(self):
		rv = self.app.get("/leaderboard/nines.json?season=2", follow_redirects = True)
		assert rv.status == self.ok

	def test_leaderboard_nines_json_season_invalid(self):
		rv = self.app.get("/leaderboard/nines.json?season=-1", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_nines_json_season_invalid_again(self):
		rv = self.app.get("/leaderboard/nines.json?season=1000", follow_redirects = True)
		assert rv.status == self.notFound

	def test_leaderboard_player_not_found(self):
		rv = self.app.get("/leaderboard/players/")
		assert rv.status == self.notFound

	def test_leaderboard_player(self):
		with self.ctx:
			players = playerService.select().first()
			rv = self.app.get("/leaderboard/players/{}".format(players.id))
			assert rv.status == self.ok

	def test_leaderboard_player_season_0(self):
		with self.ctx:
			players = playerService.select().first()
			rv = self.app.get("/leaderboard/players/{}?season=0".format(players.id))
			assert rv.status == self.ok

	def test_leaderboard_player_season_1(self):
		with self.ctx:
			players = playerService.select().first()
			rv = self.app.get("/leaderboard/players/{}?season=1".format(players.id))
			assert rv.status == self.ok

	def test_leaderboard_player_season_2(self):
		with self.ctx:
			players = playerService.select().first()
			rv = self.app.get("/leaderboard/players/{}?season=2".format(players.id))
			assert rv.status == self.ok

	def test_leaderboard_player_season__invalid(self):
		with self.ctx:
			players = playerService.select().first()
			rv = self.app.get("/leaderboard/players/{}?season=-1".format(players.id))
			assert rv.status == self.notFound

	def test_leaderboard_player_season__invalid_again(self):
		with self.ctx:
			players = playerService.select().first()
			rv = self.app.get("/leaderboard/players/{}?season=10000".format(players.id))
			assert rv.status == self.notFound

