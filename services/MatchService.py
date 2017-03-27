import Service
from models import MatchModel, TeamModel, GameModel
from datetime import datetime
from flask import current_app as app

class MatchService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, MatchModel.MatchModel)

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def selectNotById(self, id):
		app.logger.info("Selecting matches excluding match=%d", id)

		return self.session.query(self.model).filter(self.model.id != id)

	def select(self):
		app.logger.info("Selecting matches")

		return self.session.query(self.model)

	def selectComplete(self):
		app.logger.info("Selecting ready for play matches")

		return self.session.query(self.model).filter(self.model.complete == True).order_by(self.model.id.desc())

	def selectActiveMatch(self):
		app.logger.info("Selecting active match")

		return self.session.query(self.model).filter(self.model.ready == True, self.model.complete == False).order_by(self.model.id.desc()).first()

	def selectLatestMatch(self):
		app.logger.info("Selecting latest completed match")

		return self.session.query(self.model).filter(self.model.complete == True).order_by(self.model.id.desc()).first()

	def setAsNotReady(self, id):
		app.logger.info("Updateing all matches except current one to not ready")

		update(self.model).where(self.model.id != id).values(ready = False)
		self.session.commit()

	def create(self, matchType):
		match = self.model(matchType, 0, False, False, datetime.now(), datetime.now())
		self.session.add(match)
		self.session.commit()

		app.logger.info("Creating match=%d", match.id)

		return match

	def updatePlayTo(self, id, playTo):
		match = self.selectById(id)
		match.playTo = playTo
		match.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Updating match=%d playTo=%d", match.id, match.playTo)

		return match

	def updateGames(self, id, numOfGames):
		match = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Updating match=%d numOfGames=%d game=%d", match.id, match.numOfGames, match.game)

		return match

	def updateGame(self, id, game):
		match = self.selectById(id)
		match.game = game
		match.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Updating match=%d game=%d", match.id, match.game)

		return match

	def play(self, match):
		matches = self.selectNotById(match.id)
		for item in matches:
			item.ready = False

		match.ready = True
		match.modifiedAt = datetime.now()
		self.session.commit()

		app.logger.info("Play match=%d", match.id)

	def complete(self, match):
		match.complete = True
		match.modifiedAt = datetime.now()
		match.completedAt = datetime.now()
		self.session.commit()

		app.logger.info("Completing match=%d", match.id)

	def deleteAll(self):
		app.logger.info("Deleting all matches")

		self.session.query(self.model).delete()
		self.session.commit()
