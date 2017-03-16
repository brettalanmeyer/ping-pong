import Service, logging
from models import GameModel
from datetime import datetime
from sqlalchemy import text

logger = logging.getLogger(__name__)

class LeaderboardService(Service.Service):

	def __init__(self, session):
		logger.info("Initializing Leaderboard Service")
		Service.Service.__init__(self, session, None)

	def stats(self):
		return []