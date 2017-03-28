import Service
from models import ScoreModel, MatchModel
from sqlalchemy import text
from datetime import datetime
from flask import current_app as app

class ScoreService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, ScoreModel.ScoreModel)

	def score(self, matchId, teamId, game):
		score = self.model(matchId, teamId, game, datetime.now())
		self.session.add(score)
		self.session.commit()

		app.logger.info("Scoring for match=%d team=%d game=%d", matchId, teamId, game)

	def selectCount(self):
		return self.session.query(self.model.matchId).count()

	def undo(self, matchId):
		score = self.session.query(self.model).filter(self.model.matchId == matchId).order_by(self.model.id.desc()).first()
		if score != None:
			self.session.query(self.model).filter(self.model.id == score.id).delete()
			self.session.commit()

		app.logger.info("Undo score for match=%d", matchId)

	def getScore(self, matchId, teamId, game):
		app.logger.info("Getting score for match=%d team=%d game=%d", matchId, teamId, game)

		query = "\
			SELECT COUNT(*) as points\
			FROM scores\
			WHERE matchId = :matchId AND teamId = :teamId AND game = :game\
			GROUP BY matchId, teamId, game\
		"
		connection = self.session.connection()
		data = connection.execute(text(query), matchId = matchId, teamId = teamId, game = game).first()

		if data == None:
			return 0

		return int(data.points)

	def deleteByMatch(self, matchId):
		app.logger.info("Delete all scores for match=%d", matchId)

		self.session.query(self.model).filter(self.model.matchId == matchId).delete()
		self.session.commit()
