from sqlalchemy import Table, Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class TeamModel(Base):

	__tablename__ = "teams"

	associationTable = Table("teams_players", Base.metadata,
		Column("teamId", Integer, ForeignKey("teams.id"), primary_key = True),
		Column("playerId", Integer, ForeignKey("players.id"), primary_key = True)
	)

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	win = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	match = relationship("MatchModel")
	players = relationship("PlayerModel", secondary = associationTable)

	def __init__(self, matchId, createdAt, modifiedAt):
		self.matchId = matchId
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt
