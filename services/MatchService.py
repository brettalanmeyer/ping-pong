from Service import Service
from models.MatchModel import MatchModel
from models.TeamModel import TeamModel
from models.GameModel import GameModel
from models.PlayerModel import PlayerModel
from datetime import datetime
from flask import current_app as app
from sqlalchemy import or_
from utils import database as db

class MatchService(Service):

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		return db.session.query(MatchModel).filter(MatchModel.id == id).one()

	def selectNotById(self, id):
		app.logger.info("Selecting matches excluding match=%d", id)

		return db.session.query(MatchModel).filter(MatchModel.id != id)

	def select(self):
		app.logger.info("Selecting matches")

		return db.session.query(MatchModel)

	def selectComplete(self):
		app.logger.info("Selecting completed matches")

		return db.session.query(MatchModel).filter(MatchModel.complete == True).order_by(MatchModel.id.desc())

	def selectCompleteOrReady(self, playerId = None):
		app.logger.info("Selecting complete or ready for play matches")

		matches = db.session.query(MatchModel).filter(or_(MatchModel.complete == True, MatchModel.ready == True)).order_by(MatchModel.id.desc())

		if playerId != None:
			matches = matches.join(MatchModel.teams).join(TeamModel.players).filter(PlayerModel.id == playerId)

		return matches

	def selectActiveMatch(self):
		app.logger.info("Selecting active match")

		return db.session.query(MatchModel).filter(MatchModel.ready == True, MatchModel.complete == False).order_by(MatchModel.id.desc()).first()

	def selectLatestMatch(self):
		app.logger.info("Selecting latest completed match")

		return db.session.query(MatchModel).filter(MatchModel.complete == True).order_by(MatchModel.id.desc()).first()

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
		match.completedAt = datetime.now()
		db.session.commit()

		app.logger.info("Incompleting match=%d", match.id)

	def complete(self, match):
		match.complete = True
		match.modifiedAt = datetime.now()
		match.completedAt = datetime.now()
		db.session.commit()

		app.logger.info("Completing match=%d", match.id)

	def deleteAll(self):
		app.logger.info("Deleting all matches")

		db.session.query(MatchModel).delete()
		db.session.commit()
