from BaseTest import BaseTest
from pingpong.matchtypes.Nines import Nines
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
import collections
import random

nines = Nines()
matchService = MatchService()
playerService = PlayerService()

class TestNines(BaseTest):

	def createMatch(self):
		office = self.office()

		with self.request:
			player1 = playerService.create(office["id"], { "name": "Han" })
			player2 = playerService.create(office["id"], { "name": "Chewie" })
			player3 = playerService.create(office["id"], { "name": "Luke" })
			player4 = playerService.create(office["id"], { "name": "Leia" })

			match = matchService.create(office["id"], "nines")
			nines.createTeams(match, [player1.id, player2.id, player3.id, player4.id], True)
			nines.play(match)

			return match

	def test_createMatch(self):
		with self.ctx:
			match = self.createMatch()

			assert match.matchType == "nines"
			assert match.playTo == 9
			assert match.numOfGames == None
			assert match.game == 0
			assert match.ready == 1
			assert match.complete == 0
			assert match.completedAt == None

			data = nines.matchData(match)

			assert data["matchId"] == match.id
			assert data["matchType"] == match.matchType
			assert data["playTo"] == match.playTo
			assert data["template"] == nines.matchTemplate
			assert not data["complete"]
			assert data["ready"]
			assert data["createdAt"] != None
			assert data["completedAt"] == None

	def test_winner(self):
		with self.request:
			match = self.createMatch()

			for i in range(0, 9):
				nines.score(match, "green")
				nines.score(match, "yellow")
				nines.score(match, "red")

			data = nines.matchData(match)

			assert data["matchId"] == match.id
			assert data["complete"]
			assert data["completedAt"] != None

			blue = data["players"]["blue"]
			green = data["players"]["green"]
			yellow = data["players"]["yellow"]
			red = data["players"]["red"]

			assert blue["winner"]
			assert not green["winner"]
			assert not yellow["winner"]
			assert not red["winner"]

			assert blue["points"] == 9
			assert green["points"] == 0
			assert yellow["points"] == 0
			assert red["points"] == 0

			assert not blue["out"]
			assert green["out"]
			assert yellow["out"]
			assert red["out"]

	def test_matchJson(self):
		with self.ctx:
			match = self.createMatch()
			rv = self.app.get("/matches/{}.json".format(match.id))
			assert rv.status == self.ok

	def test_undoScore(self):
		with self.ctx:
			match = self.createMatch()

			nines.score(match, "green")
			nines.score(match, "green")
			nines.score(match, "red")
			nines.score(match, "red")
			nines.score(match, "red")

			data = nines.matchData(match)
			assert data["matchId"] == match.id
			assert data["players"]["green"]["points"] == 7
			assert data["players"]["red"]["points"] == 6

			nines.undo(match, "red")
			data = nines.matchData(match)
			assert data["players"]["green"]["points"] == 7
			assert data["players"]["red"]["points"] == 7

			nines.undo(match, "green")
			data = nines.matchData(match)
			assert data["players"]["green"]["points"] == 7
			assert data["players"]["red"]["points"] == 8

			nines.undo(match, "red")
			data = nines.matchData(match)
			assert data["players"]["green"]["points"] == 7
			assert data["players"]["red"]["points"] == 9

			nines.undo(match, "red")
			nines.undo(match, "yellow")
			data = nines.matchData(match)
			assert data["players"]["green"]["points"] == 9
			assert data["players"]["red"]["points"] == 9

	def test_undoMatch(self):
		with self.request:
			match = self.createMatch()

			for i in range(0, 21):
				nines.score(match, "green")
				nines.score(match, "yellow")
				nines.score(match, "blue")

			data = nines.matchData(match)
			assert data["complete"]
			assert data["completedAt"] != None

			nines.undo(match, "red")
			data = nines.matchData(match)
			assert not data["complete"]
			assert data["completedAt"] == None

	def test_playAgain(self):
		with self.request:
			match = self.createMatch()

			for i in range(0, 21):
				nines.score(match, "yellow")
				nines.score(match, "blue")
				nines.score(match, "red")

			matchPlayers = []
			for team in match.teams:
				for player in team.players:
					matchPlayers.append(player)

			data = nines.matchData(match)
			assert data["complete"]

			newMatch = nines.playAgain(match, None, None)
			newData = nines.matchData(newMatch)

			newMatchPlayers = []
			for team in newMatch.teams:
				for player in team.players:
					newMatchPlayers.append(player)

			assert collections.Counter(matchPlayers) == collections.Counter(newMatchPlayers)
			assert newData["ready"]
			assert not newData["complete"]
			assert newData["completedAt"] == None

	def test_swapPlayers(self):
		with self.request:
			match = self.createMatch()

			# both players are out on one side
			for i in range(0, 9):
				nines.score(match, "green")
				nines.score(match, "red")

			# blue will go to green/red side vs yellow which is now yellow and blue
			for i in range(0, 9):
				nines.score(match, "green" if i % 2 == 0 else "red")

			data = nines.matchData(match)

			assert data["complete"]
			assert data["completedAt"] != None

			blue = data["players"]["blue"]
			green = data["players"]["green"]
			yellow = data["players"]["yellow"]
			red = data["players"]["red"]

			assert not blue["winner"]
			assert not green["winner"]
			assert yellow["winner"]
			assert not red["winner"]

	def test_swapPlayersAgain(self):
		with self.request:
			match = self.createMatch()

			# both players are out on one side
			for i in range(0, 9):
				nines.score(match, "yellow")
				nines.score(match, "blue")

			# red goes to other side
			for i in range(0, 9):
				nines.score(match, "green" if i % 2 == 0 else "red")

			data = nines.matchData(match)

			assert data["complete"]
			assert data["completedAt"] != None

			blue = data["players"]["blue"]
			green = data["players"]["green"]
			yellow = data["players"]["yellow"]
			red = data["players"]["red"]

			assert not blue["winner"]
			assert not green["winner"]
			assert not yellow["winner"]
			assert red["winner"]
