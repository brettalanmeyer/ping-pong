import MatchType

class Singles(MatchType.MatchType):

	def __init__(self, session):
		MatchType.MatchType.__init__(self, session, "Singles", "singles", "matches/two-player.html", "matches/singles.html", 21)

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
			"createdAt": str(match.createdAt),
			"completedAt": str(match.completedAt),
			"teams": {
				"green": {
					"teamId": None,
					"playerId": game.green,
					"playerName": None,
					"points": None,
					"serving": False,
					"winner": False,
					"games": []
				},
				"yellow": {
					"teamId": None,
					"playerId": game.yellow,
					"playerName": None,
					"points": None,
					"serving": False,
					"winner": False,
					"games": []
				}
			},
			"points": 0
		}

		for team in match.teams:
			for teamPlayer in team.teamPlayers:

				points = self.scoreService.getScore(match.id, team.id, match.game)
				data["points"] += points

				color = "green"
				if data["teams"]["yellow"]["playerId"] == teamPlayer.player.id:
					color = "yellow"

				data["teams"][color]["playerName"] = teamPlayer.player.name
				data["teams"][color]["points"] = points
				data["teams"][color]["teamId"] = team.id
				data["teams"][color]["winner"] = team.win == 1

		for game in match.games:
			if game.winner == data["teams"]["green"]["teamId"]:
				winner = data["teams"]["green"]
				loser = data["teams"]["yellow"]
			else:
				loser = data["teams"]["green"]
				winner = data["teams"]["yellow"]

			winner["games"].append({
				"win": None if game.winner == None else True,
				"score": game.winnerScore
			})
			loser["games"].append({
				"win": None if game.winner == None else False,
				"score": game.loserScore
			})

		self.determineServe(data)

		return data

	def determineServe(self, data):

		# swap every 5 turns
		if data["points"] % 10 < 5:
			self.setServer(data, "green")
		else:
			self.setServer(data, "yellow")

		# possible game point
		if data["teams"]["green"]["points"] >= data["playTo"] - 1 or data["teams"]["yellow"]["points"] >= data["playTo"] - 1:

			# if teams are tied, revert to default serving
			if data["teams"]["green"]["points"] == data["teams"]["yellow"]["points"]:
				pass

			elif data["teams"]["green"]["points"] > data["teams"]["yellow"]["points"]:
				self.setServer(data, "yellow")

			elif data["teams"]["yellow"]["points"] > data["teams"]["green"]["points"]:
				self.setServer(data, "green")

	def setServer(self, data, color):
		data["teams"]["green"]["serving"] = False
		data["teams"]["yellow"]["serving"] = False

		data["teams"][color]["serving"] = True

	def determineGameWinner(self, match):
		data = self.matchData(match)

		greenWin = data["teams"]["green"]["points"] >= data["playTo"] and data["teams"]["green"]["points"] >= data["teams"]["yellow"]["points"] + 2
		yellowWin = data["teams"]["yellow"]["points"] >= data["playTo"] and data["teams"]["yellow"]["points"] >= data["teams"]["green"]["points"] + 2

		if greenWin or yellowWin:
			if greenWin:
				winner = data["teams"]["green"]["teamId"]
				winnerScore = data["teams"]["green"]["points"]
				loser = data["teams"]["yellow"]["teamId"]
				loserScore = data["teams"]["yellow"]["points"]
			elif yellowWin:
				winner = data["teams"]["yellow"]["teamId"]
				winnerScore = data["teams"]["yellow"]["points"]
				loser = data["teams"]["green"]["teamId"]
				loserScore = data["teams"]["green"]["points"]

			self.gameService.complete(data["matchId"], data["game"], winner, winnerScore, loser, loserScore)

			if data["game"] < data["numOfGames"]:
				self.matchService.updateGame(match.id, match.game + 1)

	def score(self, match, button):
		data = self.matchData(match)

		if button == "green" or button == "red":
			teamId = data["teams"]["green"]["teamId"]
		elif button == "yellow" or button == "blue":
			teamId = data["teams"]["yellow"]["teamId"]

		self.scoreService.score(match.id, teamId, match.game)

		self.determineGameWinner(match)
		self.determineMatchWinner(match)

		return self.matchData(match)

	def createTeams(self, match, data):
		team1 = self.teamService.createOnePlayer(match.id, data["green"])
		team2 = self.teamService.createOnePlayer(match.id, data["yellow"])

		for i in range(1, match.numOfGames + 1):

			if i % 2 == 1:
				green = data["green"]
				yellow = data["yellow"]
			else:
				green = data["yellow"]
				yellow = data["green"]

			self.gameService.create(match.id, i, green, yellow, None, None)

