from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class OfficeModel(Base):

	__tablename__ = "offices"

	id = Column(Integer, primary_key = True)
	city = Column(String)
	state = Column(String)
	enabled = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, city, state, enabled, createdAt, modifiedAt):
		self.name = name
		self.enabled = enabled
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isEnabled(self):
		return self.enabled == 1