from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from pingpong.services.PlayerService import PlayerService

playerController = Blueprint("playerController", __name__)

playerService = PlayerService()

@playerController.route("/players", methods = ["GET"])
def players():
	return render_template("players/index.html", players = playerService.select())

@playerController.route("/players/new", methods = ["GET"], defaults = { "matchId": None })
@playerController.route("/players/new/matches/<int:matchId>", methods = ["GET"])
def players_new(matchId):
	player = playerService.new()
	return render_template("players/new.html", player = player, matchId = matchId)

@playerController.route("/players", methods = ["POST"], defaults = { "matchId": None })
@playerController.route("/players/matches/<int:matchId>", methods = ["POST"])
def players_create(matchId):
	name = request.form["name"]

	players = playerService.selectByName(name)
	if players.count() > 0:
		player = playerService.new()
		player.name = name
		flash("The name '{}' is already taken. Please specify a unique name.".format(name), "danger")
		return render_template("players/new.html", player = player, matchId = matchId)

	playerService.create(request.form)

	if matchId != None:
		return redirect("/matches/%d/players" % matchId)

	flash("Player '{}' has been successfully created.".format(name), "success")
	return redirect("/players")

@playerController.route("/players/<int:id>/edit", methods = ["GET"])
def players_edit(id):
	player = playerService.selectById(id)

	if player == None:
		flash("Player {} does not exist.".format(id), "warning")
		return redirect("/players")

	return render_template("players/edit.html", player = player)

@playerController.route("/players/<int:id>", methods = ["POST"])
def players_update(id):
	name = request.form["name"]

	players = playerService.excludeByName(id, name)
	if players.count() > 0:
		player = playerService.selectById(id)
		player.name = name
		flash("The name '{}' is already taken. Please specify a unique name.".format(name), "danger")
		return render_template("players/edit.html", player = player)

	playerService.update(id, name)

	flash("Player '{}' has been successfully updated.".format(name), "success")
	return redirect("/players")