from flask import Response, request, render_template, redirect
from datetime import datetime
from pingpong import app
from pingpong import model
from pingpong.entities import game as gameModel
from pingpong.entities import player as playerModel
from pingpong.entities import team as teamModel
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
	model.Model().create(game)
	return redirect("/games/%d/players/" % game.id)

@app.route("/games/<int:id>/players/", methods = ["GET"])
def games_players(id):
	game = model.Model().selectById(gameModel.Game, id)
	players = model.Model().select(playerModel.Player)
	return render_template("games/players.html", players = players, game = game)

@app.route("/games/<int:id>/players/", methods = ["POST"])
def games_players_create(id):
	team = teamModel.Team(request.form["gameId"], request.form["playerId"], request.form["team"], datetime.now())
	model.Model().create(team)
	return Response(json.dumps({ "id": team.id }), status = 200, mimetype = "application/json")
