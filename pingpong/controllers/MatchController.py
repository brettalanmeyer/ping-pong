from flask import Blueprint, render_template, Response, redirect, request
from pingpong.services import PagingService, MatchService, ScoreService, LeaderboardService, PlayerService, PagingService
from pingpong.matchtypes import Singles, Doubles, Nines

matchController = Blueprint("matchController", __name__)
pagingService = PagingService.PagingService()
matchService = MatchService.MatchService()
playerService = PlayerService.PlayerService()
singles = Singles.Singles()
doubles = Doubles.Doubles()
nines = Nines.Nines()

@matchController.route("/matches", methods = ["GET"], defaults = { "page": 1 })
@matchController.route("/matches/page/<int:page>", methods = ["GET"])
def matches_index(page):
	matches = pagingService.pager(matchService.selectCompleteOrReady(), page)
	return render_template("matches/index.html", matches = matches, url = "/matches/page", paging = pagingService.data())

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
	matchService.play(match)
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

def getMatchType(match):
	if singles.isMatchType(match.matchType):
		return singles

	elif doubles.isMatchType(match.matchType):
		return doubles

	elif nines.isMatchType(match.matchType):
		return nines