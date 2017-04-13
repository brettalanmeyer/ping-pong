from Service import Service
from models.PlayerModel import PlayerModel
from datetime import datetime
from flask import current_app as app

class PlayerService(Service):

	def __init__(self, session):
		Service.__init__(self, session)

	def select(self):
		app.logger.info("Selecting players")

		return self.session.query(PlayerModel).order_by(PlayerModel.name)

	def selectById(self, id):
		app.logger.info("Selecting player=%d", id)

		return self.session.query(PlayerModel).filter(PlayerModel.id == id).one()

	def	selectActive(self):
		app.logger.info("Selecting active players")

		return self.session.query(PlayerModel).filter(PlayerModel.enabled == 1).order_by(PlayerModel.name)

	def selectByName(self, name):
		app.logger.info("Selecting player by name=%s", name)

		return self.session.query(PlayerModel).filter_by(name = name)

	def new(self):
		app.logger.info("New player")

		return PlayerModel("", True, None, None)

	def create(self, form):
		player = PlayerModel(form["name"], True, datetime.now(), datetime.now())
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

		return self.session.query(PlayerModel).filter(PlayerModel.id != id, PlayerModel.name == name)

