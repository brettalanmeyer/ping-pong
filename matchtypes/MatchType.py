from services import MatchService, GameService, TeamService, ScoreService, PlayerService
import math

class MatchType():

	def __init__(self, session, label, matchType, matchTemplate, defaultPoints, numOfPlayers, numOfTeams):
		self.matchService = MatchService.MatchService(session)
		self.gameService = GameService.GameService(session)
		self.teamService = TeamService.TeamService(session)
		self.scoreService = ScoreService.ScoreService(session)

		self.label = label
		self.matchType = matchType
		self.matchTemplate = matchTemplate
		self.defaultPoints = defaultPoints
		self.numOfPlayers = numOfPlayers
		self.numOfTeams = numOfTeams

		self.matchTypes = ["singles", "doubles", "nines"]
		self.colors = ["green", "yellow", "blue", "red"]

	def isMatchType(self, matchType):
		return self.matchType == matchType

	def undo(self, match, button):
		score = self.scoreService.selectLastScoreByMatchId(match.id)

		if score != None:
			if score.game != match.game:
				self.gameService.resetGame(match.id, score.game)
				self.matchService.updateGame(match.id, score.game)

			self.scoreService.delete(score)

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
