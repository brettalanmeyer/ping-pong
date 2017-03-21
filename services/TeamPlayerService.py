import Service
from models import TeamPlayerModel
from flask import current_app as app

class TeamPlayerService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, TeamPlayerModel.TeamPlayerModel)

	def create(self, teamId, playerId):
		teamPlayer = self.model(teamId, playerId)
		self.session.add(teamPlayer)
		self.session.commit()

		app.logger.info("Creating teamplayer=%d team=%d player=%d", teamPlayer.id, teamPlayer.teamId, teamPlayer.playerId)

		return teamPlayer
