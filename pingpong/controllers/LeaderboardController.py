from flask import Blueprint, render_template
from pingpong.matchtypes import Singles
from pingpong.services import LeaderboardService
from pingpong.services import PlayerService

leaderboardController = Blueprint("leaderboardController", __name__)

singles = Singles.Singles()
playerService = PlayerService.PlayerService()
leaderboardService = LeaderboardService.LeaderboardService()

@leaderboardController.route("/leaderboard", methods = ["GET"], defaults = { "matchType": "singles" })
@leaderboardController.route("/leaderboard/<path:matchType>", methods = ["GET"])
def leaderboard_index(matchType):
	if matchType not in singles.matchTypes:
		abort(404)

	stats = leaderboardService.matchTypeStats(matchType)
	return render_template("leaderboard/index.html", stats = stats, matchTypes = singles.matchTypes, matchType = matchType)

@leaderboardController.route("/leaderboard.json", methods = ["GET"], defaults = { "matchType": "singles" })
@leaderboardController.route("/leaderboard/<path:matchType>.json", methods = ["GET"])
def leaderboard_json(matchType):
	stats = leaderboardService.matchTypeStats(matchType)
	return Response(json.dumps(stats), status = 200, mimetype = "application/json")

@leaderboardController.route("/leaderboard/players/<int:id>", methods = ["GET"])
def leaderboard_players(id):
	player = playerService.selectById(id)
	stats = leaderboardService.playerStats(player)
	return render_template("leaderboard/players.html", player = player, stats = stats, matchTypes = singles.matchTypes)

@leaderboardController.route("/leaderboard/players/<int:id>.json", methods = ["GET"])
def leaderboard_players_json(id):
	player = playerService.selectById(id)
	stats = leaderboardService.playerStats(player)
	return Response(json.dumps(stats), status = 200, mimetype = "application/json")
