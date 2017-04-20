from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from pingpong.forms.PlayerForm import PlayerForm
from pingpong.services.PlayerService import PlayerService

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
		return render_template("players/new.html", player = player, matchId = matchId)
	else:
		playerService.create(request.form)

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

	if hasErrors:
		player = playerService.selectById(id)
		playerForm.load(player, request.form)
		return render_template("players/edit.html", player = player)
	else:
		player = playerService.update(id, request.form)
		flash("Player '{}' has been successfully updated.".format(player.name), "success")
		return redirect("/players")
