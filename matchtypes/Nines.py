import MatchType

class Nines(MatchType.MatchType):

	def __init__(self):
		MatchType.MatchType.__init__(self, "9s", "nines", "matches/four-player.html", "matches/nines.html", 9)

	def matchData(self, match):
		game = match.games[0]

		colors = ["green", "yellow", "blue", "red"]

		data = {
			"matchId": match.id,
			"matchType": self.matchType,
			"playTo": match.playTo,
			"template": self.matchTemplate,
			"complete": match.complete == 1,
			"createdAt": str(match.createdAt),
			"completedAt": str(match.completedAt),
			"players": {
				"green": {
					"playerId": game.green,
					"teamId": None,
					"teamPlayerId": None,
					"playerName": None,
					"points": match.playTo
				},
				"yellow": {
					"playerId": game.yellow,
					"teamId": None,
					"teamPlayerId": None,
					"playerName": None,
					"points": match.playTo
				},
				"blue": {
					"playerId": game.blue,
					"teamId": None,
					"teamPlayerId": None,
					"playerName": None,
					"points": match.playTo
				},
				"red": {
					"playerId": game.red,
					"teamId": None,
					"teamPlayerId": None,
					"playerName": None,
					"points": match.playTo
				}
			}
		}

		for team in match.teams:

			points = self.scoreService.getScore(match.id, team.id, match.game)

			for teamPlayer in team.teamPlayers:
				for color in colors:
					if data["players"][color]["playerId"] == teamPlayer.player.id:
						data["players"][color]["teamId"] = team.id
						data["players"][color]["teamPlayerId"] = teamPlayer.id
						data["players"][color]["playerName"] = teamPlayer.player.name
						data["players"][color]["points"] -= points

		return data

	def createTeams(self, match, data):
		team1 = self.teamService.createOnePlayer(match.id, data["green"])
		team2 = self.teamService.createOnePlayer(match.id, data["yellow"])
		team3 = self.teamService.createOnePlayer(match.id, data["blue"])
		team4 = self.teamService.createOnePlayer(match.id, data["red"])

		self.gameService.create(match.id, 0, data["green"], data["yellow"], data["blue"], data["red"])

	def score(self, match, button):
		data = self.matchData(match)

		player = data["players"][button]

		if player["points"] > 0:
			self.scoreService.score(match.id, player["teamId"], match.game)

		return self.matchData(match)

