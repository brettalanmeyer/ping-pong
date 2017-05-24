from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.GameService import GameService
from pingpong.services.IsmService import IsmService
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.ScoreService import ScoreService
from pingpong.utils import notifications
from pingpong.utils import util

adminController = Blueprint("adminController", __name__)

gameService = GameService()
ismService = IsmService()
matchService = MatchService()
playerService = PlayerService()
scoreService = ScoreService()

@adminController.route("/admin", methods = ["GET"])
@loginRequired()
def index():
	counts = {
		"numOfIsms": ismService.selectCount(),
		"numOfMatches": matchService.selectCount(),
		"numOfPlayers": playerService.selectCount(),
		"numOfScores": scoreService.selectCount(),
		"numOfGames": gameService.selectCount()
	}
	counts["total"] = sum(counts.values())

	matchData = None
	match = matchService.selectActiveMatch()
	if match != None:
		matchData = MatchType(match).matchData()

	return render_template("admin/index.html", counts = counts, matchData = matchData)

@adminController.route("/admin/send-message", methods = ["POST"])
@loginRequired("adminController.index")
def send_message():
	message = util.paramForm("message")

	if message != None and len(message) > 0:
		notifications.send(message)
		flash("Message has been sent.", "success")
	else:
		flash("Message was malformed and was not be sent.", "danger")

	return redirect(url_for("adminController.index"))
