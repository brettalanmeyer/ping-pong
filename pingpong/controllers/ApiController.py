from flask import Blueprint
from flask import render_template
from flask import Response
from pingpong.services.GameService import GameService
from pingpong.services.IsmService import IsmService
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.ScoreService import ScoreService
from pingpong.services.TeamService import TeamService
import json

from flask import current_app as app

apiController = Blueprint("apiController", __name__)

ismService = IsmService()
matchService = MatchService()
playerService = PlayerService()
gameService = GameService()
teamService = TeamService()
scoreService = ScoreService()

@apiController.route("/api", methods = ["GET"])
def index():
	return render_template("api/index.html")

@apiController.route("/api/isms.json", methods = ["GET"])
def isms():
	isms = ismService.selectApproved()
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

@apiController.route("/api/matches.json", methods = ["GET"])
def matches():
	matches = matchService.select()
	return Response(matchService.serializeMatches(matches), status = 200, mimetype = "application/json")

@apiController.route("/api/matches/<int:matchId>.json", methods = ["GET"])
def match(matchId):
	match = matchService.selectById(matchId)
	return Response(matchService.serializeMatch(match), status = 200, mimetype = "application/json")

@apiController.route("/api/games.json", methods = ["GET"])
def games():
	games = gameService.select()
	return Response(gameService.serialize(games), status = 200, mimetype = "application/json")

@apiController.route("/api/matches/<int:matchId>/teams.json", methods = ["GET"])
def teams(matchId):
	teams = teamService.selectByMatchId(matchId)
	return Response(teamService.serialize(teams), status = 200, mimetype = "application/json")


@apiController.route("/api/match/<int:matchId>/scores.json", methods = ["GET"])
def scores(matchId):
	scores = scoreService.selectByMatchId(matchId)
	return Response(scoreService.serialize(scores), status = 200, mimetype = "application/json")

@apiController.route("/api/players.json", methods = ["GET"])
def players():
	players = playerService.select()
	return Response(playerService.serialize(players), status = 200, mimetype = "application/json")