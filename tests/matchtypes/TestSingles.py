from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
import collections
import random

singles = Singles()
matchService = MatchService()
playerService = PlayerService()

class TestSingles(BaseTest):

	def createMatch(self, numOfGames, randomize = True):
		with self.request:
			player1 = playerService.create({ "name": "Han" })
			player2 = playerService.create({ "name": "Chewie " })

			match = matchService.create("singles")
			matchService.updateGames(match.id, numOfGames)

			singles.createTeams(match, [player1.id, player2.id], randomize)
			singles.play(match)

			return match

	def test_createMatch(self):
		with self.ctx:
			match = self.createMatch(5)

			assert match.matchType == "singles"
			assert match.playTo == 21
			assert match.numOfGames == 5
			assert match.game == 1
			assert match.ready == 1
			assert match.complete == 0
			assert match.completedAt == None

			data = singles.matchData(match)

			assert data["matchId"] == match.id
			assert data["matchType"] == match.matchType
			assert data["playTo"] == match.playTo
			assert data["numOfGames"] == match.numOfGames
			assert data["game"] == match.game
			assert data["template"] == singles.matchTemplate
			assert not data["complete"]
			assert data["ready"]
			assert data["createdAt"] != None
			assert data["completedAt"] == None
			assert data["points"] == 0

	def test_oneSet(self):
		with self.ctx:
			match = self.createMatch(5, False)

			for i in range(0, 21):
				singles.score(match, "green")

			data = singles.matchData(match)

			assert match.game == 2
			assert not data["complete"]
			assert data["completedAt"] == None
			assert data["game"] == 2

	def test_twoSets(self):
		with self.ctx:
			match = self.createMatch(5)

			for i in range(0, 42):
				singles.score(match, "green")

			data = singles.matchData(match)

			assert match.game == 3
			assert not data["complete"]
			assert data["completedAt"] == None
			assert data["game"] == 3

	def test_winnerShutout(self):
		with self.ctx:
			match = self.createMatch(5)

			for i in range(0, 21):
				singles.score(match, "green" if i % 2 == 0 else "red")

			for i in range(0, 21):
				singles.score(match, "yellow" if i % 2 == 0 else "blue")

			for i in range(0, 21):
				singles.score(match, "green" if i % 4 == 0 else "red")

			data = singles.matchData(match)

			assert match.game == 3
			assert match.completedAt != None
			assert data["complete"]
			assert data["completedAt"] != None
			assert data["game"] == 3

	def test_everyOtherWinner(self):
		with self.ctx:
			match = self.createMatch(5)

			for i in range(0, 105):
				singles.score(match, "green" if i % 3 == 0 else "red")

			data = singles.matchData(match)

			assert match.game == 5
			assert match.completedAt != None
			assert data["complete"]
			assert data["completedAt"] != None
			assert data["game"] == 5

	def test_winByTwoPoints(self):
		with self.ctx:
			match = self.createMatch(1)

			data = singles.matchData(match)

			while not data["complete"]:
				if random.randrange(0,1) == 0:
					singles.score(match, "green")
				else:
					singles.score(match, "yellow")

				data = singles.matchData(match)

			green = data["teams"]["green"]
			yellow = data["teams"]["yellow"]

			assert data["game"] == 1
			assert len(green["games"]) == 1
			assert len(yellow["games"]) == 1

			if green["winner"]:
				assert green["games"][0]["win"]
				assert green["games"][0]["score"] >= yellow["games"][0]["score"] + 2
			elif yellow["winner"]:
				assert yellow["games"][0]["win"]
				assert yellow["games"][0]["score"] >= green["games"][0]["score"] + 2

			assert data["points"] == green["points"] + yellow["points"]

	def test_matchJson(self):
		with self.ctx:
			match = self.createMatch(1)
			rv = self.app.get("/matches/{}.json".format(match.id))
			assert rv.status == self.ok

	def test_undoScore(self):
		with self.ctx:
			match = self.createMatch(1)

			singles.score(match, "green")
			singles.score(match, "green")

			data = singles.matchData(match)
			assert data["matchId"] == match.id
			assert data["points"] == 2

			singles.undo(match, "green")
			data = singles.matchData(match)
			assert data["points"] == 1

			singles.undo(match, "green")
			data = singles.matchData(match)
			assert data["points"] == 0

	def test_undoMatch(self):
		with self.ctx:
			match = self.createMatch(1)
			for i in range(0, 21):
				singles.score(match, "green")

			data = singles.matchData(match)
			assert data["matchId"] == match.id
			assert data["game"] == 1
			assert data["complete"]
			assert data["completedAt"] != None
			assert data["points"] == 21

			singles.undo(match, "green")
			data = singles.matchData(match)

			assert not data["complete"]
			assert data["completedAt"] == None
			assert data["points"] == 20

	def test_playAgain(self):
		with self.ctx:
			match = self.createMatch(1)
			for i in range(0, 21):
				singles.score(match, "green")

			matchPlayers = []
			for team in match.teams:
				for player in team.players:
					matchPlayers.append(player)

			data = singles.matchData(match)
			assert data["complete"]

			newMatch = singles.playAgain(match, 3, True)
			newData = singles.matchData(newMatch)

			newMatchPlayers = []
			for team in newMatch.teams:
				for player in team.players:
					newMatchPlayers.append(player)

			assert collections.Counter(matchPlayers) == collections.Counter(newMatchPlayers)
			assert newData["ready"]
			assert not newData["complete"]
			assert newData["game"] == 1
			assert newData["points"] == 0

	def test_serving(self):
		with self.ctx:
			match = self.createMatch(1)

			# 0 - 5
			for i in range(0, 5):
				data = singles.matchData(match)
				assert data["teams"]["green"]["serving"]
				assert not data["teams"]["yellow"]["serving"]
				singles.score(match, "green")

			# 5 - 5
			for i in range(0, 5):
				data = singles.matchData(match)
				assert not data["teams"]["green"]["serving"]
				assert data["teams"]["yellow"]["serving"]
				singles.score(match, "yellow")

			# 10 - 5
			for i in range(0, 5):
				data = singles.matchData(match)
				assert data["teams"]["green"]["serving"]
				assert not data["teams"]["yellow"]["serving"]
				singles.score(match, "blue")

			# 10 - 10
			for i in range(0, 5):
				data = singles.matchData(match)
				assert not data["teams"]["green"]["serving"]
				assert data["teams"]["yellow"]["serving"]
				singles.score(match, "red")

			# 10 - 15
			for i in range(0, 5):
				data = singles.matchData(match)
				assert data["teams"]["green"]["serving"]
				assert not data["teams"]["yellow"]["serving"]
				singles.score(match, "green")

			# 15 - 15
			for i in range(0, 5):
				data = singles.matchData(match)
				assert not data["teams"]["green"]["serving"]
				assert data["teams"]["yellow"]["serving"]
				singles.score(match, "yellow")

			# 20 - 15
			for i in range(0, 5):
				data = singles.matchData(match)
				assert data["teams"]["green"]["serving"]
				assert not data["teams"]["yellow"]["serving"]
				singles.score(match, "blue")

			# 20 - 20
			for i in range(0, 5):
				data = singles.matchData(match)
				assert data["teams"]["green"]["serving"]
				assert not data["teams"]["yellow"]["serving"]
				singles.score(match, "red")

			# 21 - 20
			singles.score(match, "yellow")
			data = singles.matchData(match)
			assert data["teams"]["green"]["serving"]

			# 21 - 21
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["teams"]["green"]["serving"]

			# 21 - 22
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["teams"]["yellow"]["serving"]

			# 22 - 22
			singles.score(match, "yellow")
			data = singles.matchData(match)
			assert data["teams"]["green"]["serving"]

			# 23 - 22
			singles.score(match, "yellow")
			data = singles.matchData(match)
			assert data["teams"]["green"]["serving"]

			# 23 - 23
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["teams"]["yellow"]["serving"]

			# 23 - 24
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["teams"]["yellow"]["serving"]

			# 24 - 24
			singles.score(match, "yellow")
			data = singles.matchData(match)
			assert data["teams"]["yellow"]["serving"]

			# 25 - 24
			singles.score(match, "yellow")
			data = singles.matchData(match)
			assert data["teams"]["green"]["serving"]

			# 25 - 25
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["teams"]["green"]["serving"]

			# 25 - 26
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["teams"]["yellow"]["serving"]

			# 25 - 27 - Winner
			singles.score(match, "green")
			data = singles.matchData(match)
			assert data["complete"]
