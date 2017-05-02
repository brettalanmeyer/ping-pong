from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService
from pingpong.services.MatchService import MatchService
from pingpong.matchtypes.Singles import Singles
import json

playerService = PlayerService()
matchService = MatchService()
singles = Singles()

class TestMatchController(BaseTest):

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

	def test_matches(self):
		rv = self.app.get("/matches")
		assert rv.status == self.ok

	def test_matchesNew(self):
		rv = self.app.get("/matches/new")
		assert rv.status == self.ok

	def test_matchesPage1(self):
		rv = self.app.get("/matches?page=1")
		assert rv.status == self.ok

	def test_matchesSeason0(self):
		rv = self.app.get("/matches?season=0")
		assert rv.status == self.ok

	def test_matchesSeason1(self):
		rv = self.app.get("/matches?season=1")
		assert rv.status == self.ok

	def test_matchesSeasonBad(self):
		rv = self.app.get("/matches?season=-1")
		assert rv.status == self.notFound

	def test_matchesSeasonBadAgain(self):
		rv = self.app.get("/matches?season=1000000")
		assert rv.status == self.notFound

	def test_singles(self):
		with self.ctx:
			player1Id = playerService.create({ "name": "Starsky" }).id
			player2Id = playerService.create({ "name": "Hutch" }).id

		rv = self.app.post("/matches", data = { "matchType": "singles" })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)\/num-of-games")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}/num-of-games".format(matchId))
		assert rv.status == self.ok

		rv = self.app.post("/matches/{}/num-of-games".format(matchId), data = { "numOfGames": "3" })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)\/players")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}/players".format(matchId))
		assert rv.status == self.ok

		rv = self.app.post("/matches/{}/players".format(matchId), data = { "playerId": [player1Id, player2Id] })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}".format(matchId))
		assert rv.status == self.ok

		rv = self.app.get("/matches/{}.json".format(matchId))
		assert rv.status == self.ok

		data = json.loads(rv.data)

		assert data["numOfGames"] == 3
		assert not data["complete"]
		assert data["matchId"] == int(matchId)
		assert data["game"] == 1
		assert data["ready"]
		assert data["points"] == 0
		assert data["matchType"] == "singles"
		assert data["playTo"] == 21

	def test_doubles(self):
		with self.ctx:
			player1Id = playerService.create({ "name": "Fry" }).id
			player2Id = playerService.create({ "name": "Leela" }).id
			player3Id = playerService.create({ "name": "The Professor" }).id
			player4Id = playerService.create({ "name": "Bender" }).id

		rv = self.app.post("/matches", data = { "matchType": "doubles" })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)\/num-of-games")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}/num-of-games".format(matchId))
		assert rv.status == self.ok

		rv = self.app.post("/matches/{}/num-of-games".format(matchId), data = { "numOfGames": "3" })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)\/players")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}/players".format(matchId))
		assert rv.status == self.ok

		rv = self.app.post("/matches/{}/players".format(matchId), data = { "playerId": [player1Id, player2Id, player3Id, player4Id] })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}".format(matchId))
		assert rv.status == self.ok

		rv = self.app.get("/matches/{}.json".format(matchId))
		assert rv.status == self.ok

		data = json.loads(rv.data)

		assert data["numOfGames"] == 3
		assert not data["complete"]
		assert data["matchId"] == int(matchId)
		assert data["game"] == 1
		assert data["ready"]
		assert data["points"] == 0
		assert data["matchType"] == "doubles"
		assert data["playTo"] == 21

	def test_doubles(self):
		with self.ctx:
			player1Id = playerService.create({ "name": "Fry" }).id
			player2Id = playerService.create({ "name": "Leela" }).id
			player3Id = playerService.create({ "name": "The Professor" }).id
			player4Id = playerService.create({ "name": "Bender" }).id

		rv = self.app.post("/matches", data = { "matchType": "nines" })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)\/players")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}/players".format(matchId))
		assert rv.status == self.ok

		rv = self.app.post("/matches/{}/players".format(matchId), data = { "playerId": [player1Id, player2Id, player3Id, player4Id] })
		match, matchId = self.redirects(rv, "\/matches\/(\d+)")
		assert rv.status == self.found
		assert match
		assert matchId != None

		rv = self.app.get("/matches/{}".format(matchId))
		assert rv.status == self.ok

		rv = self.app.get("/matches/{}.json".format(matchId))
		assert rv.status == self.ok

		data = json.loads(rv.data)

		assert not data["complete"]
		assert data["matchId"] == int(matchId)
		assert data["ready"]
		assert data["matchType"] == "nines"
		assert data["playTo"] == 9

	def test_notFound(self):
		rv = self.app.get("/matches/{}/num-of-games".format(0))
		assert rv.status == self.notFound

		rv = self.app.post("/matches/{}/num-of-games".format(0), data = {})
		assert rv.status == self.notFound

		rv = self.app.get("/matches/{}/players".format(0))
		assert rv.status == self.notFound

		rv = self.app.post("/matches/{}/players".format(0), data = {})
		assert rv.status == self.notFound

		rv = self.app.get("/matches/{}".format(0))
		assert rv.status == self.notFound

		rv = self.app.get("/matches/{}.json".format(0))
		assert rv.status == self.notFound

		rv = self.app.post("/matches/{}/play-again".format(0), data = {})
		assert rv.status == self.notFound

		rv = self.app.post("/matches/{}/undo".format(0), data = {})
		assert rv.status == self.notFound

		rv = self.app.post("/matches/{}/delete".format(0), data = {})
		assert rv.status == self.found

		self.authenticate()
		rv = self.app.post("/matches/{}/delete".format(0), data = {})
		assert rv.status == self.notFound

	def test_playAgain(self):
		with self.request:
			matchId = self.createMatch().id

		rv = self.app.post("/matches/{}/play-again".format(matchId), data = { "numOfGames": 5, "randomize": "false" })
		isMatch, newMatchId = self.redirects(rv, "\/matches\/(\d+)")

		assert isMatch
		assert matchId != int(newMatchId)

		with self.ctx:
			newMatch = matchService.selectById(int(newMatchId))
			assert not newMatch.complete
			assert newMatch.numOfGames == 5

	def test_undo(self):
		with self.request:
			match = self.createMatch()
			matchId = match.id
			assert match.complete

		rv = self.app.post("/matches/{}/undo".format(matchId))
		isMatch, sameMatchId = self.redirects(rv, "\/matches\/(\d+)")

		assert isMatch
		assert matchId == int(sameMatchId)

		with self.ctx:
			sameMatch = matchService.selectById(matchId)
			assert not sameMatch.complete

	def test_delete(self):
		self.authenticate()

		with self.request:
			matchId = self.createMatch().id

		rv = self.app.post("/matches/{}/delete".format(matchId))
		isMatch, none = self.redirects(rv, "\/matches")

		with self.ctx:
			match = matchService.selectById(matchId)
			assert match == None
