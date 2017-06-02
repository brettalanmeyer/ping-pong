from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class IsmModel(Base):

	__tablename__ = "isms"

	id = Column(Integer, primary_key = True)
	officeId = Column(Integer, ForeignKey("offices.id"))
	left = Column(Integer)
	right = Column(Integer)
	saying = Column(String)
	approved = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	office = relationship("OfficeModel")

	def __init__(self, officeId, left, right, saying, approved, createdAt, modifiedAt):
		self.officeId = officeId
		self.left = left
		self.right = right
		self.saying = saying
		self.approved = approved
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isApproved(self):
		return self.approved == 1

