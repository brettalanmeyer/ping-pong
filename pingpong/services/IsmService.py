from datetime import datetime
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from pingpong.models.Model import IsmModel
import json

db = SQLAlchemy()

class IsmService():

	def select(self):
		app.logger.info("Selecting isms")

		return db.session.query(IsmModel).filter(IsmModel.approved == True)

	def selectById(self, id):
		app.logger.info("Selecting ism=%d", id)

		return db.session.query(IsmModel).filter(IsmModel.id == id).one()

	def new(self):
		app.logger.info("New ism")

		return IsmModel(0, 0, "", False, None, None)

	def create(self, form):
		ism = IsmModel(form["left"], form["right"], form["saying"], True, datetime.now(), datetime.now())
		db.session.add(ism)
		db.session.commit()

		app.logger.info("Creating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		return ism

	def update(self, id, form):

		ism = self.selectById(id)
		ism.left = form["left"]
		ism.right = form["right"]
		ism.saying = form["saying"]
		ism.approved = True
		ism.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		return ism

	def delete(self, id):
		app.logger.info("Deleting ism=%d", id)

		ism = self.selectById(id)
		db.session.delete(ism)
		db.session.commit()

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
