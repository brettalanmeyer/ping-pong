from flask import abort
from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response
from pingpong.services.IsmService import IsmService
from pingpong.services.MatchService import MatchService
from pingpong.services.OfficeService import OfficeService
from pingpong.services.PlayerService import PlayerService
from pingpong.utils import util
import json

from flask import current_app as app

apiController = Blueprint("apiController", __name__)

ismService = IsmService()
matchService = MatchService()
officeService = OfficeService()
playerService = PlayerService()

@apiController.route("/api", methods = ["GET"])
def index():
	return render_template("api/index.html")

@apiController.route("/api/isms.json", methods = ["GET"])
def isms():
	office = validateOffice()
	isms = ismService.selectApproved(office.id)
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

@apiController.route("/api/matches.json", methods = ["GET"])
def matches():
	office = validateOffice()
	matches = matchService.select(office.id)
	return Response(matchService.serializeMatches(matches), status = 200, mimetype = "application/json")

@apiController.route("/api/matches/<int:matchId>.json", methods = ["GET"])
def match(matchId):
	office = validateOffice()
	match = matchService.selectById(matchId)
	return Response(matchService.serializeMatch(match), status = 200, mimetype = "application/json")

@apiController.route("/api/players.json", methods = ["GET"])
def players():
	office = validateOffice()
	players = playerService.select()
	return Response(playerService.serialize(players), status = 200, mimetype = "application/json")

def validateOffice():
	key = None

	if "key" in request.form:
		key = request.form["key"]

	if key == None:
		key = request.args.get("key")

	if key == None:
		abort(400)

	office = officeService.selectByHash(key)

	if office == None:
		abort(400)

	return office
