from pingpong.services.MatchService import MatchService
from pingpong.services.GameService import GameService
from pingpong.services.TeamService import TeamService
from pingpong.services.ScoreService import ScoreService
import math

gameService = GameService()
matchService = MatchService()
scoreService = ScoreService()
teamService = TeamService()

class MatchType():

	def __init__(self, label, matchType, matchTemplate, defaultPoints, numOfPlayers, numOfTeams):
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
		score = scoreService.selectLastScoreByMatchId(match.id)

		if score != None:

			completed = match.complete

			if completed:
				matchService.incomplete(match)
				for team in match.teams:
					teamService.status(team, None)

			if completed or score.game != match.game:
				gameService.resetGame(match.id, score.game)
				matchService.updateGame(match.id, score.game)

			scoreService.delete(score)

		return self.matchData(match)

	def determineMatchWinner(self, match):
		team1 = match.teams[0]
		team2 = match.teams[1]

		team1Wins = self.getTeamWins(match.id, team1.id)
		team2Wins = self.getTeamWins(match.id, team2.id)

		gamesNeededToWinMatch = int(math.ceil(float(match.numOfGames) / 2.0))

		if team1Wins == gamesNeededToWinMatch:
			teamService.win(team1)
			teamService.lose(team2)
			matchService.complete(match)
			self.sendWinningMessage(match, team1, team1Wins, team2, team2Wins)
		elif team2Wins == gamesNeededToWinMatch:
			teamService.win(team2)
			teamService.lose(team1)
			matchService.complete(match)
			self.sendWinningMessage(match, team2, team2Wins, team1, team1Wins)

	def getTeamWins(self, matchId, teamId):
		return gameService.getTeamWins(matchId, teamId)
