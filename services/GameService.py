from Service import Service
from models.GameModel import GameModel
from datetime import datetime
from sqlalchemy import text
from flask import current_app as app

class GameService(Service):

	def __init__(self, session):
		Service.__init__(self, session)

	def create(self, matchId, game, green, yellow, blue, red):
		app.logger.info("Creating game for match=%d", matchId)

		game = GameModel(matchId, game, green, yellow, blue, red, datetime.now(), datetime.now())
		self.session.add(game)
		self.session.commit()

		return game

	def complete(self, matchId, game, winner, winnerScore, loser, loserScore):
		app.logger.info("Setting match=%d and game=%d as complete", matchId, game)

		existingGame = self.session.query(GameModel).filter_by(matchId = matchId, game = game).one()
		existingGame.winner = winner
		existingGame.winnerScore = winnerScore
		existingGame.loser = loser
		existingGame.loserScore = loserScore
		existingGame.modifiedAt = datetime.now()
		existingGame.completedAt = datetime.now()
		self.session.commit()

	def resetGame(self, matchId, game):
		games = self.session.query(GameModel).filter_by(matchId = matchId, game = game)

		if games.count() == 1:
			game = games.one()
			game.winner = None
			game.winnerScore = None
			game.loser = None
			game.loserScore = None
			game.completedAt = None
			self.session.commit()

	def getTeamWins(self, matchId, teamId):
		app.logger.info("Getting wins for match=%d and team=%d", matchId, teamId)

		query = "\
			SELECT COUNT(*) as wins\
			FROM games\
			WHERE matchId = :matchId AND winner = :teamId\
		"
		connection = self.session.connection()
		data = connection.execute(text(query), matchId = matchId, teamId = teamId).first()

		if data == None:
			return 0

		return int(data.wins)
