import Service
from models import TeamModel
from services import TeamPlayerService
from datetime import datetime
from flask import current_app as app

class TeamService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, TeamModel.TeamModel)
		self.teamPlayerService = TeamPlayerService.TeamPlayerService(session)

	def create(self, matchId):
		team = self.model(matchId, datetime.now(), datetime.now())
		self.session.add(team)
		self.session.commit()

		app.logger.info("Creating team=%d match=%d", team.id, team.matchId)

		return team

	def createOnePlayer(self, matchId, playerId):
		team = self.create(matchId)
		teamPlayer = self.teamPlayerService.create(team.id, playerId)

		app.logger.info("Creating single player team=%d match=%d teamPlayer=%d player=%d", team.id, matchId, teamPlayer.id, teamPlayer.playerId)

		return team

	def createTwoPlayer(self, matchId, player1Id, player2Id):
		team = self.create(matchId)
		teamPlayer1 = self.teamPlayerService.create(team.id, player1Id)
		teamPlayer2 = self.teamPlayerService.create(team.id, player2Id)

		app.logger.info("Creating two player team=%d match=%d teamPlayer1=%d player1=%d teamPlayer2=%d player2=%d", team.id, matchId, teamPlayer1.id, teamPlayer1.playerId, teamPlayer2.id, teamPlayer2.playerId)

		return team

	def win(self, team):
		team.win = True
		team.loss = False
		team.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Team win team=%d", team.id)

	def lose(self, team):
		team.win = False
		team.loss = True
		team.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Team loss team=%d", team.id)
