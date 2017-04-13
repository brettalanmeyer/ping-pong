from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import Response
from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService

buttonController = Blueprint("buttonController", __name__)

matchService = MatchService()

singles = Singles()
doubles = Doubles()
nines = Nines()

@buttonController.route("/buttons", methods = ["GET"])
def buttons():
	return render_template("buttons.html")

@buttonController.route("/buttons/<path:button>/score", methods = ["POST"])
def buttons_score(button):
	data = None
	match = matchService.selectActiveMatch()

	if match != None:
		matchType = getMatchType(match)
		data = matchType.score(match, button)
	else:
		latestMatch = matchService.selectLatestMatch()
		if latestMatch.matchType == "nines":
			matchType = getMatchType(latestMatch)
			newMatch = matchType.playAgain(latestMatch, None, True)
			data = {
				"matchType": matchType.matchType,
				"redirect": True,
				"matchId": newMatch.id
			}

	app.socketio.emit("response", data, broadcast = True)
	return button

@buttonController.route("/buttons/<path:button>/undo", methods = ["POST"])
def buttons_undo(button):
	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		matchType = getMatchType(match)
		data = matchType.undo(match, button)
	app.socketio.emit("response", data, broadcast = True)
	return button

@buttonController.route("/buttons/<path:button>/delete-scores", methods = ["POST"])
def buttons_delete_scores(button):
	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		scoreService.deleteByMatch(match.id)
		data = getMatchType(match).matchData(match)
	app.socketio.emit("response", data, broadcast = True)
	return button

def getMatchType(match):
	if singles.isMatchType(match.matchType):
		return singles

	elif doubles.isMatchType(match.matchType):
		return doubles

	elif nines.isMatchType(match.matchType):
		return nines