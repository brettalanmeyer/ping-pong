from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from base import Base

class Team(Base):

	__tablename__ = "teams"

	id = Column(Integer, primary_key = True)
	gameId = Column(Integer, ForeignKey("games.id"))
	score = Column(Integer)
	createdAt = Column(DateTime)

	game = relationship("Game")
	teamPlayers = relationship("TeamPlayer", back_populates = "team")


	def __init__(self, gameId, score, createdAt):
		self.gameId = gameId
		self.score = score
		self.createdAt = createdAt
