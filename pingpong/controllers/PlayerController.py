from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from pingpong.forms.PlayerForm import PlayerForm
from pingpong.services.PlayerService import PlayerService
from pingpong.utils import notifications

playerController = Blueprint("playerController", __name__)

playerService = PlayerService()
playerForm = PlayerForm()

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
	hasErrors = playerForm.validate(None, request.form)

	if hasErrors:
		player = playerService.new()
		playerForm.load(player, request.form)
		return render_template("players/new.html", player = player, matchId = matchId), 400
	else:
		player = playerService.create(request.form)

		message = "<b>{}</b> has joined ping pong. Please consider adding them to the ping pong chat group.".format(player.name)
		notifications.send(message)

		if matchId != None:
			return redirect("/matches/%d/players" % matchId)
		else:
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
	hasErrors = playerForm.validate(id, request.form)

	player = playerService.selectById(id)
	originalName = player.name

	if hasErrors:
		playerForm.load(player, request.form)
		return render_template("players/edit.html", player = player), 400

	else:
		updatedPlayer = playerService.update(id, request.form)
		newName = updatedPlayer.name

		flash("Player '{}' has been successfully updated.".format(updatedPlayer.name), "success")

		if originalName != newName:
			message = "<b>{}</b> is now known as <b>{}</b>.".format(originalName, newName)
			notifications.send(message)

		return redirect("/players")
