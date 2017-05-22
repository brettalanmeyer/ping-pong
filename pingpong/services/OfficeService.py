from flask import current_app as app
from pingpong.models.OfficeModel import OfficeModel
from pingpong.services.Service import Service
from pingpong.utils import database as db

class OfficeService(Service):

	def select(self):
		app.logger.info("Selecting offices")

		return db.session.query(OfficeModel)

	def selectActive(self):
		app.logger.info("Selecting offices")

		return db.session.query(OfficeModel).filter(OfficeModel.enabled == 1)

	def load(self):
		offices = self.selectActive();

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
