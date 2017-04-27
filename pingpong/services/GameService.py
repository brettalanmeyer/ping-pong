from datetime import datetime
from flask import current_app as app
from pingpong.models.GameModel import GameModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from sqlalchemy import text

class GameService(Service):

	def select(self):
		app.logger.info("Selecting games")

		return db.session.query(GameModel)

	def selectCount(self):
		app.logger.info("Selecting number of games")

		return self.select().count()

	def create(self, matchId, game, green, yellow, blue, red):
		app.logger.info("Creating game for match=%d", matchId)

		game = GameModel(matchId, game, green, yellow, blue, red, datetime.now(), datetime.now())
		db.session.add(game)
		db.session.commit()

		return game

	def complete(self, matchId, game, winner, winnerScore, loser, loserScore):
		app.logger.info("Setting match=%d and game=%d as complete", matchId, game)

		existingGame = db.session.query(GameModel).filter_by(matchId = matchId, game = game).one()
		existingGame.winner = winner
		existingGame.winnerScore = winnerScore
		existingGame.loser = loser
		existingGame.loserScore = loserScore
		existingGame.modifiedAt = datetime.now()
		existingGame.completedAt = datetime.now()
		db.session.commit()

	def resetGame(self, matchId, game):
		games = db.session.query(GameModel).filter_by(matchId = matchId, game = game)

		if games.count() == 1:
			game = games.one()
			game.winner = None
			game.winnerScore = None
			game.loser = None
			game.loserScore = None
			game.completedAt = None
			db.session.commit()

	def getTeamWins(self, matchId, teamId):
		app.logger.info("Getting wins for match=%d and team=%d", matchId, teamId)

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
