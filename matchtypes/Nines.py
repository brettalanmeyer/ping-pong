import MatchType, random

class Nines(MatchType.MatchType):

	def __init__(self, session):
		MatchType.MatchType.__init__(self, session, "9s", "nines", "matches/four-player.html", "matches/nines.html", 9)

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

			points = self.scoreService.getScore(match.id, team.id, match.game)

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

	def createTeams(self, match, data):
		team1 = self.teamService.createOnePlayer(match.id, data["green"])
		team2 = self.teamService.createOnePlayer(match.id, data["yellow"])
		team3 = self.teamService.createOnePlayer(match.id, data["blue"])
		team4 = self.teamService.createOnePlayer(match.id, data["red"])

		self.gameService.create(match.id, 0, data["green"], data["yellow"], data["blue"], data["red"])

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
			self.scoreService.score(match.id, player["teamId"], match.game)

		data = self.matchData(match)
		data = self.determineMatchWinner(match, data)

		return data

	def determineMatchWinner(self, match, data):
		if match.complete:
			return data

		hasWinner = False

		for color in self.colors:
			if data["players"][color]["winner"]:
				self.matchService.complete(match)
				hasWinner = True
				break

		if hasWinner:
			for color in self.colors:
				team = self.teamService.selectById(data["players"][color]["teamId"])

				if data["players"][color]["winner"]:
					self.teamService.win(team)
				else:
					self.teamService.lose(team)

			data = self.matchData(match)

		return data

	def playAgain(self, match):
		players = []
		for game in match.games:
			players.append(game.yellow)
			players.append(game.blue)
			players.append(game.red)
			players.append(game.green)

		random.shuffle(players)

		teams = {
			"green": players[0],
			"yellow": players[1],
			"blue": players[2],
			"red": players[3]
		}

		newMatch = self.matchService.create(self.matchType)
		self.matchService.updatePlayTo(newMatch.id, match.playTo)
		self.createTeams(newMatch, teams)
		self.matchService.play(newMatch)

		return newMatch