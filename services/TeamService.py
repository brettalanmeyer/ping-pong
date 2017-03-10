import Service
from models import TeamModel
from services import TeamPlayerService
from datetime import datetime

class TeamService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, TeamModel.TeamModel)
		self.teamPlayerService = TeamPlayerService.TeamPlayerService(session)

	def create(self, matchId):
		team = self.model(matchId, datetime.now(), datetime.now())
		self.session.add(team)
		self.session.commit()
		return team

	def createOnePlayer(self, matchId, playerId):
		team = self.create(matchId)
		teamPlayer = self.teamPlayerService.create(team.id, playerId)
		return team

	def createTwoPlayer(self, matchId, player1Id, player2Id):
		team = self.create(matchId)
		teamPlayer1 = self.teamPlayerService.create(team.id, player1Id)
		teamPlayer2 = self.teamPlayerService.create(team.id, player2Id)

		return team

	def win(self, team):
		team.win = True
		team.loss = False
		team.modifiedAt = datetime.now()
		self.session.commit()

	def lose(self, team):
		team.win = False
		team.loss = True
		team.modifiedAt = datetime.now()
		self.session.commit()
