import Service
from models import TeamPlayerModel

class TeamPlayerService(Service.Service):

	def __init__(self):
		Service.Service.__init__(self, TeamPlayerModel.TeamPlayerModel)

	def create(self, teamId, playerId):
		teamPlayer = self.model(teamId, playerId)
		self.session.add(teamPlayer)
		self.session.commit()

		return teamPlayer
