import Service
from models import MatchModel, TeamModel, GameModel, TeamPlayerModel
from datetime import datetime

class MatchService(Service.Service):

	def __init__(self):
		Service.Service.__init__(self, MatchModel.MatchModel)

	def selectById(self, id):
		match = self.session.query(self.model).filter(self.model.id == id).one()
		return match

	def select(self):
		return self.session.query(self.model)

	def selectActiveMatch(self):
		return self.session.query(self.model).filter(self.model.ready == True, self.model.complete == False).order_by(self.model.id.desc()).first()

	def create(self, matchType):
		match = self.model(matchType, False, False, datetime.now(), datetime.now())
		self.session.add(match)
		self.session.commit()

		return match

	def updatePlayTo(self, id, playTo):
		match = self.selectById(id)
		match.playTo = playTo
		match.modifiedAt = datetime.now()
		self.session.commit()

		return match

	def updateGames(self, id, numOfGames):
		match = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		self.session.commit()

		return match

	def updateGame(self, id, game):
		match = self.selectById(id)
		match.game = game
		match.modifiedAt = datetime.now()
		self.session.commit()

		return match

	def play(self, match):
		match.ready = True
		match.modifiedAt = datetime.now()
		self.session.commit()

	def complete(self, match):
		match.complete = True
		match.modifiedAt = datetime.now()
		match.completedAt = datetime.now()
		self.session.commit()

	def deleteAll(self):
		self.session.query(self.model).delete()
		self.session.commit()
