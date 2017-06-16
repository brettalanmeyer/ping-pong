from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import session
from flask import url_for
from pingpong.app import socketio
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.LeaderboardService import LeaderboardService
from pingpong.services.MatchService import MatchService
from pingpong.services.PagingService import PagingService
from pingpong.services.PlayerService import PlayerService
from pingpong.utils import util
import json

matchController = Blueprint("matchController", __name__)

playerService = PlayerService()
matchService = MatchService()
pagingService = PagingService()
leaderboardService = LeaderboardService()

@matchController.route("/matches", methods = ["GET"])
def index():
	page = util.param("page", 1, "int")
	playerId = util.param("playerId", None, "int")
	opponentId = util.param("opponentId", None, "int")
	matchType = util.param("matchType")

	season = util.param("season", None, "int")
	seasons, season, start, end = leaderboardService.seasons(season, session["office"]["id"])

	players = playerService.select(session["office"]["id"])
	matches = matchService.selectCompleteOrReady(session["office"]["id"], playerId, opponentId, matchType, start, end)
	pagedMatches = pagingService.pager(matches, page)
	elo = leaderboardService.elo(session["office"]["id"], start, end)

	return render_template("matches/index.html",
		matches = pagedMatches,
		count = matches.count(),
		paging = pagingService.data(),
		playerId = playerId,
		opponentId = opponentId,
		matchType = matchType,
		matchTypes = matchService.matchTypes,
		players = players,
		elo = elo,
		seasons = seasons,
		season = season
	)

@matchController.route("/matches/new", methods = ["GET"])
def new():
	return render_template("matches/new.html")

@matchController.route("/matches", methods = ["POST"])
def create():
	match = matchService.create(session["office"]["id"], request.form["matchType"])
	matchType = MatchType(match)

	if matchType.isNines():
		return redirect(url_for("matchController.players", id = match.id))

	return redirect(url_for("matchController.games", id = match.id))

@matchController.route("/matches/<int:id>/num-of-games", methods = ["GET"])
def games(id):
	match = matchService.selectById(id)

	exists(match)

	return render_template("matches/num-of-games.html", match = match)

@matchController.route("/matches/<int:id>/num-of-games", methods = ["POST"])
def games_update(id):
	match = matchService.selectById(id)

	exists(match)

	matchService.updateGames(id, request.form["numOfGames"])
	return redirect(url_for("matchController.players", id = id))

@matchController.route("/matches/<int:id>/players", methods = ["GET"])
def players(id):
	match = matchService.selectById(id)

	exists(match)

	matchType = MatchType(match)
	instance = matchType.getMatchType()
	players = playerService.selectActive(session["office"]["id"])
	return render_template("matches/players.html", title = instance.label, matchType = instance, match = match, players = players)

@matchController.route("/matches/<int:id>/players", methods = ["POST"])
def players_create(id):
	match = matchService.selectById(id)

	exists(match)

	matchType = MatchType(match)

	if not match.hasTeams():
		matchType.createTeams(match, request.form.getlist("playerId"), True)

	if not match.isReady():
		matchType.play(match)

	return redirect(url_for("matchController.show", id = id))

@matchController.route("/matches/<int:id>", methods = ["GET"])
def show(id):
	match = matchService.selectById(id)

	exists(match)

	data = MatchType(match).matchData()
	return render_template(data["template"], data = data)

@matchController.route("/matches/<int:id>.json", methods = ["GET"])
def show_json(id):
	match = matchService.selectById(id)

	exists(match)

	data = MatchType(match).matchData()
	return Response(json.dumps(data, default = util.jsonSerial), status = 200, mimetype = "application/json")

@matchController.route("/matches/<int:id>/play-again", methods = ["POST"])
def again(id):
	match = matchService.selectById(id)

	exists(match)

	matchType = MatchType(match)

	numOfGames = None
	randomize = True
	if "numOfGames" in request.form:
		numOfGames = int(request.form["numOfGames"])
	if "randomize" in request.form:
		randomize = request.form["randomize"] == "true"

	newMatch = matchType.playAgain(match, numOfGames, randomize)
	return redirect(url_for("matchController.show", id = newMatch.id))

@matchController.route("/matches/<int:id>/undo", methods = ["POST"])
def undo(id):
	match = matchService.selectById(id)

	exists(match)

	if match.ready:
		matchType = MatchType(match)
		data = matchType.undo(match, None)

	if request.is_xhr:
		socketio.emit("response-{}".format(match.officeId), data, broadcast = True)
		return Response("", status = 200, mimetype = "application/json")
	else:
		return redirect(url_for("matchController.show", id = match.id))

@matchController.route("/matches/entry", methods = ["GET"])
@loginRequired()
def entry():
	players = playerService.selectActive(session["office"]["id"])
	return render_template("matches/entry.html", players = players)

@matchController.route("/matches/entry", methods = ["POST"])
@loginRequired()
def entry_create():
	return redirect(url_for("matchController.index"))

@matchController.route("/matches/<int:id>/delete", methods = ["POST"])
@loginRequired("matchController.index")
def delete(id):
	match = matchService.selectById(id)

	exists(match)

	match, success = matchService.delete(match)

	if success:
		flash("Match has been successfully deleted.", "success")
	else:
		flash("Match could not be deleted .", "warning")

	return redirect(url_for("matchController.index",
		season = util.param("season", None),
		playerId = util.param("playerId", None),
		matchType = util.param("matchType", None)
	))

@matchController.route("/matches/<int:id>/smack-talk", methods = ["POST"])
def smack_talk(id):
	message = util.paramForm("message", None)
	if message != None and len(message) > 0:
		data = { "message": message }
		socketio.emit("smack-talk-{}".format(session["office"]["id"]), data, broadcast = True)
		app.logger.info("Smack Talk: %s \"%s\"", request.remote_addr, message)

	return message

def exists(match):
	if match == None:
		abort(404)

	if match.office.id != session["office"]["id"]:
		abort(404)
