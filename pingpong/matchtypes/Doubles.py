from flask import request
from pingpong.matchtypes.BaseMatch import BaseMatch
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

class Doubles(BaseMatch):

	def __init__(self):
		BaseMatch.__init__(self, "Doubles", "doubles", "matches/doubles.html", 21, 4, 2)

	def matchData(self, match):
		game = match.games[match.game - 1]

		data = {
			"matchId": match.id,
			"matchType": self.matchType,
			"playTo": match.playTo,
			"numOfGames": match.numOfGames,
			"game": match.game,
			"template": self.matchTemplate,
			"complete": match.isComplete(),
			"ready": match.isReady(),
			"createdAt": util.date(match.createdAt),
			"completedAt": util.date(match.completedAt),
			"teams": {
				"north": self.newTeam(),
				"south": self.newTeam()
			},
			"players": {},
			"points": 0
		}

		for color in self.colors:
			data["players"][color] = self.newPlayer(getattr(game, color).id)

		data["points"] = self.setTeamData(match, data["players"], data["teams"])
		self.determineWinner(match, data["teams"])
		self.determineServe(data)

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
			"playerName": None,
			"playerAvatar": None,
			"serving": False
		}

	def setTeamData(self, match, players, teams):
		for team in match.teams:

			points = scoreService.getScore(match.id, team.id, match.game)

			for player in team.players:
				if players["green"]["playerId"] == player.id:
					color = "green"
					teams["north"]["teamId"] = team.id
					teams["north"]["points"] = points
					teams["north"]["players"].append(player.name)
					teams["north"]["winner"] = team.hasWon()

				elif players["yellow"]["playerId"] == player.id:
					color = "yellow"
					teams["south"]["teamId"] = team.id
					teams["south"]["points"] = points
					teams["south"]["players"].append(player.name)
					teams["south"]["winner"] = team.hasWon()

				elif players["blue"]["playerId"] == player.id:
					color = "blue"
					teams["south"]["players"].append(player.name)

				elif players["red"]["playerId"] == player.id:
					color = "red"
					teams["north"]["players"].append(player.name)

				players[color]["playerName"] = player.name
				players[color]["playerAvatar"] = player.avatar
				players[color]["teamId"] = team.id

		return teams["north"]["points"] + teams["south"]["points"]

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

	def determineServe(self, data):
		points = data["points"]
		players = data["players"]

		swapEvery = 2
		if data["playTo"] == 21:
			swapEvery = 5

		if (points - swapEvery) % (swapEvery * 4) < (swapEvery * 2):
			self.swapRedGreen(players)
		if points % (swapEvery * 4) >= (swapEvery * 2):
			self.swapBlueYellow(players)

		if points % (swapEvery * 2) < swapEvery:
			players["green"]["serving"] = True
		else:
			players["blue"]["serving"] = True

	def swapRedGreen(self, players):
		green = players["green"]
		red = players["red"]
		players["green"] = red
		players["red"] = green

	def swapBlueYellow(self, players):
		yellow = players["yellow"]
		blue = players["blue"]
		players["yellow"] = blue
		players["blue"] = yellow

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

			gameService.complete(data["matchId"], data["game"], winner, winnerScore, loser, loserScore)

			self.determineMatchWinner(match)

			if not match.complete and match.game < match.numOfGames:
				matchService.updateGame(match.id, match.game + 1)

	def createTeams(self, match, data, randomize):
		if randomize:
			ids = util.shuffle(map(int, data))
		else:
			ids = map(int, data)

		green = ids[0]
		yellow = ids[1]
		blue = ids[2]
		red = ids[3]

		team1 = teamService.createTwoPlayer(match.id, green, red)
		team2 = teamService.createTwoPlayer(match.id, yellow, blue)

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

			gameService.create(match.id, i + 1, a, b, c, d)

	def score(self, match, button):
		data = self.matchData(match)

		if button == "green" or button == "red":
			teamId = data["teams"]["north"]["teamId"]
		elif button == "yellow" or button == "blue":
			teamId = data["teams"]["south"]["teamId"]

		scoreService.score(match.id, teamId, match.game)

		self.determineGameWinner(match)

		return self.matchData(match)

	def play(self, match):
		matchService.play(match)

		t1p1 = match.teams[0].players[0]
		t1p2 = match.teams[0].players[1]
		t2p1 = match.teams[1].players[0]
		t2p2 = match.teams[1].players[1]

		message = '<a href="{}matches/{}">{} and {} are playing {} and {} in a best of {}</a>'.format(request.url_root, match.id, t1p1.name, t1p2.name, t2p1.name, t2p2.name, match.numOfGames)

		notifications.send(message, match.officeId)

	def playAgain(self, match, numOfGames, randomize):
		game = match.games[0]

		# put in this order so if teams are not randomized, they will at least swap sides
		playerIds = [game.yellow.id, game.green.id, game.red.id, game.blue.id]

		newMatch = matchService.create(match.officeId, self.matchType)
		newMatch.numOfGames = numOfGames
		newMatch.playTo = match.playTo
		newMatch.game = 1
		self.createTeams(newMatch, playerIds, randomize)
		matchService.play(newMatch)

		return newMatch

	def sendWinningMessage(self, match, winningTeam, winningSets, losingTeam, losingSets):
		winnerPlayer1 = winningTeam.players[0]
		winnerPlayer2 = winningTeam.players[1]
		losingPlayer1 = losingTeam.players[0]
		losingPlayer2 = losingTeam.players[1]

		message = "<b>{}</b> and <b>{}</b> defeated {} and {}, {} - {}".format(winnerPlayer1.name, winnerPlayer2.name, losingPlayer1.name, losingPlayer2.name, winningSets, losingSets)

		winnerScores = "\n"
		loserScores = "\n"

		for game in match.games:
			if game.completedAt == None:
				continue

			if game.winner == winningTeam.id:
				winnerScores += "<b>{}</b> \t".format(game.getFormattedWinnerScore())
				loserScores += "{} \t".format(game.getFormattedLoserScore())
			else:
				winnerScores += "{} \t".format(game.getFormattedLoserScore())
				loserScores += "<b>{}</b> \t".format(game.getFormattedWinnerScore())

		message += winnerScores
		message += loserScores

		message += '\n<a href="{}leaderboard/doubles">Leaderboard Standings</a>'.format(request.url_root)

		notifications.send(message, match.officeId)
