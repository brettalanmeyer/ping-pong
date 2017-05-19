from flask import Blueprint
from flask import render_template
from flask import Response
from pingpong.services.IsmService import IsmService
from pingpong.services.PlayerService import PlayerService
import json

apiController = Blueprint("apiController", __name__)

playerService = PlayerService()
ismService = IsmService()

@apiController.route("/api", methods = ["GET"])
def index():
	return render_template("api/index.html")

@apiController.route("/api/players.json", methods = ["GET"])
def players():
	players = playerService.select()
	return Response(playerService.serialize(players), status = 200, mimetype = "application/json")

@apiController.route("/api/isms.json", methods = ["GET"])
def isms():
	isms = ismService.selectApproved()
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

