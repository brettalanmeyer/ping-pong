from datetime import datetime
from flask import current_app as app
from pingpong.models.GameModel import GameModel
from pingpong.models.MatchModel import MatchModel
from pingpong.models.PlayerModel import PlayerModel
from pingpong.models.TeamModel import TeamModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from sqlalchemy import or_

class MatchService(Service):

	def select(self):
		app.logger.info("Selecting matches")

		return db.session.query(MatchModel)

	def selectCount(self):
		app.logger.info("Selecting number of matches")

		return self.select().count()

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		matches = db.session.query(MatchModel).filter(MatchModel.id == id)

		if matches.count() == 1:
			return matches.one()

		return None

	def selectNotById(self, id):
		app.logger.info("Selecting matches excluding match=%d", id)

		return db.session.query(MatchModel).filter(MatchModel.id != id)

	def selectComplete(self):
		app.logger.info("Selecting completed matches")

		return db.session.query(MatchModel).filter(MatchModel.complete == True).order_by(MatchModel.id.desc())

	def selectCompleteOrReady(self, playerId = None, opponentId = None, matchType = None, start = None, end = None):
		app.logger.info("Selecting complete or ready for play matches")

		matches = db.session.query(MatchModel).filter(or_(MatchModel.complete == True, MatchModel.ready == True)).order_by(MatchModel.id.desc())

		if playerId != None:
			matches = matches.join(MatchModel.teams).join(TeamModel.players).filter(PlayerModel.id == playerId)

			if opponentId != None:
				ids = []
				for match in matches:
					if self.hasOpponent(match, opponentId):
						ids.append(match.id)

				matches = db.session.query(MatchModel).filter(MatchModel.id.in_(ids))

		if matchType != None:
			matches = matches.filter(MatchModel.matchType == matchType)

		if start != None:
			matches = matches.filter(MatchModel.createdAt >= start)

		if end != None:
			matches = matches.filter(MatchModel.createdAt < end)

		return matches

	def hasOpponent(self, match, opponentId):
		for team in match.teams:
			for player in team.players:
				if player.id == opponentId:
					return True

		return False

	def selectActiveMatch(self):
		app.logger.info("Selecting active match")

		matches = db.session.query(MatchModel).filter(MatchModel.ready == True, MatchModel.complete == False).order_by(MatchModel.id.desc())

		if matches.count() == 0:
			return None

		return matches.first()

	def selectLatestMatch(self):
		app.logger.info("Selecting latest completed match")

		matches = db.session.query(MatchModel).filter(MatchModel.complete == True).order_by(MatchModel.id.desc())

		if matches.count() == 0:
			return None

		return matches.first()

	def setAsNotReady(self, id):
		app.logger.info("Updateing all matches except current one to not ready")

		update(MatchModel).where(MatchModel.id != id).values(ready = False)
		db.session.commit()

	def create(self, matchType):
		playTo = 21
		if matchType == "nines":
			playTo = 9

		match = MatchModel(matchType, playTo, 0, False, False, datetime.now(), datetime.now())
		db.session.add(match)
		db.session.commit()

		app.logger.info("Creating match=%d", match.id)

		return match

	def updateGames(self, id, numOfGames):
		match = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating match=%d numOfGames=%d game=%d", match.id, match.numOfGames, match.game)

		return match

	def updateGame(self, id, game):
		match = self.selectById(id)
		match.game = game
		match.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating match=%d game=%d", match.id, match.game)

		return match

	def play(self, match):
		matches = self.selectNotById(match.id)
		for item in matches:
			item.ready = False

		match.ready = True
		match.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Play match=%d", match.id)

	def incomplete(self, match):
		match.complete = False
		match.modifiedAt = datetime.now()
		match.completedAt = None
		db.session.commit()

		app.logger.info("Incompleting match=%d", match.id)

	def complete(self, match):
		match.complete = True
		match.modifiedAt = datetime.now()
		match.completedAt = datetime.now()
		db.session.commit()

		app.logger.info("Completing match=%d", match.id)

	def deleteById(self, id):
		app.logger.info("Deleting match by id=%d", id)
		match = self.selectById(id)
		return self.delete(match)

	def delete(self, match):
		app.logger.info("Deleting match=%d", match.id)

		try:
			db.session.delete(match)
			db.session.commit()
			return match, True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return match, False

	def deleteAll(self):
		app.logger.info("Deleting all matches")

		try:
			db.session.query(MatchModel).delete()
			db.session.commit()
			return True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return False
