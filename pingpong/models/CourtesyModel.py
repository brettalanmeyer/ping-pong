from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class CourtesyModel(Base):

	__tablename__ = "courtesies"

	id = Column(Integer, primary_key = True)
	officeId = Column(Integer, ForeignKey("offices.id"))
	text = Column(String)
	language = Column(String)
	slow = Column(Integer)
	file = Column(String)
	approved = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	office = relationship("OfficeModel")

	def __init__(self, officeId, text, language, slow, file, approved, createdAt, modifiedAt):
		self.officeId = officeId
		self.text = text
		self.language = language
		self.slow = slow
		self.file = file
		self.approved = approved
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def isSlow(self):
		return self.slow == 1 or self.slow == "1"

	def isApproved(self):
		return self.approved == 1 or self.approved == "1"

	def getLanguages(self):
		return [{
			"value": "zh",
			"label": "Chinese"
		}, {
			"value": "en-us",
			"label": "English (United States)"
		}, {
			"value": "en-uk",
			"label": "English (United Kingdom)"
		}, {
			"value": "en-au",
			"label": "English (Australia)"
		}, {
			"value": "fr",
			"label": "French"
		}, {
			"value": "de",
			"label": "German"
		}, {
			"value": "el",
			"label": "Greek"
		}, {
			"value": "it",
			"label": "Italian"
		}, {
			"value": "ja",
			"label": "Japanese"
		}, {
			"value": "ru",
			"label": "Russian"
		}, {
			"value": "es-es",
			"label": "Spanish"
		}]

	def getLanguageLabel(self):
		languages = self.getLanguages()

		for language in languages:
			if self.language == language["value"]:
				return language["label"]

		return None
