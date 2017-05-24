from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class OfficeModel(Base):

	__tablename__ = "offices"

	id = Column(Integer, primary_key = True)
	city = Column(String)
	state = Column(String)
	skypeChatId = Column(String)
	hash = Column(String)
	enabled = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, city, state, skypeChatId, hash, enabled, createdAt, modifiedAt):
		self.city = city
		self.state = state
		self.skypeChatId = skypeChatId
		self.hash = hash
		self.enabled = enabled
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isEnabled(self):
		return self.enabled == 1
