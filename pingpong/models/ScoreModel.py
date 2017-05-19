from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class ScoreModel(Base):

	__tablename__ = "scores"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	teamId = Column(Integer, ForeignKey("teams.id"))
	game = Column(Integer)
	createdAt = Column(DateTime)

	match = relationship("MatchModel")

	def __init__(self, matchId, teamId, game, createdAt):
		self.matchId = matchId
		self.teamId = teamId
		self.game = game
		self.createdAt = createdAt
