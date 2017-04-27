from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request
from flask import send_from_directory
from pingpong.services.MatchService import MatchService
from pingpong.services.ScoreService import ScoreService
from pingpong.utils import database as db
from pingpong.utils import util

mainController = Blueprint("mainController", __name__)

matchService = MatchService()
scoreService = ScoreService()

@mainController.route("/", methods = ["GET"])
def index():
	matches = matchService.selectComplete().count()
	scores = scoreService.selectCount()
	return render_template("main/index.html", matches = matches, scores = scores)

@mainController.route("/favicon.ico")
def favicon():
	return send_from_directory("{}/static/images".format(app.root_path), "ping-pong-icon.png", mimetype = "image/vnd.microsoft.icon")

@mainController.before_app_request
def beforeRequest():
	app.logger.access("%s \"%s %s\"", request.remote_addr, request.environ["REQUEST_METHOD"], request.url)

@mainController.after_app_request
def afterRequest(response):
	db.session.close()
	return response
