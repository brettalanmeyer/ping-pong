from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class Game(Base):

	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	players = Column(Integer)
	playTo = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	completedAt = Column(DateTime)

	def __init__(self, createdAt):
		self.createdAt = createdAt
