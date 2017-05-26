from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request
from flask import Response
from pingpong.app import socketio
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.MatchService import MatchService
from pingpong.services.OfficeService import OfficeService
import json

buttonController = Blueprint("buttonController", __name__)

matchService = MatchService()
officeService = OfficeService()

@buttonController.route("/api/buttons/<path:button>/score", methods = ["POST"])
def score(button):
	validateButton(button)
	office = validateOffice()

	data = None
	response = {
		"matchId": None,
		"action": "score",
		"button": button,
		"officeName": "{}, {}".format(office.city, office.state)
	}
	match = matchService.selectActiveMatch(office.id)

	if match != None:
		matchType = MatchType(match)
		data = matchType.score(match, button)
		response["matchId"] = match.id
	else:
		latestMatch = matchService.selectLatestMatch(office.id)
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

@buttonController.route("/api/buttons/<path:button>/undo", methods = ["POST"])
def undo(button):
	validateButton(button)
	office = validateOffice()

	data = None
	response = {
		"matchId": None,
		"action": "undo",
		"button": button,
		"officeName": "{}, {}".format(office.city, office.state)
	}
	match = matchService.selectActiveMatch(office.id)
	if match != None:
		response["matchId"] = match.id
		matchType = MatchType(match)
		data = matchType.undo(match, button)
	socketio.emit("response", data, broadcast = True)
	return Response(json.dumps(response), status = 200, mimetype = "application/json")

def validateButton(button):
	if button not in matchService.colors:
		abort(400)

def validateOffice():
	if "key" not in request.form:
		abort(400)

	office = officeService.selectByHash(request.form["key"])

	if office == None:
		abort(400)

	return office
