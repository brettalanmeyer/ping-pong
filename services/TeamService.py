import Service
from models import TeamModel
from services import PlayerService
from datetime import datetime
from flask import current_app as app

class TeamService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, TeamModel.TeamModel)
		self.playerService = PlayerService.PlayerService(session)

	def selectById(self, id):
		app.logger.info("Selecting team=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def create(self, matchId):
		team = self.model(matchId, datetime.now(), datetime.now())
		self.session.add(team)
		self.session.commit()

		app.logger.info("Creating team=%d match=%d", team.id, team.matchId)

		return team

	def createOnePlayer(self, matchId, playerId):
		team = self.create(matchId)
		team.players.append(self.playerService.selectById(playerId))

		app.logger.info("Creating single player team=%d match=%d player=%d", team.id, matchId, playerId)

		return team

	def createTwoPlayer(self, matchId, player1Id, player2Id):
		team = self.create(matchId)
		team.players.append(self.playerService.selectById(player1Id))
		team.players.append(self.playerService.selectById(player2Id))
		self.session.commit()

		app.logger.info("Creating two player team=%d match=%d player1=%d player2=%d", team.id, matchId, player1Id, player2Id)

		return team

	def win(self, team):
		self.status(team, True)

	def lose(self, team):
		self.status(team, False)

	def status(self, team, win):
		team.win = win
		team.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Team win=%s team=%d", win, team.id)