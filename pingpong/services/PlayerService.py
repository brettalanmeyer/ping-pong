from datetime import datetime
from flask import current_app as app
from flask import url_for
from pingpong.models.PlayerModel import PlayerModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import exc
import json

class PlayerService(Service):

	def select(self, officeId):
		app.logger.info("Selecting players")

		return db.session.query(PlayerModel).filter(PlayerModel.officeId == officeId).order_by(PlayerModel.name)

	def selectCount(self, officeId):
		app.logger.info("Selecting number of players")

		return self.select(officeId).count()

	def selectById(self, id):
		app.logger.info("Selecting player=%d", id)

		players = db.session.query(PlayerModel).filter(PlayerModel.id == id)

		if players.count() == 0:
			return None

		return players.one()

	def	selectActive(self, officeId):
		app.logger.info("Selecting active players")

		players = db.session.query(PlayerModel).filter(PlayerModel.enabled == 1, PlayerModel.officeId == officeId).order_by(PlayerModel.name)

		return players

	def selectByName(self, officeId, name):
		app.logger.info("Selecting player by name=%s", name)

		return db.session.query(PlayerModel).filter(PlayerModel.officeId == officeId).filter_by(name = name)

	def selectByNameExcludingPlayer(self, officeId, id, name):
		app.logger.info("Selecting player=%d not by name=%s", id, name)

		return db.session.query(PlayerModel).filter(PlayerModel.officeId == officeId, PlayerModel.id != id, PlayerModel.name == name)

	def new(self):
		app.logger.info("New player")

		return PlayerModel(None, "", True, None, None)

	def create(self, officeId, form):
		player = PlayerModel(officeId, form["name"], True, datetime.now(), datetime.now())
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
		app.logger.info("Disabling player=%d", player.id)

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

	def serialize(self, players):
		app.logger.info("Serializing players")

		data = []

		for player in players:
			playerData = {
				"id": int(player.id),
				"name": player.name,
				"avatar": player.avatar,
				"extension": player.extension,
				"avatarUrl": None,
				"enabled": player.isEnabled(),
				"createdAt": player.createdAt,
				"modifiedAt": player.modifiedAt
			}

			if player.avatar != None:
				playerData["avatarUrl"] = url_for('playerController.avatar', id = player.id, avatar = player.avatar)

			data.append(playerData)

		return json.dumps(data, default = util.jsonSerial)