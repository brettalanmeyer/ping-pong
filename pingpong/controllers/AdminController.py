from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.services.DataService import DataService
from pingpong.services.GameService import GameService
from pingpong.services.IsmService import IsmService
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.ScoreService import ScoreService
from pingpong.utils import notifications
from pingpong.utils import util

adminController = Blueprint("adminController", __name__)

dataService = DataService()
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

	return render_template("admin/index.html", counts = counts, allowed = dataService.isConfigured())

@adminController.route("/admin/send-message", methods = ["POST"])
@loginRequired("adminController.index")
def send_message():

	print("hi")
	print("hi")
	print("hi")
	print("hi")

	message = util.paramForm("message")

	if message != None and len(message) > 0:
		notifications.send(message)
		flash("Message has been sent.", "success")
	else:
		flash("Message was malformed and was not be sent.", "danger")

	return redirect(url_for("adminController.index"))

@adminController.route("/admin/copy-remote-data", methods = ["POST"])
@loginRequired("adminController.index")
def copy_remote_data():
	if not access():
		return redirect(url_for("adminController.index"))

	dataService.copyPlayers()
	flash("Players have been copied.", "success")

	dataService.copyIsms()
	flash("Isms have been copied.", "success")

	dataService.copyMatches()
	flash("Matches have been copied.", "success")

	dataService.copyTeams()
	flash("Teams have been copied.", "success")

	dataService.copyTeamsPlayers()
	flash("TeamsPlayers have been copied.", "success")

	dataService.copyGames()
	flash("Games have been copied.", "success")

	dataService.copyScores()
	flash("Scores have been copied.", "success")

	return redirect(url_for("adminController.index"))

@adminController.route("/admin/delete-all", methods = ["POST"])
@loginRequired("adminController.index")
def delete_all():
	if not access():
		return redirect(url_for("adminController.index"))

	ismService.deleteAll()
	flash("All isms have been successfully deleted.", "success")

	matchService.deleteAll()
	flash("All matches have been successfully deleted.", "success")

	playerService.deleteAll()
	flash("All players have been successfully deleted.", "success")

	return redirect(url_for("adminController.index"))

def access():
	if  not dataService.isConfigured():
		flash("This action is only allowed in development mode.", "danger")
		return False

	return True
