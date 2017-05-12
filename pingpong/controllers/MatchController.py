from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import url_for
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.matchtypes.Singles import Singles
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

singles = Singles()
doubles = Doubles()
nines = Nines()

@matchController.route("/matches", methods = ["GET"])
def index():
	page = util.param("page", 1, "int")
	playerId = util.param("playerId", None, "int")
	matchType = util.param("matchType")

	season = util.param("season", None, "int")
	seasons, season, start, end = leaderboardService.seasons(season)

	players = playerService.select()
	matches = matchService.selectCompleteOrReady(playerId, matchType, start, end)
	pagedMatches = pagingService.pager(matches, page)
	elo = leaderboardService.elo(start, end)

	return render_template("matches/index.html",
		matches = pagedMatches,
		count = matches.count(),
		paging = pagingService.data(),
		playerId = playerId,
		matchType = matchType,
		matchTypes = singles.matchTypes,
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
	match = matchService.create(request.form["matchType"])
	matchType = getMatchType(match)

	if matchType.matchType == "nines":
		return redirect(url_for("matchController.players", id = match.id))

	return redirect(url_for("matchController.games", id = match.id))

@matchController.route("/matches/<int:id>/num-of-games", methods = ["GET"])
def games(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchType = getMatchType(match)
	return render_template("matches/num-of-games.html", match = match)

@matchController.route("/matches/<int:id>/num-of-games", methods = ["POST"])
def games_update(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchService.updateGames(id, request.form["numOfGames"])
	return redirect(url_for("matchController.players", id = id))

@matchController.route("/matches/<int:id>/players", methods = ["GET"])
def players(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchType = getMatchType(match)
	players = playerService.selectActive()
	return render_template("matches/players.html", title = matchType.label, matchType = matchType, match = match, players = players)

@matchController.route("/matches/<int:id>/players", methods = ["POST"])
def players_create(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchType = getMatchType(match)

	if not match.hasTeams():
		matchType.createTeams(match, request.form.getlist("playerId"), True)

	if not match.isReady():
		matchType.play(match)

	return redirect(url_for("matchController.show", id = id))

@matchController.route("/matches/<int:id>", methods = ["GET"])
def show(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchType = getMatchType(match)
	data = matchType.matchData(match)
	return render_template(data["template"], data = data)

@matchController.route("/matches/<int:id>.json", methods = ["GET"])
def show_json(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchType = getMatchType(match)
	data = matchType.matchData(match)
	return Response(json.dumps(data, default = util.jsonSerial), status = 200, mimetype = "application/json")

@matchController.route("/matches/<int:id>/play-again", methods = ["POST"])
def again(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	matchType = getMatchType(match)

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

	if match == None:
		abort(404)

	if match.ready:
		matchType = getMatchType(match)
		matchType.undo(match, None)

	return redirect(url_for("matchController.show", id = match.id))

@matchController.route("/matches/<int:id>/delete", methods = ["POST"])
@loginRequired("matchController.index")
def delete(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

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

def getMatchType(match):
	if singles.isMatchType(match.matchType):
		return singles

	elif doubles.isMatchType(match.matchType):
		return doubles

	elif nines.isMatchType(match.matchType):
		return nines
