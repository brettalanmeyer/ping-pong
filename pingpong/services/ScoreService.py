from datetime import datetime
from flask import current_app as app
from pingpong.models.MatchModel import MatchModel
from pingpong.models.ScoreModel import ScoreModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import text
import json

class ScoreService(Service):

	def select(self):
		app.logger.info("Selecting scores")

		return db.session.query(ScoreModel)

	def selectCount(self):
		app.logger.info("Selecting number of scores")

		return self.select().count()

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		return db.session.query(ScoreModel).filter(ScoreModel.id == id).one()

	def selectByMatch(self, match):
		return self.selectByMatchId(match.id)

	def selectByMatchId(self, matchId):
		app.logger.info("Selecting matchId=%d", matchId)

		return db.session.query(ScoreModel).filter(ScoreModel.matchId == matchId)

	def score(self, matchId, teamId, game):
		score = ScoreModel(matchId, teamId, game, datetime.now())
		db.session.add(score)
		db.session.commit()

		app.logger.info("Scoring for match=%d team=%d game=%d", matchId, teamId, game)

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

	def serialize(self, scores):
		app.logger.info("Serializing scores")

		data = []

		for score in scores:
			data.append({
				"id": score.id,
				"matchId": score.matchId,
				"teamId": score.teamId,
				"game": score.game,
				"createdAt": score.createdAt
			})

		return json.dumps(data, default = util.jsonSerial)