import Service, logging
from models import MatchModel, TeamModel, GameModel, TeamPlayerModel
from datetime import datetime

logger = logging.getLogger(__name__)

class MatchService(Service.Service):

	def __init__(self, session):
		logger.info("Initializing Match Service")
		Service.Service.__init__(self, session, MatchModel.MatchModel)

	def selectById(self, id):
		logger.info("Selecting match=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def select(self):
		logger.info("Selecting matches")

		return self.session.query(self.model)

	def selectReady(self):
		logger.info("Selecting ready for play matches")

		return self.session.query(self.model).filter(self.model.ready == True)

	def selectActiveMatch(self):
		logger.info("Selecting active matches")

		return self.session.query(self.model).filter(self.model.ready == True, self.model.complete == False).order_by(self.model.id.desc()).first()

	def create(self, matchType):
		match = self.model(matchType, 0, False, False, datetime.now(), datetime.now())
		self.session.add(match)
		self.session.commit()

		logger.info("Creating match=%d", match.id)

		return match

	def updatePlayTo(self, id, playTo):
		match = self.selectById(id)
		match.playTo = playTo
		match.modifiedAt = datetime.now()
		self.session.commit()

		logger.info("Updating match=%d playTo=%d", match.id, match.playTo)

		return match

	def updateGames(self, id, numOfGames):
		match = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		self.session.commit()

		logger.info("Updating match=%d numOfGames=%d game=%d", match.id, match.numOfGames, match.game)

		return match

	def updateGame(self, id, game):
		match = self.selectById(id)
		match.game = game
		match.modifiedAt = datetime.now()
		self.session.commit()

		logger.info("Updating match=%d game=%d", match.id, match.game)

		return match

	def play(self, match):
		match.ready = True
		match.modifiedAt = datetime.now()
		self.session.commit()

		logger.info("Play match=%d", match.id)

	def complete(self, match):
		match.complete = True
		match.modifiedAt = datetime.now()
		match.completedAt = datetime.now()
		self.session.commit()

		logger.info("Completing match=%d", match.id)

	def deleteAll(self):
		logger.info("Deleting all matches")

		self.session.query(self.model).delete()
		self.session.commit()
