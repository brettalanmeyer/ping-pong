from flask import Flask, render_template, Response, redirect, request
from flask_assets import Environment
from flask_socketio import SocketIO, emit
import json
from utils import database, logger
from services import IsmService, PlayerService, MatchService, ScoreService, LeaderboardService, PagingService
from matchtypes import Singles, Doubles, Nines

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
assets = Environment(app)
socketio = SocketIO(app)

@app.route("/", methods = ["GET"])
def index():
	matches = matchService.selectComplete()
	return render_template("main/index.html", num = matches.count())

@app.route("/matches", methods = ["GET"], defaults = { "page": 1 })
@app.route("/matches/page/<int:page>", methods = ["GET"])
def matches_index(page):
	matches = pagingService.pager(matchService.selectComplete(), page)
	return render_template("matches/index.html", matches = matches, paging = pagingService.data())

@app.route("/matches/new", methods = ["GET"])
def matches_new():
	return render_template("matches/new.html")

@app.route("/matches", methods = ["POST"])
def matches_create():
	match = matchService.create(request.form["matchType"])
	return redirect("/matches/%d/play-to" % match.id)

@app.route("/matches/delete", methods = ["POST"])
def matches_delete():
	matchService.deleteAll()
	return redirect("/?debug=true")

@app.route("/matches/<int:id>/play-to", methods = ["GET"])
def matches_play_to(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	return render_template("matches/play-to.html", match = match, default = matchType.defaultPoints)

@app.route("/matches/<int:id>/play-to", methods = ["POST"])
def matches_play_to_update(id):
	match = matchService.updatePlayTo(id, request.form["playTo"])
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
	return render_template(matchType.playerTemplate, title = matchType.label, match = match, players = players)

@app.route("/matches/<int:id>/players", methods = ["POST"])
def matches_players_create(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	matchType.createTeams(match, request.form)
	matchService.play(match)
	return redirect("/matches/%d" % id)

@app.route("/matches/<int:id>", methods = ["GET"])
def matches(id):
	match = matchService.selectById(id)
	matchType = getMatchType(match)
	data = matchType.matchData(match)
	isms = ismService.select()
	return render_template(data["template"], data = data, isms = ismService.serialize(isms))

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

	newMatch = matchType.playAgain(match)
	return redirect("/matches/%d" % newMatch.id)

@app.route("/players", methods = ["GET"])
def players():
	return render_template("players/index.html", players = playerService.select())

@app.route("/players/new", methods = ["GET"])
def players_new():
	player = playerService.new()
	return render_template("players/new.html", player = player)

@app.route("/players", methods = ["POST"])
def players_create():
	name = request.form["name"]

	players = playerService.selectByName(name)
	if players.count() > 0:
		player = playerService.new()
		player.name = name
		return render_template("players/new.html", player = player, error = True)

	playerService.create(request.form)

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

@app.route("/leaderboard", methods = ["GET"])
def leaderboard_index():
	stats = leaderboardService.stats()
	return render_template("leaderboard/index.html", stats = stats)

@app.route("/leaderboard.json", methods = ["GET"])
def leaderboard_json():
	stats = leaderboardService.stats()
	return Response(json.dumps(stats), status = 200, mimetype = "application/json")

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
			newMatch = matchType.playAgain(latestMatch)
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

	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
