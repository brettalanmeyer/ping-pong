from flask import Blueprint, render_template, Response

buttonsController = Blueprint("buttonsController", __name__)

@buttonsController.route("/buttons", methods = ["GET"])
def buttons():
	return render_template("buttons.html")

@buttonsController.route("/buttons/<path:button>/score", methods = ["POST"])
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

	socketio.emit("response", data, broadcast = True)
	return button

@buttonsController.route("/buttons/<path:button>/undo", methods = ["POST"])
def buttons_undo(button):
	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		matchType = getMatchType(match)
		data = matchType.undo(match, button)
	socketio.emit("response", data, broadcast = True)
	return button

@buttonsController.route("/buttons/<path:button>/delete-scores", methods = ["POST"])
def buttons_delete_scores(button):
	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		scoreService.deleteByMatch(match.id)
		data = getMatchType(match).matchData(match)
	socketio.emit("response", data, broadcast = True)
	return button
