import MatchType

class Nines(MatchType.MatchType):

	label = "9s"
	matchType = "nines"
	playerTemplate = "matches/four-player.html"
	matchTemplate = "matches/nines.html"
	defaultPoints = 9

	def __init__(self):
		MatchType.MatchType.__init__(self, "9s", "nines", "matches/four-player.html", "matches/nines.html", 9)
