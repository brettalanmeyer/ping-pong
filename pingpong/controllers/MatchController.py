from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask_login import login_required
from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.matchtypes.Singles import Singles
from pingpong.services.LeaderboardService import LeaderboardService
from pingpong.services.MatchService import MatchService
from pingpong.services.PagingService import PagingService
from pingpong.services.PlayerService import PlayerService
from pingpong.utils import util

matchController = Blueprint("matchController", __name__)

playerService = PlayerService()
matchService = MatchService()
pagingService = PagingService()
leaderboardService = LeaderboardService()

singles = Singles()
doubles = Doubles()
nines = Nines()

@matchController.route("/matches", methods = ["GET"])
def matches_index():
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
def matches_new():
	return render_template("matches/new.html")

@matchController.route("/matches", methods = ["POST"])
def matches_create():
	match = matchService.create(request.form["matchType"])
	matchType = getMatchType(match)

	if matchType.matchType == "nines":
		return redirect("/matches/%d/players" % match.id)

	return redirect("/matches/%d/num-of-games" % match.id)

@matchController.route("/matches/<int:id>/num-of-games", methods = ["GET"])
def matches_games(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	return render_template("matches/num-of-games.html", match = match)

@matchController.route("/matches/<int:id>/num-of-games", methods = ["POST"])
def matches_games_update(id):
	matchService.updateGames(id, request.form["numOfGames"])
	return redirect("/matches/%d/players" % id)

@matchController.route("/matches/<int:id>/players", methods = ["GET"])
def matches_players(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	players = playerService.selectActive()
	return render_template("matches/players.html", title = matchType.label, matchType = matchType, match = match, players = players)

@matchController.route("/matches/<int:id>/players", methods = ["POST"])
def matches_players_create(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	matchType.createTeams(match, request.form.getlist("playerId"), True)
	matchType.play(match)
	return redirect("/matches/%d" % id)

@matchController.route("/matches/<int:id>", methods = ["GET"])
def matches(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	data = matchType.matchData(match)
	return render_template(data["template"], data = data)

@matchController.route("/matches/<int:id>.json", methods = ["GET"])
def matches_json(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	data = matchType.matchData(match)
	return Response(json.dumps(data), status = 200, mimetype = "application/json")

@matchController.route("/matches/<int:id>/play-again", methods = ["POST"])
def matches_again(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)

	numOfGames = None
	randomize = True
	if "numOfGames" in request.form:
		numOfGames = int(request.form["numOfGames"])
	if "randomize" in request.form:
		randomize = request.form["randomize"] == "true"

	newMatch = matchType.playAgain(match, numOfGames, randomize)
	return redirect("/matches/%d" % newMatch.id)

@matchController.route("/matches/<int:id>/undo", methods = ["POST"])
def matches_undo(id):
	match = matchService.selectById(id)
	if match.ready:
		matchType = getMatchType(match)
		matchType.undo(match, None)

	return redirect("/matches/%d" % match.id)

@matchController.route("/matches/<int:id>/delete", methods = ["POST"])
@login_required
def matches_delete(id):
	match = matchService.selectById(id)

	if match == None:
		abort(404)

	match, success = matchService.delete(match)

	if success:
		flash("Match has been successfully.", "success")
	else:
		flash("Match could not be deleted .", "warning")

	season = util.paramForm("season")
	playerId = util.paramForm("playerId")
	matchType = util.paramForm("matchType")

	params = []

	if season != None:
		params.append("season={}".format(season))

	if playerId != None:
		params.append("playerId={}".format(playerId))

	if matchType != None:
		params.append("matchType={}".format(matchType))

	if len(params) > 0:
		return redirect("/matches?{}".format("&".join(params)))
	else:
		return redirect("/matches")

def getMatchType(match):
	if singles.isMatchType(match.matchType):
		return singles

	elif doubles.isMatchType(match.matchType):
		return doubles

	elif nines.isMatchType(match.matchType):
		return nines
