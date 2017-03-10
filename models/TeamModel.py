from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class TeamModel(Base):

	__tablename__ = "teams"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	win = Column(Integer)
	loss = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	match = relationship("MatchModel")
	teamPlayers = relationship("TeamPlayerModel", backref = "TeamModel.id")

	def __init__(self, matchId, createdAt, modifiedAt):
		self.matchId = matchId
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt
