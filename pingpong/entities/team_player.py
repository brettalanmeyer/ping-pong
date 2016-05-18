from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from base import Base

class TeamPlayer(Base):

	__tablename__ = "teams_players"

	id = Column(Integer, primary_key = True)
	teamId = Column(Integer, ForeignKey("teams.id"))
	playerId = Column(Integer, ForeignKey("players.id"))

	team = relationship("Team")
	player = relationship("Player")

	def __init__(self, teamId, playerId):
		self.teamId = teamId
		self.playerId = playerId
