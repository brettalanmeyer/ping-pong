from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class MatchModel(Base):

	__tablename__ = "matches"

	id = Column(Integer, primary_key = True)
	officeId = Column(Integer, ForeignKey("offices.id"))
	matchType = Column(String)
	playTo = Column(Integer)
	numOfGames = Column(Integer)
	game = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	matchNum = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)
	completedAt = Column(DateTime)

	office = relationship("OfficeModel")

	teams = relationship("TeamModel", cascade = "all, delete-orphan")
	games = relationship("GameModel", cascade = "all, delete-orphan")
	scores = relationship("ScoreModel", cascade = "all, delete-orphan")

	def __init__(self, officeId, matchType, playTo, game, ready, complete, matchNum, createdAt, modifiedAt):
		self.officeId = officeId
		self.matchType = matchType
		self.playTo = playTo
		self.game = game
		self.ready = ready
		self.complete = complete
		self.matchNum = matchNum
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
