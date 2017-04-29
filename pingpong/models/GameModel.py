from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class GameModel(Base):

	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	game = Column(Integer)
	greenId = Column(Integer, ForeignKey("players.id"))
	yellowId = Column(Integer, ForeignKey("players.id"))
	blueId = Column(Integer, ForeignKey("players.id"))
	redId = Column(Integer, ForeignKey("players.id"))
	winner = Column(Integer, ForeignKey("teams.id"))
	winnerScore = Column(Integer)
	loser = Column(Integer, ForeignKey("teams.id"))
	loserScore = Column(Integer)
	completedAt = Column(DateTime)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	match = relationship("MatchModel")
	green = relationship("PlayerModel", foreign_keys = [greenId])
	yellow = relationship("PlayerModel", foreign_keys = [yellowId])
	blue = relationship("PlayerModel", foreign_keys = [blueId])
	red = relationship("PlayerModel", foreign_keys = [redId])

	def __init__(self, matchId, game, greenId, yellowId, blueId, redId, createdAt, modifiedAt):
		self.matchId = matchId
		self.game = game
		self.greenId = greenId
		self.yellowId = yellowId
		self.blueId = blueId
		self.redId = redId
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt
