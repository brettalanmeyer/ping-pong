import Service, logging
from models import GameModel
from datetime import datetime
from sqlalchemy import text

class LeaderboardService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, None)

	def stats(self):
		return []