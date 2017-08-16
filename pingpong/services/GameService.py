from datetime import datetime
from flask import current_app as app
from pingpong.models.GameModel import GameModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import text
import json

class GameService(Service):

	def select(self):
		app.logger.info("Selecting games")

		return db.session.query(GameModel)

	def selectCount(self):
		app.logger.info("Selecting number of games")

		return self.select().count()

	def create(self, matchId, game, green, yellow, blue, red):
		app.logger.info("Creating game for matchId=%d", matchId)

		game = GameModel(matchId, game, green, yellow, blue, red, datetime.now(), datetime.now())
		db.session.add(game)
		db.session.commit()

		return game

	def complete(self, matchId, game, winner, winnerScore, loser, loserScore, completedAt = None):
		app.logger.info("Setting matchId=%d and game=%d as complete", matchId, game)

		existingGame = db.session.query(GameModel).filter_by(matchId = matchId, game = game).one()
		existingGame.winner = winner
		existingGame.winnerScore = winnerScore
		existingGame.loser = loser
		existingGame.loserScore = loserScore
		existingGame.modifiedAt = datetime.now()

		if completedAt == None:
			existingGame.completedAt = datetime.now()
		else:
			existingGame.completedAt = completedAt

		db.session.commit()

		return existingGame

	def resetGame(self, matchId, game):
		app.logger.info("Resetting complete game to incomplete for matchId=%d and game=%d", matchId, game)

		games = db.session.query(GameModel).filter_by(matchId = matchId, game = game)

		if games.count() == 1:
			game = games.one()
			game.winner = None
			game.winnerScore = None
			game.loser = None
			game.loserScore = None
			game.completedAt = None
			db.session.commit()

			return game

		return None

	def getTeamWins(self, matchId, teamId):
		app.logger.info("Getting wins for matchId=%d and teamId=%d", matchId, teamId)

		query = "\
			SELECT COUNT(*) as wins\
			FROM games\
			WHERE matchId = :matchId AND winner = :teamId\
		"
		connection = db.session.connection()
		data = connection.execute(text(query), matchId = matchId, teamId = teamId).first()

		if data == None:
			return 0

		return int(data.wins)
