from Service import Service
import json
from models.IsmModel import IsmModel
from datetime import datetime
from flask import current_app as app

class IsmService(Service):

	def __init__(self, session):
		Service.__init__(self, session)

	def select(self):
		app.logger.info("Selecting isms")

		return self.session.query(IsmModel).filter(IsmModel.approved == True)

	def selectById(self, id):
		app.logger.info("Selecting ism=%d", id)

		return self.session.query(IsmModel).filter(IsmModel.id == id).one()

	def new(self):
		app.logger.info("New ism")

		return IsmModel(0, 0, "", False, None, None)

	def create(self, form):
		ism = IsmModel(form["left"], form["right"], form["saying"], True, datetime.now(), datetime.now())
		self.session.add(ism)
		self.session.commit()

		app.logger.info("Creating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		return ism

	def update(self, id, form):

		ism = self.selectById(id)
		ism.left = form["left"]
		ism.right = form["right"]
		ism.saying = form["saying"]
		ism.approved = True
		ism.modifiedAt = datetime.now()
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
				"saying": ism.saying
			})

		return json.dumps(data)
