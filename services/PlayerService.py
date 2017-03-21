import Service
from models import PlayerModel
from datetime import datetime
from flask import current_app as app

class PlayerService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, PlayerModel.PlayerModel)

	def select(self):
		app.logger.info("Selecting players")

		return self.session.query(self.model).order_by(self.model.name)

	def selectById(self, id):
		app.logger.info("Selecting player=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def selectByName(self, name):
		app.logger.info("Selecting player by name=%s", name)

		return self.session.query(self.model).filter_by(name = name)

	def new(self):
		app.logger.info("New player")

		return self.model("", None, None)

	def create(self, form):
		player = self.model(form["name"], datetime.now(), datetime.now())
		self.session.add(player)
		self.session.commit()

		app.logger.info("Creating player=%d name=%s", player.id, player.name)

		return player

	def update(self, id, name):
		player = self.selectById(id)
		player.name = name
		player.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Updating player=%d name=%s", player.id, player.name)

		return player

	def excludeByName(self, id, name):
		app.logger.info("Selecting player=%d not by name=%s", id, name)

		return self.session.query(self.model).filter(self.model.id != id, self.model.name == name)

