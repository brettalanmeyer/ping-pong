from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class GameModel(Base):

	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	game = Column(Integer)
	green = Column(Integer, ForeignKey("players.id"))
	yellow = Column(Integer, ForeignKey("players.id"))
	blue = Column(Integer, ForeignKey("players.id"))
	red = Column(Integer, ForeignKey("players.id"))
	winner = Column(Integer, ForeignKey("teams.id"))
	winnerScore = Column(Integer)
	loser = Column(Integer, ForeignKey("teams.id"))
	loserScore = Column(Integer)
	createdAt = Column(DateTime)
	completedAt = Column(DateTime)

	match = relationship("MatchModel")

	def __init__(self, matchId, game, green, yellow, blue, red, createdAt):
		self.matchId = matchId
		self.game = game
		self.green = green
		self.yellow = yellow
		self.blue = blue
		self.red = red
		self.createdAt = createdAt
