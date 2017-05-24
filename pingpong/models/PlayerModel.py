from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class PlayerModel(Base):

	__tablename__ = "players"

	id = Column(Integer, primary_key = True)
	officeId = Column(Integer, ForeignKey("offices.id"))
	name = Column(String)
	avatar = Column(String)
	extension = Column(String)
	enabled = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	office = relationship("OfficeModel")

	def __init__(self, officeId, name, enabled, createdAt, modifiedAt):
		self.officeId = officeId
		self.name = name
		self.enabled = enabled
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isEnabled(self):
		return self.enabled == 1