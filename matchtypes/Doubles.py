import MatchType

class Doubles(MatchType.MatchType):

	def __init__(self):
		MatchType.MatchType.__init__(self, "Doubles", "doubles", "matches/four-player.html", "matches/doubles.html", 21)

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
				"north": {
					"teamId": None,
					"points": 0,
					"winner": False,
					"players": [],
					"games": []
				},
				"south": {
					"teamId": None,
					"points": 0,
					"winner": False,
					"players": [],
					"games": []
				}
			},
			"players": {
				"green": {
					"playerId": game.green,
					"teamPlayerId": None,
					"playerName": None,
					"serving": False
				},
				"yellow": {
					"playerId": game.yellow,
					"teamPlayerId": None,
					"playerName": None,
					"serving": False
				},
				"blue": {
					"playerId": game.blue,
					"teamPlayerId": None,
					"playerName": None,
					"serving": False
				},
				"red": {
					"playerId": game.red,
					"teamPlayerId": None,
					"playerName": None,
					"serving": False
				}
			},
			"points": 0
		}

		for team in match.teams:

			points = self.scoreService.getScore(match.id, team.id, match.game)
			data["points"] += points

			for teamPlayer in team.teamPlayers:
				if data["players"]["green"]["playerId"] == teamPlayer.player.id:
					color = "green"
					data["teams"]["north"]["teamId"] = team.id
					data["teams"]["north"]["points"] = points
					data["teams"]["north"]["players"].append(teamPlayer.player.name)

				elif data["players"]["yellow"]["playerId"] == teamPlayer.player.id:
					color = "yellow"
					data["teams"]["south"]["teamId"] = team.id
					data["teams"]["south"]["points"] = points
					data["teams"]["south"]["players"].append(teamPlayer.player.name)

				elif data["players"]["blue"]["playerId"] == teamPlayer.player.id:
					color = "blue"
					data["teams"]["south"]["players"].append(teamPlayer.player.name)

				elif data["players"]["red"]["playerId"] == teamPlayer.player.id:
					color = "red"
					data["teams"]["north"]["players"].append(teamPlayer.player.name)

				data["players"][color]["playerName"] = teamPlayer.player.name
				data["players"][color]["teamId"] = team.id

		for game in match.games:
			if game.winner == data["teams"]["north"]["teamId"]:
				winner = data["teams"]["north"]
				loser = data["teams"]["south"]
			else:
				loser = data["teams"]["north"]
				winner = data["teams"]["south"]

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

		# green serves first and swaps after serving is complete
		if (data["points"] - 5) % 20 < 10:
			green = data["players"]["green"]
			red = data["players"]["red"]
			data["players"]["green"] = red
			data["players"]["red"] = green

		# blue serves second and swaps after serving is complete
		if (data["points"]) % 20 >= 10:
			yellow = data["players"]["yellow"]
			blue = data["players"]["blue"]
			data["players"]["yellow"] = blue
			data["players"]["blue"] = yellow

		if data["points"] % 10 < 5:
			data["players"]["green"]["serving"] = True
		else:
			data["players"]["blue"]["serving"] = True

	def determineGameWinner(self, match):
		data = self.matchData(match)

		northWin = data["teams"]["north"]["points"] >= data["playTo"] and data["teams"]["north"]["points"] >= data["teams"]["south"]["points"] + 2
		southWin = data["teams"]["south"]["points"] >= data["playTo"] and data["teams"]["south"]["points"] >= data["teams"]["north"]["points"] + 2

		if northWin or southWin:
			if northWin:
				winner = data["teams"]["north"]["teamId"]
				winnerScore = data["teams"]["north"]["points"]
				loser = data["teams"]["south"]["teamId"]
				loserScore = data["teams"]["south"]["points"]
			elif southWin:
				winner = data["teams"]["south"]["teamId"]
				winnerScore = data["teams"]["south"]["points"]
				loser = data["teams"]["north"]["teamId"]
				loserScore = data["teams"]["north"]["points"]

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

