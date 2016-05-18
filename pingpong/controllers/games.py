from flask import Response, request, render_template, redirect
from datetime import datetime
from pingpong import app
from pingpong import model
from pingpong.entities import game as gameModel
from pingpong.entities import player as playerModel
from pingpong.entities import team as teamModel
from pingpong.entities import team_player as teamPlayerModel
import json

@app.route("/games/", methods = ["GET"])
def games_index():
	games = model.Model().select(gameModel.Game)
	return render_template("games/index.html", games = games)

@app.route("/games/new/", methods = ["GET"])
def games_new():
	games = model.Model().select(gameModel.Game)
	return render_template("games/new.html", games = games)

@app.route("/games/", methods = ["POST"])
def games_create():
	game = gameModel.Game(datetime.now())
	game.players = request.form["players"]
	game.ready = False
	game.complete = False
	model.Model().create(game)

	model.Model().create(teamModel.Team(game.id, 0, datetime.now()))
	model.Model().create(teamModel.Team(game.id, 0, datetime.now()))

	return redirect("/games/%d/players/" % game.id)

@app.route("/games/<int:id>/players/", methods = ["GET"])
def games_players(id):
	game = model.Model().selectById(gameModel.Game, id)
	players = model.Model().select(playerModel.Player)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)
	return render_template("games/players.html", players = players, teams = teams, game = game)

@app.route("/games/<int:id>/players/", methods = ["POST"])
def games_players_create(id):
	teamPlayer = teamPlayerModel.TeamPlayer(request.form["teamId"], request.form["playerId"])
	model.Model().create(teamPlayer)
	return Response(json.dumps({ "id": teamPlayer.id }), status = 200, mimetype = "application/json")

@app.route("/games/<int:id>/score/", methods = ["GET"])
def games_score(id):
	game = model.Model().selectById(gameModel.Game, id)
	return render_template("games/score.html", game = game)

@app.route("/games/<int:id>/score/", methods = ["POST"])
def games_score_update(id):
	game = model.Model().selectById(gameModel.Game, id)
	model.Model().update(gameModel.Game, id, {
		"playTo": request.form["playTo"],
		"ready": True
	})
	return redirect("/games/%d/play/" % game.id)


@app.route("/games/<int:id>/play/", methods = ["GET"])
def games_play(id):
	game = model.Model().selectById(gameModel.Game, id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)
	return render_template("games/play.html", game = game,  teams = teams)