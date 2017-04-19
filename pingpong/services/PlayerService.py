from datetime import datetime
from flask import current_app as app
from pingpong.models.PlayerModel import PlayerModel
from pingpong.services.Service import Service
from pingpong.utils import database as db

class PlayerService(Service):

	def select(self):
		app.logger.info("Selecting players")

		return db.session.query(PlayerModel).order_by(PlayerModel.name)

	def selectById(self, id):
		app.logger.info("Selecting player=%d", id)

		players = db.session.query(PlayerModel).filter(PlayerModel.id == id)

		if players.count() == 0:
			return None

		return players.one()

	def	selectActive(self):
		app.logger.info("Selecting active players")

		return db.session.query(PlayerModel).filter(PlayerModel.enabled == 1).order_by(PlayerModel.name)

	def selectByName(self, name):
		app.logger.info("Selecting player by name=%s", name)

		return db.session.query(PlayerModel).filter_by(name = name)

	def new(self):
		app.logger.info("New player")

		return PlayerModel("", True, None, None)

	def create(self, form):
		player = PlayerModel(form["name"], True, datetime.now(), datetime.now())
		db.session.add(player)
		db.session.commit()

		app.logger.info("Creating player=%d name=%s", player.id, player.name)

		return player

	def update(self, id, name):
		player = self.selectById(id)
		player.name = name
		player.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating player=%d name=%s", player.id, player.name)

		return player

	def excludeByName(self, id, name):
		app.logger.info("Selecting player=%d not by name=%s", id, name)

		return db.session.query(PlayerModel).filter(PlayerModel.id != id, PlayerModel.name == name)

