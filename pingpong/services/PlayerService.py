from datetime import datetime
from flask import current_app as app
from pingpong.models.PlayerModel import PlayerModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from sqlalchemy import exc

class PlayerService(Service):

	def select(self):
		app.logger.info("Selecting players")

		return db.session.query(PlayerModel).order_by(PlayerModel.name)

	def selectCount(self):
		app.logger.info("Selecting number of players")

		return self.select().count()

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

	def selectByNameExcludingPlayer(self, id, name):
		app.logger.info("Selecting player=%d not by name=%s", id, name)

		return db.session.query(PlayerModel).filter(PlayerModel.id != id, PlayerModel.name == name)

	def new(self):
		app.logger.info("New player")

		return PlayerModel("", True, None, None)

	def create(self, form):
		player = PlayerModel(form["name"], True, datetime.now(), datetime.now())
		db.session.add(player)
		db.session.commit()

		app.logger.info("Creating player=%d name=%s", player.id, player.name)

		return player

	def update(self, id, form):
		player = self.selectById(id)
		player.name = form["name"]
		player.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating player=%d name=%s", player.id, player.name)

		return player

	def enable(self, player):
		app.logger.info("Enabling player=%d", player.id)

		player.enabled = True
		player.modifiedAt = datetime.now()
		db.session.commit()

		return player

	def disable(self, player):
		app.logger.info("Enabling player=%d", player.id)

		player.enabled = False
		player.modifiedAt = datetime.now()
		db.session.commit()

		return player

	def avatar(self, player, name, extension):
		app.logger.info("Setting avatar for player=%d", player.id)

		player.avatar = name
		player.extension = extension
		player.modifiedAt = datetime.now()
		db.session.commit()

		return player

	def deleteById(self, id):
		app.logger.info("Deleting player by id=%d", id)
		player = self.selectById(id)
		return self.delete(player)

	def delete(self, player):
		app.logger.info("Deleting player=%d", player.id)

		try:
			db.session.delete(player)
			db.session.commit()
			return player, True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return player, False

	def deleteAll(self):
		app.logger.info("Deleting all players")

		try:
			db.session.query(PlayerModel).delete()
			db.session.commit()
			return True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return False
