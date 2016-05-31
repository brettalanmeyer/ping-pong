from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from base import Base

class Game(Base):

	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	players = Column(Integer)
	playTo = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	completedAt = Column(DateTime)

	teams = relationship("Team", back_populates = "game")

	def __init__(self, createdAt):
		self.createdAt = createdAt
