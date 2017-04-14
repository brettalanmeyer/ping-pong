from pingpong.services.MatchService import MatchService
from pingpong.services.GameService import GameService
from pingpong.services.TeamService import TeamService
from pingpong.services.ScoreService import ScoreService
import math

class MatchType():

	def __init__(self, label, matchType, matchTemplate, defaultPoints, numOfPlayers, numOfTeams):
		self.matchService = MatchService()
		self.gameService = GameService()
		self.teamService = TeamService()
		self.scoreService = ScoreService()

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

			completed = match.complete

			if completed:
				self.matchService.incomplete(match)
				for team in match.teams:
					self.teamService.status(team, None)

			if completed or score.game != match.game:
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
			self.sendWinningMessage(match, team1, team1Wins, team2, team2Wins)
		elif team2Wins == gamesNeededToWinMatch:
			self.teamService.win(team2)
			self.teamService.lose(team1)
			self.matchService.complete(match)
			self.sendWinningMessage(match, team2, team2Wins, team1, team1Wins)

	def getTeamWins(self, matchId, teamId):
		return self.gameService.getTeamWins(matchId, teamId)
