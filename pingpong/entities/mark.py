from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mark(Base):

	__tablename__ = "marks"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer)
	teamId = Column(Integer)
	playerId = Column(Integer)
	game = Column(Integer)
	round = Column(Integer)
	value = Column(Integer)
	createdAt = Column(DateTime)
