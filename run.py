from flask import Flask, render_template, Response, redirect, request, abort, send_from_directory
from flask_socketio import SocketIO, emit
import json
from utils import database, logger, assets
from services import IsmService, PlayerService, MatchService, ScoreService, LeaderboardService, PagingService
from matchtypes import Singles, Doubles, Nines

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
socketio = SocketIO(app)

@app.route("/", methods = ["GET"])
def index():
	matches = matchService.selectComplete().count()
	scores = scoreService.selectCount()
	return render_template("main/index.html", matches = matches, scores = scores)

@app.route("/matches", methods = ["GET"], defaults = { "page": 1 })
@app.route("/matches/page/<int:page>", methods = ["GET"])
def matches_index(page):
	matches = pagingService.pager(matchService.selectCompleteOrReady(), page)
	return render_template("matches/index.html", matches = matches, url = "/matches/page", paging = pagingService.data())

@app.route("/matches/new", methods = ["GET"])
def matches_new():
	return render_template("matches/new.html")

@app.route("/matches", methods = ["POST"])
def matches_create():
	match = matchService.create(request.form["matchType"])
	matchType = getMatchType(match)

	if matchType.matchType == "nines":
		return redirect("/matches/%d/players" % match.id)

	return redirect("/matches/%d/num-of-games" % match.id)

@app.route("/matches/<int:id>/num-of-games", methods = ["GET"])
def matches_games(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	return render_template("matches/num-of-games.html", match = match)

@app.route("/matches/<int:id>/num-of-games", methods = ["POST"])
def matches_games_update(id):
	matchService.updateGames(id, request.form["numOfGames"])
	return redirect("/matches/%d/players" % id)

@app.route("/matches/<int:id>/players", methods = ["GET"])
def matches_players(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	players = playerService.selectActive()
	return render_template("matches/players.html", title = matchType.label, matchType = matchType, match = match, players = players)

@app.route("/matches/<int:id>/players", methods = ["POST"])
def matches_players_create(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	matchType.createTeams(match, request.form.getlist("playerId"), True)
	matchService.play(match)
	return redirect("/matches/%d" % id)

@app.route("/matches/<int:id>", methods = ["GET"])
def matches(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	data = matchType.matchData(match)
	return render_template(data["template"], data = data)

@app.route("/matches/<int:id>.json", methods = ["GET"])
def matches_json(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	data = matchType.matchData(match)
	return Response(json.dumps(data), status = 200, mimetype = "application/json")

@app.route("/matches/<int:id>/play-again", methods = ["POST"])
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

@app.route("/players", methods = ["GET"])
def players():
	return render_template("players/index.html", players = playerService.select())

@app.route("/players/new", methods = ["GET"], defaults = { "matchId": None })
@app.route("/players/new/matches/<int:matchId>", methods = ["GET"])
def players_new(matchId):
	player = playerService.new()
	return render_template("players/new.html", player = player, matchId = matchId)

@app.route("/players", methods = ["POST"], defaults = { "matchId": None })
@app.route("/players/matches/<int:matchId>", methods = ["POST"])
def players_create(matchId):
	name = request.form["name"]

	players = playerService.selectByName(name)
	if players.count() > 0:
		player = playerService.new()
		player.name = name
		return render_template("players/new.html", player = player, matchId = matchId, error = True)

	playerService.create(request.form)

	if matchId != None:
		return redirect("/matches/%d/players" % matchId)

	return redirect("/players")

@app.route("/players/<int:id>/edit", methods = ["GET"])
def players_edit(id):
	player = playerService.selectById(id)
	return render_template("players/edit.html", player = player)

@app.route("/players/<int:id>", methods = ["POST"])
def players_update(id):
	name = request.form["name"]

	players = playerService.excludeByName(id, name)
	if players.count() > 0:
		player = playerService.selectById(id)
		player.name = name
		return render_template("players/edit.html", player = player, error = True)

	playerService.update(id, name)

	return redirect("/players")

@app.route("/isms", methods = ["GET"])
def isms():
	return render_template("isms/index.html", isms = ismService.select())

@app.route("/isms.json", methods = ["GET"])
def isms_json():
	isms = ismService.select()
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

@app.route("/isms/new", methods = ["GET"])
def isms_new():
	ism = ismService.new()
	return render_template("isms/new.html", ism = ism)

@app.route("/isms", methods = ["POST"])
def isms_create():
	ismService.create(request.form)
	return redirect("/isms")

@app.route("/isms/<int:id>/edit", methods = ["GET"])
def isms_edit(id):
	ism = ismService.selectById(id)
	return render_template("isms/edit.html", ism = ism)

@app.route("/isms/<int:id>", methods = ["POST"])
def isms_update(id):
	ismService.update(id, request.form)
	return redirect("/isms")

@app.route("/isms/<int:id>/delete", methods = ["POST"])
def isms_delete(id):
	ismService.delete(id)
	return redirect("/isms")

@app.route("/leaderboard", methods = ["GET"], defaults = { "matchType": "singles" })
@app.route("/leaderboard/<path:matchType>", methods = ["GET"])
def leaderboard_index(matchType):
	if matchType not in singles.matchTypes:
		abort(404)

	stats = leaderboardService.matchTypeStats(matchType)
	return render_template("leaderboard/index.html", stats = stats, matchTypes = singles.matchTypes, matchType = matchType)

@app.route("/leaderboard.json", methods = ["GET"], defaults = { "matchType": "singles" })
@app.route("/leaderboard/<path:matchType>.json", methods = ["GET"])
def leaderboard_json(matchType):
	stats = leaderboardService.matchTypeStats(matchType)
	return Response(json.dumps(stats), status = 200, mimetype = "application/json")

@app.route("/leaderboard/players/<int:id>", methods = ["GET"])
def leaderboard_players(id):
	player = playerService.selectById(id)
	stats = leaderboardService.playerStats(player)
	return render_template("leaderboard/players.html", player = player, stats = stats, matchTypes = singles.matchTypes)

@app.route("/leaderboard/players/<int:id>.json", methods = ["GET"])
def leaderboard_players_json(id):
	player = playerService.selectById(id)
	stats = leaderboardService.playerStats(player)
	return Response(json.dumps(stats), status = 200, mimetype = "application/json")

@app.route("/rules", methods = ["GET"])
def rules():
	return render_template("rules/index.html")

@app.route("/buttons", methods = ["GET"])
def buttons():
	return render_template("buttons.html")

@app.route("/buttons/<path:button>/score", methods = ["POST"])
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

@app.route("/buttons/<path:button>/undo", methods = ["POST"])
def buttons_undo(button):
	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		matchType = getMatchType(match)
		data = matchType.undo(match, button)
	socketio.emit("response", data, broadcast = True)
	return button

@app.route("/buttons/<path:button>/delete-scores", methods = ["POST"])
def buttons_delete_scores(button):
	data = None
	match = matchService.selectActiveMatch()
	if match != None:
		scoreService.deleteByMatch(match.id)
		data = getMatchType(match).matchData(match)
	socketio.emit("response", data, broadcast = True)
	return button

@app.route("/debug-mode")
def debug_mode():
	if app.config["DEBUG"]:
		app.config["DEBUG_TOOLS"] = not app.config["DEBUG_TOOLS"]

	return redirect("/")

@app.route("/favicon.ico")
def favicon():
	return send_from_directory("{}/static/images".format(app.root_path), "ping-pong-icon.png", mimetype = "image/vnd.microsoft.icon")

@app.before_request
def beforeRequest():
	app.logger.access("%s \"%s %s\"", request.remote_addr, request.environ["REQUEST_METHOD"], request.url)

@app.after_request
def afterRequest(response):
	session.close()
	return response

@app.errorhandler(404)
def not_found(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/500.html"), 500

def getMatchType(match):
	if singles.isMatchType(match.matchType):
		return singles

	elif doubles.isMatchType(match.matchType):
		return doubles

	elif nines.isMatchType(match.matchType):
		return nines

if __name__ == "__main__":
	logger.setupLogging(app)
	assets.setupAssets(app)
	session = database.setupSession(app)

	ismService = IsmService.IsmService(session)
	playerService = PlayerService.PlayerService(session)
	matchService = MatchService.MatchService(session)
	scoreService = ScoreService.ScoreService(session)
	leaderboardService = LeaderboardService.LeaderboardService(session)
	pagingService = PagingService.PagingService()

	singles = Singles.Singles(session)
	doubles = Doubles.Doubles(session)
	nines = Nines.Nines(session)

	app.config["DEBUG_TOOLS"] = False

	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
