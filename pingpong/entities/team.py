from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Team(Base):

	__tablename__ = "teams"

	id = Column(Integer, primary_key = True)
	gameId = Column(Integer)
	playerId = Column(Integer)
	team = Column(Integer)
	createdAt = Column(DateTime)

	def __init__(self, gameId, playerId, team, createdAt):
		self.gameId = gameId
		self.playerId = playerId
		self.team = team
		self.createdAt = createdAt
