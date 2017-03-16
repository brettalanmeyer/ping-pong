import Service, logging
from models import TeamPlayerModel

logger = logging.getLogger(__name__)

class TeamPlayerService(Service.Service):

	def __init__(self, session):
		logger.info("Initializing TeamPlayer Service")
		Service.Service.__init__(self, session, TeamPlayerModel.TeamPlayerModel)

	def create(self, teamId, playerId):
		teamPlayer = self.model(teamId, playerId)
		self.session.add(teamPlayer)
		self.session.commit()

		logger.info("Creating teamplayer=%d team=%d player=%d", teamPlayer.id, teamPlayer.teamId, teamPlayer.playerId)

		return teamPlayer
