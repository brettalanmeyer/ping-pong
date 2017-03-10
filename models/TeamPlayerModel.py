from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class TeamPlayerModel(Base):

	__tablename__ = "teams_players"

	id = Column(Integer, primary_key = True)
	teamId = Column(Integer, ForeignKey("teams.id"))
	playerId = Column(Integer, ForeignKey("players.id"))

	team = relationship("TeamModel")
	player = relationship("PlayerModel")

	def __init__(self, teamId, playerId):
		self.teamId = teamId
		self.playerId = playerId
