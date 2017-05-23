from datetime import datetime
from flask import current_app as app
from pingpong.models.IsmModel import IsmModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import exc
import json

class IsmService(Service):

	def select(self):
		app.logger.info("Selecting isms")

		return db.session.query(IsmModel)

	def selectApproved(self):
		app.logger.info("Selecting approved isms")

		return db.session.query(IsmModel).filter(IsmModel.approved == True)

	def selectCount(self):
		app.logger.info("Selecting number of isms")

		return self.select().count()

	def selectById(self, id):
		app.logger.info("Selecting ism=%d", id)

		isms = db.session.query(IsmModel).filter(IsmModel.id == id)

		if isms.count() == 0:
			return None

		return isms.one()

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

	def approve(self, ism):
		app.logger.info("Enabling ism=%d", ism.id)

		ism.approved = True
		ism.modifiedAt = datetime.now()
		db.session.commit()

		return ism

	def reject(self, ism):
		app.logger.info("Enabling ism=%d", ism.id)

		ism.approved = False
		ism.modifiedAt = datetime.now()
		db.session.commit()

		return ism

	def deleteById(self, id):
		app.logger.info("Deleting ism by id=%d", id)
		ism = self.selectById(id)
		return self.delete(ism)

	def delete(self, ism):
		app.logger.info("Deleting ism=%d", ism.id)

		try:
			db.session.delete(ism)
			db.session.commit()
			return ism, True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return ism, False

	def deleteAll(self):
		app.logger.info("Deleting all isms")

		try:
			db.session.query(IsmModel).delete()
			db.session.commit()
			return True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return False

	def serialize(self, isms):
		app.logger.info("Serializing isms")

		data = []

		for ism in isms:
			data.append({
				"id": ism.id,
				"left": ism.left,
				"right": ism.right,
				"saying": ism.saying,
				"approved": ism.isApproved(),
				"createdAt": ism.createdAt,
				"modifiedAt": ism.modifiedAt
			})

		return json.dumps(data, default = util.jsonSerial)
