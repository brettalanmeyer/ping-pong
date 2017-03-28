from services import MatchService, GameService, TeamService, ScoreService, PlayerService
import math

class MatchType():

	def __init__(self, session, label, matchType, playerTemplate, matchTemplate, defaultPoints):
		self.matchService = MatchService.MatchService(session)
		self.gameService = GameService.GameService(session)
		self.teamService = TeamService.TeamService(session)
		self.scoreService = ScoreService.ScoreService(session)

		self.label = label
		self.matchType = matchType
		self.playerTemplate = playerTemplate
		self.matchTemplate = matchTemplate
		self.defaultPoints = defaultPoints

		self.matchTypes = ["singles", "doubles", "nines"]
		self.colors = ["green", "yellow", "blue", "red"]

	def getLabel(self):
		return self.label

	def getMatchType(self):
		return self.matchType

	def getPlayerTemplate(self):
		return self.playerTemplate

	def getMatchTemplate(self):
		return self.matchTemplate

	def getDefaultPoints(self):
		return self.defaultPoints

	def isMatchType(self, matchType):
		return self.matchType == matchType

	def undo(self, match, button):
		self.scoreService.undo(match.id)
		return self.matchData(match)

	def determineMatchWinner(self, match):
		team1 = match.teams[0]
		team2 = match.teams[1]

		team1Wins = self.getTeamWins(match.id, team1.id)
		team2Wins = self.getTeamWins(match.id, team2.id)

		gamesNeededToWinMatch = int(math.ceil(float(match.numOfGames) / 2.0))

		if team1Wins == gamesNeededToWinMatch:
			self.teamService.win(team1)
			self.teamService.lose(team2)
			self.matchService.complete(match)
		elif team2Wins == gamesNeededToWinMatch:
			self.teamService.win(team2)
			self.teamService.lose(team1)
			self.matchService.complete(match)

	def getTeamWins(self, matchId, teamId):
		return self.gameService.getTeamWins(matchId, teamId)

	def playAgain(self, match):
		return match