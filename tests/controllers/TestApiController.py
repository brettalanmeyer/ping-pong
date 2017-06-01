from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.utils import util
import json

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

	def test_playersOk(self):
		office = self.office()
		rv = self.app.get("/api/players.json?key={}".format(office["key"]))
		assert rv.status == self.ok

	def test_playersUnauthorized(self):
		rv = self.app.get("/api/players.json?key={}".format(util.generateUUID()))
		assert rv.status == self.unauthorized
		self.checkUnauthorizedResponse(rv.data)

	def test_matchesOk(self):
		office = self.office()
		rv = self.app.get("/api/matches.json?key={}".format(office["key"]))
		assert rv.status == self.ok

	def test_matchesUnauthorized(self):
		rv = self.app.get("/api/matches.json?key={}".format(util.generateUUID()))
		assert rv.status == self.unauthorized
		self.checkUnauthorizedResponse(rv.data)

	def test_matchOk(self):
		office = self.office()
		with self.request:
			matchId = self.createMatch(office["id"]).id
			rv = self.app.get("/api/matches/{}.json?key={}".format(matchId, office["key"]))
			assert rv.status == self.ok

	def test_matchUnauthorized(self):
		with self.request:
			rv = self.app.get("/api/matches/{}.json?key={}".format(0, util.generateUUID()))
			assert rv.status == self.unauthorized
			self.checkUnauthorizedResponse(rv.data)

	def test_matchNotFound(self):
		office = self.office()
		with self.request:
			rv = self.app.get("/api/matches/{}.json?key={}".format(0, office["key"]))
			assert rv.status == self.notFound

	def test_ismsOk(self):
		office = self.office()
		rv = self.app.get("/api/isms.json?key={}".format(office["key"]))
		assert rv.status == self.ok

	def test_ismsUnauthorized(self):
		rv = self.app.get("/api/isms.json?key={}".format(util.generateUUID()))
		assert rv.status == self.unauthorized
		self.checkUnauthorizedResponse(rv.data)

	def test_scoreOk(self):
		office = self.office()
		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/score".format(color), data = { "key": office["key"] })
			assert rv.status == self.ok
			self.checkButtonResponse(rv.data, "score", color)

	def test_scoreUnauthorized(self):
		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/score".format(color), data = { "key": util.generateUUID() })
			assert rv.status == self.unauthorized
			self.checkUnauthorizedResponse(rv.data)

	def test_scoreBadRequest(self):
		office = self.office()
		rv = self.app.post("/api/buttons/black/score", data = { "key": office["key"] })
		assert rv.status == self.badRequest

	def test_undoOk(self):
		office = self.office()
		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/undo".format(color), data = { "key": office["key"] })
			assert rv.status == self.ok
			self.checkButtonResponse(rv.data, "undo", color)

	def test_undoUnauthorized(self):
		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/undo".format(color), data = { "key": util.generateUUID() })
			assert rv.status == self.unauthorized
			self.checkUnauthorizedResponse(rv.data)

	def test_undoBadRequest(self):
		office = self.office()
		rv = self.app.post("/api/buttons/black/undo", data = { "key": office["key"] })
		assert rv.status == self.badRequest

	def checkUnauthorizedResponse(self, response):
		data = json.loads(response)
		assert "error" in data
		assert "success" in data
		assert not data["success"]

	def checkButtonResponse(self, response, action, button):
		data = json.loads(response)
		assert "matchId" in data
		assert "action" in data
		assert "button" in data
		assert "officeId" in data
		assert "officeName" in data
		assert data["action"] == action
		assert data["button"] == button
