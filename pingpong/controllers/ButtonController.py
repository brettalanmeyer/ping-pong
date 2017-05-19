from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import Response
from pingpong.app import socketio
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.MatchService import MatchService

buttonController = Blueprint("buttonController", __name__)

matchService = MatchService()

@buttonController.route("/buttons", methods = ["GET"])
def index():
	return render_template("buttons.html")

@buttonController.route("/buttons/<path:button>/score", methods = ["POST"])
def score(button):
	validateButton(button)

	data = None
	match = matchService.selectActiveMatch()

	if match != None:
		matchType = MatchType(match)
		data = matchType.score(match, button)
	else:
		latestMatch = matchService.selectLatestMatch()
		matchType = MatchType(latestMatch)

		if matchType.isNines():
			newMatch = matchType.playAgain(latestMatch, None, True)
			data = {
				"matchType": "nines",
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
		matchType = MatchType(match)
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
		data = MatchType(match).matchData(match)
	socketio.emit("response", data, broadcast = True)
	return button

def validateButton(button):
	if button not in matchService.colors:
		abort(400)
