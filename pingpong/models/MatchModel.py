from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class MatchModel(Base):

	__tablename__ = "matches"

	id = Column(Integer, primary_key = True)
	matchType = Column(String)
	playTo = Column(Integer)
	numOfGames = Column(Integer)
	game = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)
	completedAt = Column(DateTime)

	teams = relationship("TeamModel", cascade = "all, delete-orphan")
	games = relationship("GameModel", cascade = "all, delete-orphan")
	scores = relationship("ScoreModel", cascade = "all, delete-orphan")

	def __init__(self, matchType, playTo, game, ready, complete, createdAt, modifiedAt):
		self.matchType = matchType
		self.playTo = playTo
		self.game = game
		self.ready = ready
		self.complete = complete
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isReady(self):
		return self.ready == 1

	def isComplete(self):
		return self.complete == 1

	def hasTeams(self):
		return len(self.teams) > 0

	def hasGames(self):
		return len(self.games) > 0
