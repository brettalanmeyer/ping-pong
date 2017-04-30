from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
import random

singles = Singles()
matchService = MatchService()
playerService = PlayerService()

class TestSingles(BaseTest):

	def createMatch(self, numOfGames):
		with self.request:
			player1 = playerService.create({ "name": "Han" })
			player2 = playerService.create({ "name": "Chewie " })

			match = matchService.create("singles")
			matchService.updateGames(match.id, numOfGames)

			singles.createTeams(match, [player1.id, player2.id], True)
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
			assert data["points"] == 0

	def test_oneSet(self):
		with self.ctx:
			match = self.createMatch(5)

			for i in range(0, 21):
				singles.score(match, "green")

			data = singles.matchData(match)

			assert match.game == 2
			assert not data["complete"]
			assert data["game"] == 2

	def test_twoSets(self):
		with self.ctx:
			match = self.createMatch(5)

			for i in range(0, 42):
				singles.score(match, "green")

			data = singles.matchData(match)

			assert match.game == 3
			assert not data["complete"]
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

	def test_undoScore(self):
		pass

	def test_undoMatch(self):
		pass

	def test_playAgain(self):
		pass
