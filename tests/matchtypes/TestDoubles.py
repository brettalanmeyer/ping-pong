from BaseTest import BaseTest
from pingpong.matchtypes.Doubles import Doubles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
import collections
import random

doubles = Doubles()
matchService = MatchService()
playerService = PlayerService()

class TestDoubles(BaseTest):

	def createMatch(self, numOfGames, randomize = True):
		with self.request:
			player1 = playerService.create({ "name": "Han" })
			player2 = playerService.create({ "name": "Chewie" })
			player3 = playerService.create({ "name": "Luke" })
			player4 = playerService.create({ "name": "Leia" })

			match = matchService.create("doubles")
			matchService.updateGames(match.id, numOfGames)

			doubles.createTeams(match, [player1.id, player2.id, player3.id, player4.id], randomize)
			doubles.play(match)

			return match

	def test_createMatch(self):
		with self.ctx:
			match = self.createMatch(5, True)

			assert match.matchType == "doubles"
			assert match.playTo == 21
			assert match.numOfGames == 5
			assert match.game == 1
			assert match.ready == 1
			assert match.complete == 0
			assert match.completedAt == None

			data = doubles.matchData(match)

			assert data["matchId"] == match.id
			assert data["matchType"] == match.matchType
			assert data["playTo"] == match.playTo
			assert data["numOfGames"] == match.numOfGames
			assert data["game"] == match.game
			assert data["template"] == doubles.matchTemplate
			assert not data["complete"]
			assert data["ready"]
			assert data["createdAt"] != None
			assert data["completedAt"] == None
			assert data["points"] == 0

	def test_oneSet(self):
		with self.ctx:
			match = self.createMatch(5, False)

			for i in range(0, 21):
				doubles.score(match, "green")

			data = doubles.matchData(match)

			assert match.game == 2
			assert not data["complete"]
			assert data["completedAt"] == None
			assert data["game"] == 2

	def test_twoSets(self):
		with self.ctx:
			match = self.createMatch(5)

			for i in range(0, 42):
				doubles.score(match, "green")

			data = doubles.matchData(match)

			assert match.game == 3
			assert not data["complete"]
			assert data["completedAt"] == None
			assert data["game"] == 3

	def test_winnerShutout(self):
		with self.request:
			match = self.createMatch(5)

			for i in range(0, 21):
				doubles.score(match, "green" if i % 2 == 0 else "red")

			for i in range(0, 21):
				doubles.score(match, "yellow" if i % 2 == 0 else "blue")

			for i in range(0, 21):
				doubles.score(match, "green" if i % 4 == 0 else "red")

			data = doubles.matchData(match)

			assert match.game == 3
			assert match.completedAt != None
			assert data["complete"]
			assert data["completedAt"] != None
			assert data["game"] == 3

	def test_everyOtherWinner(self):
		with self.request:
			match = self.createMatch(5)

			for i in range(0, 105):
				doubles.score(match, "green" if i % 3 == 0 else "red")

			data = doubles.matchData(match)

			assert match.game == 5
			assert match.completedAt != None
			assert data["complete"]
			assert data["completedAt"] != None
			assert data["game"] == 5

	def test_winByTwoPoints(self):
		with self.request:
			match = self.createMatch(1)

			data = doubles.matchData(match)

			while not data["complete"]:
				if random.randrange(0,1) == 0:
					doubles.score(match, "green")
				else:
					doubles.score(match, "yellow")

				data = doubles.matchData(match)

			north = data["teams"]["north"]
			south = data["teams"]["south"]

			assert data["game"] == 1
			assert len(north["games"]) == 1
			assert len(south["games"]) == 1

			if north["winner"]:
				assert north["games"][0]["win"]
				assert north["games"][0]["score"] >= south["games"][0]["score"] + 2
			elif south["winner"]:
				assert south["games"][0]["win"]
				assert south["games"][0]["score"] >= north["games"][0]["score"] + 2

			assert data["points"] == north["points"] + south["points"]

	def test_matchJson(self):
		with self.ctx:
			match = self.createMatch(1)
			rv = self.app.get("/matches/{}.json".format(match.id))
			assert rv.status == self.ok

	def test_undoScore(self):
		with self.ctx:
			match = self.createMatch(1)

			doubles.score(match, "green")
			doubles.score(match, "green")

			data = doubles.matchData(match)
			assert data["matchId"] == match.id
			assert data["points"] == 2

			doubles.undo(match, "green")
			data = doubles.matchData(match)
			assert data["points"] == 1

			doubles.undo(match, "green")
			data = doubles.matchData(match)
			assert data["points"] == 0

	def test_undoMatch(self):
		with self.request:
			match = self.createMatch(1)
			for i in range(0, 21):
				doubles.score(match, "green")

			data = doubles.matchData(match)
			assert data["matchId"] == match.id
			assert data["game"] == 1
			assert data["complete"]
			assert data["completedAt"] != None
			assert data["points"] == 21

			doubles.undo(match, "green")
			data = doubles.matchData(match)

			assert not data["complete"]
			assert data["completedAt"] == None
			assert data["points"] == 20

	def test_playAgain(self):
		with self.request:
			match = self.createMatch(1)
			for i in range(0, 21):
				doubles.score(match, "green")

			matchPlayers = []
			for team in match.teams:
				for player in team.players:
					matchPlayers.append(player)

			data = doubles.matchData(match)
			assert data["complete"]

			newMatch = doubles.playAgain(match, 3, True)
			newData = doubles.matchData(newMatch)

			newMatchPlayers = []
			for team in newMatch.teams:
				for player in team.players:
					newMatchPlayers.append(player)

			assert collections.Counter(matchPlayers) == collections.Counter(newMatchPlayers)
			assert newData["ready"]
			assert not newData["complete"]
			assert newData["game"] == 1
			assert newData["points"] == 0
