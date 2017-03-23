import MatchType

class Doubles(MatchType.MatchType):

	def __init__(self, session):
		MatchType.MatchType.__init__(self, session, "Doubles", "doubles", "matches/four-player.html", "matches/doubles.html", 21)

	def matchData(self, match):
		game = match.games[match.game - 1]

		data = {
			"matchId": match.id,
			"matchType": self.matchType,
			"playTo": match.playTo,
			"numOfGames": match.numOfGames,
			"game": match.game,
			"template": self.matchTemplate,
			"complete": match.complete == 1,
			"teams": {
				"north": self.newTeam(),
				"south": self.newTeam()
			},
			"players": {},
			"points": 0
		}

		for color in self.colors:
			data["players"][color] = self.newPlayer(getattr(game, color))

		data["points"] = data["teams"]["north"]["points"] + data["teams"]["south"]["points"]

		self.setTeamData(match, data["players"], data["teams"])
		self.determineWinner(match, data["teams"])
		self.determineServe(data["points"], data["players"])

		return data

	def newTeam(self):
		return {
			"teamId": None,
			"points": 0,
			"winner": False,
			"players": [],
			"games": []
		}

	def newPlayer(self, playerId):
		return {
			"playerId": playerId,
			"teamPlayerId": None,
			"playerName": None,
			"serving": False
		}

	def setTeamData(self, match, players, teams):
		for team in match.teams:

			points = self.scoreService.getScore(match.id, team.id, match.game)

			for teamPlayer in team.teamPlayers:
				if players["green"]["playerId"] == teamPlayer.player.id:
					color = "green"
					teams["north"]["teamId"] = team.id
					teams["north"]["points"] = points
					teams["north"]["players"].append(teamPlayer.player.name)
					teams["north"]["winner"] = (team.win == 1)

				elif players["yellow"]["playerId"] == teamPlayer.player.id:
					color = "yellow"
					teams["south"]["teamId"] = team.id
					teams["south"]["points"] = points
					teams["south"]["players"].append(teamPlayer.player.name)
					teams["south"]["winner"] = (team.win == 1)

				elif players["blue"]["playerId"] == teamPlayer.player.id:
					color = "blue"
					teams["south"]["players"].append(teamPlayer.player.name)

				elif players["red"]["playerId"] == teamPlayer.player.id:
					color = "red"
					teams["north"]["players"].append(teamPlayer.player.name)

				players[color]["playerName"] = teamPlayer.player.name
				players[color]["teamId"] = team.id

	def determineWinner(self, match, teams):
		for game in match.games:
			if game.winner == teams["north"]["teamId"]:
				winner = teams["north"]
				loser = teams["south"]
			else:
				loser = teams["north"]
				winner = teams["south"]

			winner["games"].append({
				"win": None if game.winner == None else True,
				"score": game.winnerScore
			})
			loser["games"].append({
				"win": None if game.winner == None else False,
				"score": game.loserScore
			})

	def determineServe(self, points, players):

		# green serves first and swaps after serving is complete
		if (points - 5) % 20 < 10:
			green = players["green"]
			red = players["red"]
			players["green"] = red
			players["red"] = green

		# blue serves second and swaps after serving is complete
		if (points) % 20 >= 10:
			yellow = players["yellow"]
			blue = players["blue"]
			players["yellow"] = blue
			players["blue"] = yellow

		if points % 10 < 5:
			players["green"]["serving"] = True
		else:
			players["blue"]["serving"] = True

	def determineGameWinner(self, match):
		data = self.matchData(match)
		north = data["teams"]["north"]
		south = data["teams"]["south"]

		northWin = north["points"] >= data["playTo"] and north["points"] >= south["points"] + 2
		southWin = south["points"] >= data["playTo"] and south["points"] >= north["points"] + 2

		if northWin or southWin:
			if northWin:
				winner = north["teamId"]
				winnerScore = north["points"]
				loser = south["teamId"]
				loserScore = south["points"]
			elif southWin:
				winner = south["teamId"]
				winnerScore = south["points"]
				loser = north["teamId"]
				loserScore = north["points"]

			self.gameService.complete(data["matchId"], data["game"], winner, winnerScore, loser, loserScore)

			if match.game < match.numOfGames:
				self.matchService.updateGame(match.id, match.game + 1)

	def createTeams(self, match, data):
		green = data["green"]
		yellow = data["yellow"]
		blue = data["blue"]
		red = data["red"]

		team1 = self.teamService.createTwoPlayer(match.id, green, red)
		team2 = self.teamService.createTwoPlayer(match.id, yellow, blue)

		for i in range(0, match.numOfGames):

			# Game 1
			# B  A
			# C  D
			if i % 4 == 0:
				a = green
				b = yellow
				c = blue
				d = red

			# Game 2
			# A  B
			# D  C
			elif i % 4 == 1:
				a = yellow
				b = green
				c = red
				d = blue

			# Game 3
			# C  D
			# B  A
			elif i % 4 == 2:
				a = red
				b = blue
				c = yellow
				d = green

			# Game 4
			# D  C
			# A  B
			elif i % 4 == 3:
				a = blue
				b = red
				c = green
				d = yellow

			self.gameService.create(match.id, i + 1, a, b, c, d)

	def score(self, match, button):
		data = self.matchData(match)

		if button == "green" or button == "red":
			teamId = data["teams"]["north"]["teamId"]
		elif button == "yellow" or button == "blue":
			teamId = data["teams"]["south"]["teamId"]

		self.scoreService.score(match.id, teamId, match.game)

		self.determineGameWinner(match)
		self.determineMatchWinner(match)

		return self.matchData(match)

