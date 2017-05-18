from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class IsmModel(Base):

	__tablename__ = "isms"

	id = Column(Integer, primary_key = True)
	left = Column(Integer)
	right = Column(Integer)
	saying = Column(String)
	approved = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, left, right, saying, approved, createdAt, modifiedAt):
		self.left = left
		self.right = right
		self.saying = saying
		self.approved = approved
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isApproved(self):
		return self.approved == 1

