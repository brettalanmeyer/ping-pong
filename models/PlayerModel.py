from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class PlayerModel(Base):

	__tablename__ = "players"

	id = Column(Integer, primary_key = True)
	name = Column(String)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, name, createdAt, modifiedAt):
		self.name = name
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt
