import Service
from models import MatchModel, TeamModel, GameModel, TeamPlayerModel
from datetime import datetime
from matchtypes import Singles, Doubles, Nines

class MatchService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, MatchModel.MatchModel)
		self.singles = Singles.Singles(session)
		self.doubles = Doubles.Doubles(session)
		self.nines = Nines.Nines(session)

	def selectById(self, id):
		match = self.session.query(self.model).filter(self.model.id == id).one()
		matchType = self.getMatchType(match)
		return match, matchType

	def select(self):
		return self.session.query(self.model)

	def selectActiveMatch(self):
		match = self.session.query(self.model).filter(self.model.ready == True, self.model.complete == False).order_by(self.model.id.desc()).first()
		matchType = None
		if match != None:
			matchType = self.getMatchType(match)
		return match, matchType

	def create(self, matchType):
		match = self.model(matchType, False, False, datetime.now(), datetime.now())
		self.session.add(match)
		self.session.commit()

		return match

	def updatePlayTo(self, id, playTo):
		match, matchType = self.selectById(id)
		match.playTo = playTo
		match.modifiedAt = datetime.now()
		self.session.commit()

		return match, matchType

	def updateGames(self, id, numOfGames):
		match, matchType = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		self.session.commit()

		return match, matchType

	def updateGame(self, id, game):
		match, matchType = self.selectById(id)
		match.game = game
		match.modifiedAt = datetime.now()
		self.session.commit()

		return match, matchType

	def getMatchType(self, match):
		if self.singles.isMatchType(match.matchType):
			return self.singles

		elif self.doubles.isMatchType(match.matchType):
			return self.doubles

		elif self.nines.isMatchType(match.matchType):
			return self.nines

	def matchDataById(self, id):
		match, matchType = self.selectById(id)
		return matchType.matchData(match)

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
