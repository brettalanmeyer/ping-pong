from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import Response
from pingpong.matchtypes.Singles import Singles
from pingpong.services.LeaderboardService import LeaderboardService
from pingpong.services.PlayerService import PlayerService
from pingpong.utils import util
import json

leaderboardController = Blueprint("leaderboardController", __name__)

leaderboardService = LeaderboardService()
playerService = PlayerService()
singles = Singles()

@leaderboardController.route("/leaderboard", methods = ["GET"], defaults = { "matchType": "singles" })
@leaderboardController.route("/leaderboard/<path:matchType>", methods = ["GET"])
def leaderboard_index(matchType):
	if matchType not in singles.matchTypes:
		abort(404)

	season = util.param("season", None, "int")
	stats = leaderboardService.matchTypeStats(matchType, season)
	return render_template("leaderboard/index.html", stats = stats, matchTypes = singles.matchTypes)

@leaderboardController.route("/leaderboard.json", methods = ["GET"], defaults = { "matchType": "singles" })
@leaderboardController.route("/leaderboard/<path:matchType>.json", methods = ["GET"])
def leaderboard_json(matchType):
	season = util.param("season", None, "int")
	stats = leaderboardService.matchTypeStats(matchType, season)
	return Response(json.dumps(stats, default = util.jsonSerial), status = 200, mimetype = "application/json")

@leaderboardController.route("/leaderboard/players/<int:id>", methods = ["GET"])
def leaderboard_players(id):
	player = playerService.selectById(id)

	season = util.param("season", None, "int")
	stats = leaderboardService.playerStats(player, season)
	return render_template("leaderboard/players.html", player = player, stats = stats, matchTypes = singles.matchTypes)

@leaderboardController.route("/leaderboard/players/<int:id>.json", methods = ["GET"])
def leaderboard_players_json(id):
	player = playerService.selectById(id)

	season = util.param("season", None, "int")
	stats = leaderboardService.playerStats(player, season)
	return Response(json.dumps(stats, default = util.jsonSerial), status = 200, mimetype = "application/json")
