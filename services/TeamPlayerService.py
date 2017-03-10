import Service
from models import TeamPlayerModel

class TeamPlayerService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, TeamPlayerModel.TeamPlayerModel)

	def create(self, teamId, playerId):
		teamPlayer = self.model(teamId, playerId)
		self.session.add(teamPlayer)
		self.session.commit()

		return teamPlayer
