import MatchType

class Nines(MatchType.MatchType):

	def __init__(self):
		MatchType.MatchType.__init__(self, "9s", "nines", "matches/four-player.html", "matches/nines.html", 9)
