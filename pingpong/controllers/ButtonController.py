from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import Response
from pingpong.app import socketio
from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from datetime import datetime

buttonController = Blueprint("buttonController", __name__)

matchService = MatchService()

singles = Singles()
doubles = Doubles()
nines = Nines()

@buttonController.route("/buttons", methods = ["GET"])
def index():
	return render_template("buttons.html")

@buttonController.route("/buttons/<path:button>/score", methods = ["POST"])
def score(button):
	validateButton(button)

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

	socketio.emit("response", data, broadcast = True)
	return button

@buttonController.route("/buttons/<path:button>/undo", methods = ["POST"])
def undo(button):
	validateButton(button)

	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		matchType = getMatchType(match)
		data = matchType.undo(match, button)
	socketio.emit("response", data, broadcast = True)
	return button

@buttonController.route("/buttons/<path:button>/delete-scores", methods = ["POST"])
def delete_scores(button):
	validateButton(button)

	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		scoreService.deleteByMatch(match.id)
		data = getMatchType(match).matchData(match)
	socketio.emit("response", data, broadcast = True)
	return button

def validateButton(button):
	if button not in singles.colors:
		abort(400)

def getMatchType(match):
	if singles.isMatchType(match.matchType):
		return singles

	elif doubles.isMatchType(match.matchType):
		return doubles

	elif nines.isMatchType(match.matchType):
		return nines