from flask import request
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.GameService import GameService
from pingpong.services.MatchService import MatchService
from pingpong.services.ScoreService import ScoreService
from pingpong.services.TeamService import TeamService
from pingpong.utils import notifications
from pingpong.utils import util

gameService = GameService()
matchService = MatchService()
scoreService = ScoreService()
teamService = TeamService()

class Singles(MatchType):

	def __init__(self):
		MatchType.__init__(self, "Singles", "singles", "matches/singles.html", 21, 2, 2)

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
				"green": self.newPlayer(game.green),
				"yellow": self.newPlayer(game.yellow)
			},
			"points": 0
		}

		self.setPlayerData(match, data["teams"])
		data["points"] = data["teams"]["green"]["points"] + data["teams"]["yellow"]["points"]
		self.determineWinner(match, data["teams"])
		self.determineServe(data)

		return data

	def newPlayer(self, playerId):
		return {
			"teamId": None,
			"playerId": playerId,
			"playerName": None,
			"points": None,
			"serving": False,
			"winner": False,
			"games": []
		}

	def setPlayerData(self, match, teams):
		for team in match.teams:
			for player in team.players:

				points = scoreService.getScore(match.id, team.id, match.game)

				color = "green"
				if teams["yellow"]["playerId"] == player.id:
					color = "yellow"

				teams[color]["playerName"] = player.name
				teams[color]["points"] = points
				teams[color]["teamId"] = team.id
				teams[color]["winner"] = (team.win == 1)

	def determineWinner(self, match, teams):
		for game in match.games:
			if game.winner == teams["green"]["teamId"]:
				winner = teams["green"]
				loser = teams["yellow"]
			else:
				loser = teams["green"]
				winner = teams["yellow"]

			winner["games"].append({
				"win": None if game.winner == None else True,
				"score": game.winnerScore
			})

			loser["games"].append({
				"win": None if game.winner == None else False,
				"score": game.loserScore
			})

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

			gameService.complete(data["matchId"], data["game"], winner, winnerScore, loser, loserScore)

			self.determineMatchWinner(match)

			if not match.complete and data["game"] < data["numOfGames"]:
				matchService.updateGame(match.id, match.game + 1)

	def score(self, match, button):
		data = self.matchData(match)

		if button == "green" or button == "red":
			teamId = data["teams"]["green"]["teamId"]
		elif button == "yellow" or button == "blue":
			teamId = data["teams"]["yellow"]["teamId"]

		scoreService.score(match.id, teamId, match.game)

		self.determineGameWinner(match)

		return self.matchData(match)

	def createTeams(self, match, data, randomize):
		if randomize:
			ids = util.shuffle(map(int, data))
		else:
			ids = map(int, data)

		team1 = teamService.createOnePlayer(match.id, ids[0])
		team2 = teamService.createOnePlayer(match.id, ids[1])

		for i in range(1, match.numOfGames + 1):

			if i % 2 == 1:
				green = ids[0]
				yellow = ids[1]
			else:
				green = ids[1]
				yellow = ids[0]

			gameService.create(match.id, i, green, yellow, None, None)

	def play(self, match):
		matchService.play(match)

		player1 = match.teams[0].players[0]
		player2 = match.teams[1].players[0]

		message = '<a href="{}matches/{}">{} is playing {} in a best of {}</a>'.format(request.url_root, match.id, player1.name, player2.name, match.numOfGames)

		notifications.send(message)

	def playAgain(self, match, numOfGames, persistTeams):
		game = match.games[0]
		playerIds = [game.green, game.yellow]

		newMatch = matchService.create(self.matchType)
		newMatch.numOfGames = numOfGames
		newMatch.game = 1
		self.createTeams(newMatch, playerIds, True)
		matchService.play(newMatch)

		return newMatch

	def sendWinningMessage(self, match, winningTeam, winningSets, losingTeam, losingSets):
		winnerPlayer = winningTeam.players[0]
		losingPlayer = losingTeam.players[0]

		message = "<b>{}</b> defeated {}, {} - {}".format(winnerPlayer.name, losingPlayer.name, winningSets, losingSets)

		winnerScores = "\n"
		loserScores = "\n"

		for game in match.games:
			if game.completedAt == None:
				continue

			if game.winner == winningTeam.id:
				winnerScores += "<b>{}</b>\t\t\t".format(game.winnerScore)
				loserScores += "{}\t\t\t".format(game.loserScore)
			else:
				winnerScores += "{}\t\t\t".format(game.loserScore)
				loserScores += "<b>{}</b>\t\t\t".format(game.winnerScore)

		message += winnerScores
		message += loserScores

		notifications.send(message)
