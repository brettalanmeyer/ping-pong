from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import Response
from pingpong.app import socketio
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.MatchService import MatchService
import json

buttonController = Blueprint("buttonController", __name__)

matchService = MatchService()

@buttonController.route("/buttons/<path:button>/score", methods = ["POST"])
def score(button):
	validateButton(button)

	data = None
	response = {
		"matchId": None,
		"action": "score",
		"button": button
	}
	match = matchService.selectActiveMatch()

	if match != None:
		matchType = MatchType(match)
		data = matchType.score(match, button)
		response["matchId"] = match.id
	else:
		latestMatch = matchService.selectLatestMatch()
		matchType = MatchType(latestMatch)

		if matchType.isNines():
			newMatch = matchType.playAgain(latestMatch, None, True)
			response["matchId"] = newMatch.id
			data = {
				"matchType": "nines",
				"redirect": True,
				"matchId": newMatch.id
			}

	socketio.emit("response", data, broadcast = True)
	return Response(json.dumps(response), status = 200, mimetype = "application/json")

@buttonController.route("/buttons/<path:button>/undo", methods = ["POST"])
def undo(button):
	validateButton(button)

	data = None
	response = {
		"matchId": None,
		"action": "undo",
		"button": button
	}
	match = matchService.selectActiveMatch()
	if match != None:
		response["matchId"] = match.id
		matchType = MatchType(match)
		data = matchType.undo(match, button)
	socketio.emit("response", data, broadcast = True)
	return Response(json.dumps(response), status = 200, mimetype = "application/json")

def validateButton(button):
	if button not in matchService.colors:
		abort(400)
