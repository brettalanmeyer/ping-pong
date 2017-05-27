from datetime import datetime
from flask import current_app as app
from pingpong.models.OfficeModel import OfficeModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util

class OfficeService(Service):

	def select(self):
		app.logger.info("Selecting offices")

		return db.session.query(OfficeModel)

	def selectActive(self):
		app.logger.info("Selecting offices")

		return db.session.query(OfficeModel).filter(OfficeModel.enabled == 1)

	def selectById(self, id):
		app.logger.info("Selecting office=%d", id)

		offices = db.session.query(OfficeModel).filter(OfficeModel.id == id)

		if offices.count() == 0:
			return None

		return offices.one()

	def selectByHash(self, hash):
		offices = db.session.query(OfficeModel).filter(OfficeModel.hash == hash)

		if offices.count() == 0:
			return None

		return offices.one()

	def new(self):
		app.logger.info("New office")

		return OfficeModel("", "", "", "", 1, None, None)

	def create(self, form):
		office = OfficeModel(form["city"], form["state"], form["skypeChatId"], util.generateUUID(), True, datetime.now(), datetime.now())
		db.session.add(office)
		db.session.commit()

		app.logger.info("Creating office=%s city=%s state=%s skypeChatId=%s", office.id, office.city, office.state, office.skypeChatId)

		return office

	def update(self, id, form):
		office = self.selectById(id)
		office.city = form["city"]
		office.state = form["state"]
		office.skypeChatId = form["skypeChatId"]
		office.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating office=%s city=%s state=%s skypeChatId=%s", office.id, office.city, office.state, office.skypeChatId)

		return office

	def enable(self, office):
		app.logger.info("Enabling office=%d", office.id)

		office.enabled = True
		office.modifiedAt = datetime.now()
		db.session.commit()

		return office

	def disable(self, office):
		app.logger.info("Disabling office=%d", office.id)

		office.enabled = False
		office.modifiedAt = datetime.now()
		db.session.commit()

		return office

	def deleteById(self, id):
		app.logger.info("Deleting office by id=%d", id)
		office = self.selectById(id)
		return self.delete(office)

	def delete(self, office):
		app.logger.info("Deleting office=%d", office.id)

		try:
			db.session.delete(office)
			db.session.commit()
			return office, True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return office, False

	def load(self):
		offices = self.selectActive()

		data = []

		for office in offices:
			data.append({
				"id": office.id,
				"city": office.city,
				"state": office.state,
				"enabled": office.enabled,
				"createdAt": office.createdAt,
				"modifiedAt": office.modifiedAt
			})

		return data
