import Service, logging, os, uuid
from models import IsmModel
from datetime import datetime
from flask import current_app as app
from gtts import gTTS

class IsmService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, IsmModel.IsmModel)

	def select(self):
		app.logger.info("Selecting isms")

		return self.session.query(self.model).filter(self.model.approved == True)

	def selectById(self, id):
		app.logger.info("Selecting ism=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def new(self):
		app.logger.info("New ism")

		return self.model(0, 0, "", False, None, None)

	def create(self, form):
		ism = self.model(form["left"], form["right"], form["saying"], True, datetime.now(), datetime.now())
		self.session.add(ism)
		self.session.commit()

		app.logger.info("Creating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		ism.file = self.generateAudio(ism)
		self.session.commit()

		return ism

	def update(self, id, form):

		ism = self.selectById(id)
		ism.left = form["left"]
		ism.right = form["right"]
		ism.saying = form["saying"]
		ism.approved = True
		ism.modifiedAt = datetime.now()
		ism.file = self.generateAudio(ism)
		self.session.commit()

		app.logger.info("Updating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		return ism

	def delete(self, id):
		app.logger.info("Deleting ism=%d", id)

		ism = self.selectById(id)
		self.session.delete(ism)
		self.session.commit()

		return ism

	def serialize(self, isms):
		app.logger.info("Serializing isms")

		data = []

		for ism in isms:
			data.append({
				"id": int(ism.id),
				"left": int(ism.left),
				"right": int(ism.right),
				"saying": ism.saying,
				"file": ism.file
			})

		return data

	def generateAudio(self, ism):
		app.logger.info("Generating audio file for ism %d", ism.id)

		oldFile = ism.file
		newFile = "ism-audio-{}.mp3".format(uuid.uuid4())

		path = "static/isms/{}"
		oldPath = path.format(oldFile)
		newPath = path.format(newFile)

		if os.path.isfile(oldPath):
			os.remove(oldPath)

		app.logger.info("Generating ism audio file")
		tts = gTTS(text = ism.saying, lang = "en-us")
		tts.save(newPath)

		return newFile