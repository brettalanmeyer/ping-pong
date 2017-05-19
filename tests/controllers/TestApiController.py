from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService

playerService = PlayerService()
matchService = MatchService()
singles = Singles()

class TestMainController(BaseTest):

	def createMatch(self):
		with self.request:
			player1 = playerService.create({ "name": "Fry" })
			player2 = playerService.create({ "name": "Bender" })

			match = matchService.create("singles")
			matchService.updateGames(match.id, 1)

			singles.createTeams(match, [player1.id, player2.id], True)
			singles.play(match)

			for i in range(0, 21):
				singles.score(match, "green")

			return match

	def test_api(self):
		rv = self.app.get("/api")
		assert rv.status == self.ok

	def test_players(self):
		rv = self.app.get("/api/players.json")
		assert rv.status == self.ok

	def test_matches(self):
		rv = self.app.get("/api/matches.json")
		assert rv.status == self.ok

	def test_match(self):
		with self.request:
			matchId = self.createMatch().id

			rv = self.app.get("/api/matches/{}.json".format(matchId))
			assert rv.status == self.ok

	def test_match_teams(self):
		with self.request:
			matchId = self.createMatch().id

			rv = self.app.get("/api/matches/{}/teams.json".format(matchId))
			assert rv.status == self.ok

	def test_match_scores(self):
		with self.request:
			matchId = self.createMatch().id

			rv = self.app.get("/api/matches/{}/scores.json".format(matchId))
			assert rv.status == self.ok

	def test_games(self):
		rv = self.app.get("/api/games.json")
		assert rv.status == self.ok

	def test_isms(self):
		rv = self.app.get("/api/isms.json")
		assert rv.status == self.ok

