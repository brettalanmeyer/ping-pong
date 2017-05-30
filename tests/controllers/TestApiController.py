from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService

playerService = PlayerService()
matchService = MatchService()
singles = Singles()

class TestApiController(BaseTest):

	def createMatch(self, officeId):
		with self.request:
			player1 = playerService.create(officeId, { "name": "Fry" })
			player2 = playerService.create(officeId, { "name": "Bender" })

			match = matchService.create(officeId, "singles")
			matchService.updateGames(match.id, 1)

			singles.createTeams(match, [player1.id, player2.id], True)
			singles.play(match)

			for i in range(0, 21):
				singles.score(match, "green")

			return match

	def test_api(self):
		self.office()
		rv = self.app.get("/api")
		assert rv.status == self.ok

	def test_players(self):
		office = self.office()
		rv = self.app.get("/api/players.json?key={}".format(office["key"]))
		assert rv.status == self.ok

	def test_matches(self):
		office = self.office()
		rv = self.app.get("/api/matches.json?key={}".format(office["key"]))
		assert rv.status == self.ok

	def test_match(self):
		office = self.office()
		with self.request:
			matchId = self.createMatch(office["id"]).id
			rv = self.app.get("/api/matches/{}.json?key={}".format(matchId, office["key"]))
			assert rv.status == self.ok

	def test_isms(self):
		office = self.office()
		rv = self.app.get("/api/isms.json?key={}".format(office["key"]))
		assert rv.status == self.ok

	def test_score(self):
		office = self.office()
		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/score".format(color), data = { "key": office["key"] })
			assert rv.status == self.ok

	def test_invalid_score(self):
		rv = self.app.post("/api/buttons/black/score", data = { "key": "" })
		assert rv.status == self.badRequest

		rv = self.app.post("/api/buttons/green/score", data = { "key": "" })
		assert rv.status == self.badRequest

	def test_undo(self):
		office = self.office()
		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/undo".format(color), data = { "key": office["key"] })
			assert rv.status == self.ok

	def test_invalid_undo(self):
		rv = self.app.post("/api/buttons/black/undo", data = { "key": "" })
		assert rv.status == self.badRequest

		rv = self.app.post("/api/buttons/green/undo", data = { "key": "" })
		assert rv.status == self.badRequest
