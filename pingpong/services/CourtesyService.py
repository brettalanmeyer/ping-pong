from datetime import datetime
from flask import current_app as app
from gtts import gTTS
from pingpong.models.CourtesyModel import CourtesyModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import exc
import json
import os
import uuid

class CourtesyService(Service):

	def select(self, officeId):
		app.logger.info("Selecting courtesies")

		return db.session.query(CourtesyModel).filter(CourtesyModel.officeId == officeId)

	def selectApproved(self, officeId):
		app.logger.info("Selecting approved courtesies")

		return db.session.query(CourtesyModel).filter(CourtesyModel.officeId == officeId, CourtesyModel.approved == True)

	def selectCount(self, officeId):
		app.logger.info("Selecting number of courtesies")

		return self.select(officeId).count()

	def selectById(self, id):
		app.logger.info("Selecting courtesy=%d", id)

		courtesies = db.session.query(CourtesyModel).filter(CourtesyModel.id == id)

		if courtesies.count() == 0:
			return None

		return courtesies.one()

	def new(self):
		app.logger.info("New courtesy")

		return CourtesyModel(None, "", "en-us", False, None, False, None, None)

	def create(self, officeId, form):
		courtesy = CourtesyModel(officeId, form["text"], form["language"], form["slow"], None, True, datetime.now(), datetime.now())
		db.session.add(courtesy)
		db.session.commit()

		app.logger.info("Creating courtesy=%d text=%s", courtesy.id, courtesy.text)

		courtesy.file = self.generateAudio(courtesy)
		db.session.commit()

		return courtesy

	def update(self, id, form):
		courtesy = self.selectById(id)
		courtesy.text = form["text"]
		courtesy.language = form["language"]
		courtesy.slow = form["slow"]
		courtesy.approved = True
		courtesy.modifiedAt = datetime.now()
		courtesy.file = self.generateAudio(courtesy)
		db.session.commit()

		app.logger.info("Updating courtesy=%d text=%s", courtesy.id, courtesy.text)

		return courtesy

	def approve(self, courtesy):
		app.logger.info("Enabling courtesy=%d", courtesy.id)

		courtesy.approved = True
		courtesy.modifiedAt = datetime.now()
		db.session.commit()

		return courtesy

	def reject(self, courtesy):
		app.logger.info("Enabling courtesy=%d", courtesy.id)

		courtesy.approved = False
		courtesy.modifiedAt = datetime.now()
		db.session.commit()

		return courtesy

	def deleteById(self, id):
		app.logger.info("Deleting courtesy by id=%d", id)
		courtesy = self.selectById(id)
		return self.delete(courtesy)

	def delete(self, courtesy):
		app.logger.info("Deleting courtesy=%d", courtesy.id)

		try:
			db.session.delete(courtesy)
			db.session.commit()
			self.deleteAudio(courtesy)
			return courtesy, True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return courtesy, False

	def serialize(self, courtesies):
		app.logger.info("Serializing courtesies")

		data = []

		for courtesy in courtesies:
			data.append({
				"id": courtesy.id,
				"text": courtesy.text,
				"file": courtesy.file,
				"path": "courtesies/{}".format(courtesy.file),
				"approved": courtesy.isApproved(),
				"createdAt": courtesy.createdAt,
				"modifiedAt": courtesy.modifiedAt
			})

		return json.dumps(data, default = util.jsonSerial)

	def deleteAudio(self, courtesy):
		app.logger.info("Deleting audio file for courtesy %d", courtesy.id)

		path = "pingpong/static/audio/courtesies/{}".format(courtesy.file)

		if os.path.isfile(path):
			os.remove(path)

	def generateAudio(self, courtesy):
		app.logger.info("Generating audio file for courtesy %d", courtesy.id)

		oldFile = courtesy.file
		newFile = "courtesy-audio-{}.mp3".format(uuid.uuid4())

		path = "pingpong/static/audio/courtesies/{}"
		oldPath = path.format(oldFile)
		newPath = path.format(newFile)

		if os.path.isfile(oldPath):
			os.remove(oldPath)

		app.logger.info("Generating courtesy audio file")
		tts = gTTS(text = courtesy.text, lang = courtesy.language, slow = courtesy.isSlow())
		tts.save(newPath)

		return newFile
