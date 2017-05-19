from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.matchtypes.Singles import Singles

singles = Singles()
doubles = Doubles()
nines = Nines()

class MatchType():

	def __init__(self, match):
		self.match = match
		self.setMatchType()

	def isSingles(self):
		return singles.isMatchType(self.match.matchType)

	def isDoubles(self):
		return doubles.isMatchType(self.match.matchType)

	def isNines(self):
		return nines.isMatchType(self.match.matchType)

	def createTeams(self, *args, **kwargs):
		return self.matchType.createTeams(*args, **kwargs)

	def play(self, *args, **kwargs):
		return self.matchType.play(*args, **kwargs)

	def matchData(self, *args, **kwargs):
		return self.matchType.matchData(*args, **kwargs)

	def playAgain(self, *args, **kwargs):
		return self.matchType.playAgain(*args, **kwargs)

	def undo(self, *args, **kwargs):
		return self.matchType.undo(*args, **kwargs)

	def score(self, *args, **kwargs):
		return self.matchType.score(*args, **kwargs)

	def setMatchType(self):
		if singles.isMatchType(self.match.matchType):
			self.matchType = singles

		elif doubles.isMatchType(self.match.matchType):
			self.matchType = doubles

		elif nines.isMatchType(self.match.matchType):
			self.matchType = nines

	def getMatchType(self):
		return self.matchType
