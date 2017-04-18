from flask import request
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.GameService import GameService
from pingpong.services.MatchService import MatchService
from pingpong.services.ScoreService import ScoreService
from pingpong.services.TeamService import TeamService
from pingpong.utils import notifications
import random

gameService = GameService()
matchService = MatchService()
scoreService = ScoreService()
teamService = TeamService()

class Nines(MatchType):

	def __init__(self):
		MatchType.__init__(self, "Nines", "nines", "matches/nines.html", 9, 4, 4)

	def matchData(self, match):
		game = match.games[0]

		data = {
			"matchId": match.id,
			"matchType": self.matchType,
			"playTo": match.playTo,
			"template": self.matchTemplate,
			"complete": match.complete == 1,
			"createdAt": str(match.createdAt),
			"completedAt": str(match.completedAt),
			"players": {}
		}

		for color in self.colors:
			data["players"][color] = self.newPlayer(getattr(game, color))

		self.setPlayerData(match, data["players"])
		self.swapPlayers(data["players"])
		self.determineWinner(data["players"])

		return data

	def newPlayer(self, playerId):
		return {
			"playerId": playerId,
			"teamId": None,
			"playerName": None,
			"points": 0,
			"winner": False,
			"out": False
		}

	def setPlayerData(self, match, players):
		for team in match.teams:

			points = scoreService.getScore(match.id, team.id, match.game)

			for player in team.players:
				for color in self.colors:
					if players[color]["playerId"] == player.id:
						players[color]["teamId"] = team.id
						players[color]["playerName"] = player.name
						players[color]["points"] = match.playTo - points
						players[color]["out"] = players[color]["points"] == 0

	def swapPlayers(self, players):
		# if both players on one side are out and neither on the other side are out, swap one player to the other side
		if players["green"]["out"] and players["red"]["out"]:
			if not players["yellow"]["out"] and not players["blue"]["out"]:
				a = players["green"]
				b = players["yellow"]
				c = players["blue"]
				d = players["red"]

				players["blue"] = a
				players["green"] = c

		if players["yellow"]["out"] and players["blue"]["out"]:
			if not players["green"]["out"] and not players["red"]["out"]:
				a = players["green"]
				b = players["yellow"]
				c = players["blue"]
				d = players["red"]

				players["red"] = b
				players["yellow"] = d

	def determineWinner(self, players):
		players["green"]["winner"] = players["yellow"]["out"] and players["blue"]["out"] and players["red"]["out"]
		players["yellow"]["winner"] = players["green"]["out"] and players["blue"]["out"] and players["red"]["out"]
		players["blue"]["winner"] = players["green"]["out"] and players["yellow"]["out"] and players["red"]["out"]
		players["red"]["winner"] = players["green"]["out"] and players["yellow"]["out"] and players["blue"]["out"]

	def createTeams(self, match, data, randomize):
		ids = map(int, data)

		if randomize:
			random.shuffle(ids)

		team1 = teamService.createOnePlayer(match.id, ids[0])
		team2 = teamService.createOnePlayer(match.id, ids[1])
		team3 = teamService.createOnePlayer(match.id, ids[2])
		team4 = teamService.createOnePlayer(match.id, ids[3])

		gameService.create(match.id, 0, ids[0], ids[1], ids[2], ids[3])

	def score(self, match, button):
		data = self.matchData(match)
		players = data["players"]
		player = players[button]

		# allow both buttons on each side to score for the other player if one of them is out
		if button == "green" or button == "red":
			if players["green"]["out"] and not players["red"]["out"]:
				player = players["red"]
			elif players["red"]["out"] and not players["green"]["out"]:
				player = players["green"]

		elif button == "yellow" or button == "blue":
			if players["yellow"]["out"] and not players["blue"]["out"]:
				player = players["blue"]
			elif players["blue"]["out"] and not players["yellow"]["out"]:
				player = players["yellow"]

		if player["points"] > 0:
			scoreService.score(match.id, player["teamId"], match.game)

		data = self.matchData(match)
		data = self.determineMatchWinner(match, data)

		return data

	def determineMatchWinner(self, match, data):
		if match.complete:
			return data

		hasWinner = False

		for color in self.colors:
			if data["players"][color]["winner"]:
				matchService.complete(match)
				hasWinner = True
				break

		if hasWinner:
			for color in self.colors:
				team = teamService.selectById(data["players"][color]["teamId"])

				if data["players"][color]["winner"]:
					teamService.win(team)
				else:
					teamService.lose(team)

			self.sendWinningMessage(match)

			data = self.matchData(match)

		return data

	def play(self, match):
		matchService.play(match)

		player1 = match.teams[0].players[0]
		player2 = match.teams[1].players[0]
		player3 = match.teams[2].players[0]
		player4 = match.teams[3].players[0]

		message = '<a href="{}matches/{}">{}, {}, {} and {} are playing nines</a>'.format(request.url_root, match.id, player1.name, player2.name, player3.name, player4.name)
		notifications.send(message)

	def playAgain(self, match, numOfGames, randomize):
		game = match.games[0]
		playerIds = [game.yellow, game.blue, game.red, game.green]

		newMatch = matchService.create(self.matchType)
		self.createTeams(newMatch, playerIds, True)
		matchService.play(newMatch)

		return newMatch

	def sendWinningMessage(self, match):
		winningTeam = None
		losingTeams = []

		for team in match.teams:
			if team.win:
				winningTeam = team
			else:
				losingTeams.append(team)

		player1 = winningTeam.players[0]
		player2 = losingTeams[0].players[0]
		player3 = losingTeams[1].players[0]
		player4 = losingTeams[2].players[0]

		message = "<b>{}</b> defeated {}, {}, and {} in nines".format(player1.name, player2.name, player3.name, player4.name)

		notifications.send(message)
