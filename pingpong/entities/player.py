from sqlalchemy import create_engine, Column, Integer, String, DateTime
from base import Base

class Player(Base):

	__tablename__ = "players"

	id = Column(Integer, primary_key = True)
	name = Column(String)
	createdAt = Column(DateTime)

	def __init__(self, name, createdAt):
		self.name = name
		self.createdAt = createdAt
