from datetime import datetime
from pingpong.utils.database import Base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

class OfficeModel(Base):

	__tablename__ = "offices"

	id = Column(Integer, primary_key = True)
	city = Column(String)
	state = Column(String)
	seasonYear = Column(String)
	seasonMonth = Column(String)
	skypeChatId = Column(String)
	key = Column(String)
	enabled = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, city, state, seasonYear, seasonMonth, skypeChatId, key, enabled, createdAt, modifiedAt):
		self.city = city
		self.state = state
		self.seasonYear = seasonYear
		self.seasonMonth = seasonMonth
		self.skypeChatId = skypeChatId
		self.key = key
		self.enabled = enabled
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def hasSkypeChatId(self):
		return self.skypeChatId != None and len(self.skypeChatId.strip()) > 0

	def isEnabled(self):
		return self.enabled == 1

	def formatSeason(self):
		if self.seasonYear != None and self.seasonMonth != None:
			return "{:%b %d, %Y}".format(datetime(self.seasonYear, self.seasonMonth, 1))

		return ""