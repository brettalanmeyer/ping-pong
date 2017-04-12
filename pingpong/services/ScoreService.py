from datetime import datetime
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from pingpong.models.Model import MatchModel, ScoreModel
from sqlalchemy import text

db = SQLAlchemy()

class ScoreService():

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		return db.session.query(ScoreModel).filter(ScoreModel.id == id).one()

	def score(self, matchId, teamId, game):
		score = ScoreModel(matchId, teamId, game, datetime.now())
		db.session.add(score)
		db.session.commit()

		app.logger.info("Scoring for match=%d team=%d game=%d", matchId, teamId, game)

	def selectCount(self):
		app.logger.info("Selecting number of scores")

		return db.session.query(ScoreModel.matchId).count()

	def selectLastScoreByMatchId(self, matchId):
		scores = db.session.query(ScoreModel).filter(ScoreModel.matchId == matchId).order_by(ScoreModel.id.desc())

		if scores.count() > 0:
			return scores.first()

		return None

	def delete(self, score):
		db.session.delete(score)
		db.session.commit()
		app.logger.info("Deleting score=%d", score.id)

	def getScore(self, matchId, teamId, game):
		app.logger.info("Getting score for match=%d team=%d game=%d", matchId, teamId, game)

		query = "\
			SELECT COUNT(*) as points\
			FROM scores\
			WHERE matchId = :matchId AND teamId = :teamId AND game = :game\
			GROUP BY matchId, teamId, game\
		"
		connection = db.session.connection()
		data = connection.execute(text(query), matchId = matchId, teamId = teamId, game = game).first()

		if data == None:
			return 0

		return int(data.points)

	def deleteByMatch(self, matchId):
		app.logger.info("Delete all scores for match=%d", matchId)

		db.session.query(ScoreModel).filter(ScoreModel.matchId == matchId).delete()
		db.session.commit()
