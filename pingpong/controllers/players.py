from flask import request, render_template, redirect
from datetime import datetime
from pingpong import app
from pingpong import model
from pingpong.entities import player as playerModel

@app.route("/players/", methods = ["GET"])
def players_index():
	players = model.Model().select(playerModel.Player).order_by(playerModel.Player.name)
	return render_template("players/index.html", players = players)

@app.route("/players/new/", methods = ["GET"])
def players_new():
	return render_template("players/new.html", error = False)

@app.route("/players/matches/<int:matchId>/new/", methods = ["GET"])
def players_new_match(matchId):
	return render_template("players/new.html")

@app.route("/players/", methods = ["POST"])
def players_create():
	players = model.Model().select(playerModel.Player).filter_by(name = request.form["name"])

	if players.count() > 0:
		return render_template("players/new.html", name = request.form["name"], error = True)

	newPlayer = playerModel.Player(request.form["name"], datetime.now())
	model.Model().create(newPlayer)

	return redirect("/players/")

@app.route("/players/<int:id>/edit/", methods = ["GET"])
def players_edit(id):
	player = model.Model().selectById(playerModel.Player, id)
	return render_template("players/edit.html", player = player, error = False)

@app.route("/players/<int:id>/", methods = ["POST"])
def players_update(id):
	players = model.Model().select(playerModel.Player).filter_by(name = request.form["name"]).filter(playerModel.Player.id != id)

	if players.count() > 0:
		player = model.Model().selectById(playerModel.Player, id)
		player.name = request.form["name"]
		return render_template("players/edit.html", player = player, error = True)

	model.Model().update(playerModel.Player, id, request.form)
	return redirect("/players/")

@app.route("/players/<int:id>/delete/", methods = ["POST"])
def players_delete(id):
	model.Model().delete(playerModel.Player, id)
	return redirect("/players/")

