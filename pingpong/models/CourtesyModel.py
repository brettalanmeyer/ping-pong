from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class CourtesyModel(Base):

	__tablename__ = "courtesies"

	id = Column(Integer, primary_key = True)
	officeId = Column(Integer, ForeignKey("offices.id"))
	text = Column(String)
	file = Column(String)
	approved = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	office = relationship("OfficeModel")

	def __init__(self, officeId, text, file, approved, createdAt, modifiedAt):
		self.officeId = officeId
		self.text = text
		self.file = file
		self.approved = approved
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isApproved(self):
		return self.approved == 1

