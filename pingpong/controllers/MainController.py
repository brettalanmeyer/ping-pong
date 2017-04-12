from flask import Blueprint, render_template, request, current_app as app
from flask_sqlalchemy import SQLAlchemy
from pingpong.services import MatchService, ScoreService, TeamService

mainController = Blueprint("mainController", __name__)

db = SQLAlchemy()

matchService = MatchService.MatchService()
scoreService = ScoreService.ScoreService()

@mainController.route("/")
def index():
	matches = matchService.selectComplete().count()
	scores = scoreService.selectCount()

	return render_template("main/index.html", matches = matches, scores = scores)

@mainController.route("/favicon.ico")
def favicon():
	return send_from_directory("{}/static/images".format(app.root_path), "ping-pong-icon.png", mimetype = "image/vnd.microsoft.icon")
