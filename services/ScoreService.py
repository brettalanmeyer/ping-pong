import Service
from models import ScoreModel, MatchModel
from sqlalchemy import text
from datetime import datetime
from flask import current_app as app

class ScoreService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, ScoreModel.ScoreModel)

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def score(self, matchId, teamId, game):
		score = self.model(matchId, teamId, game, datetime.now())
		self.session.add(score)
		self.session.commit()

		app.logger.info("Scoring for match=%d team=%d game=%d", matchId, teamId, game)

	def selectCount(self):
		app.logger.info("Selecting number of scores")

		return self.session.query(self.model.matchId).count()

	def selectLastScoreByMatchId(self, matchId):
		scores = self.session.query(self.model).filter(self.model.matchId == matchId).order_by(self.model.id.desc())

		if scores.count() > 0:
			return scores.first()

		return None

	def delete(self, score):
		self.session.delete(score)
		self.session.commit()
		app.logger.info("Deleting score=%d", score.id)

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
