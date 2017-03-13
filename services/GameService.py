import Service
from models import GameModel
from datetime import datetime
from sqlalchemy import text

class GameService(Service.Service):

	def __init__(self):
		Service.Service.__init__(self, GameModel.GameModel)

	def create(self, matchId, game, green, yellow, blue, red):
		game = self.model(matchId, game, green, yellow, blue, red, datetime.now(), datetime.now())
		self.session.add(game)
		self.session.commit()

		return game

	def complete(self, matchId, game, winner, winnerScore, loser, loserScore):
		existingGame = self.session.query(self.model).filter_by(matchId = matchId, game = game).one()
		existingGame.winner = winner
		existingGame.winnerScore = winnerScore
		existingGame.loser = loser
		existingGame.loserScore = loserScore
		existingGame.modifiedAt = datetime.now()
		existingGame.completedAt = datetime.now()
		self.session.commit()

	def getTeamWins(self, matchId, teamId):
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
