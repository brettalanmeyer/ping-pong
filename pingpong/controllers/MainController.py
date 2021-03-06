from datetime import datetime
from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from pingpong.forms.FeedbackForm import FeedbackForm
from pingpong.services.MatchService import MatchService
from pingpong.services.OfficeService import OfficeService
from pingpong.services.ScoreService import ScoreService
from pingpong.utils import database as db
from pingpong.utils import notifications

mainController = Blueprint("mainController", __name__)

matchService = MatchService()
scoreService = ScoreService()
feedbackForm = FeedbackForm()
officeService = OfficeService()

@mainController.route("/", methods = ["GET"])
def index():
	matches = matchService.selectComplete().count()
	scores = scoreService.selectCount()
	session["offices"] = officeService.load()
	return render_template("main/index.html", matches = matches, scores = scores)

@mainController.route("/favicon.ico")
def favicon():
	return send_from_directory("{}/static/images".format(app.root_path), "ping-pong-icon.png", mimetype = "image/vnd.microsoft.icon")

@mainController.route("/rules", methods = ["GET"])
def rules():
	return render_template("main/rules.html")

@mainController.route("/change-log", methods = ["GET"])
def changeLog():
	return render_template("main/change-log.html")

@mainController.route("/feedback", methods = ["GET"])
def feedback():
	return render_template("main/feedback.html")

@mainController.route("/feedback", methods = ["POST"])
def send_feedback():
	hasErrors = feedbackForm.validate(request.form)

	if hasErrors:
		return render_template("main/feedback.html"), 400

	else:
		notifications.mailFeedback(request.form["name"], request.form["email"], request.form["message"])
		flash("Thank you for your feedback!", "success")
		return redirect(url_for("mainController.index"))

@mainController.before_app_request
def beforeRequest():
	app.logger.access("%s \"%s %s\"", request.remote_addr, request.environ["REQUEST_METHOD"], request.url)

	if "offices" not in session:
		session["offices"] = officeService.load()

	if request.endpoint != "static":
		if "office" not in session:
			if request.endpoint != None:
				if not (request.endpoint.startswith("apiController") or request.endpoint == "mainController.favicon" or request.endpoint == "officeController.select" or request.endpoint == "officeController.set"):
					next = url_for(request.endpoint, **request.view_args)
					return redirect(url_for("officeController.select", next = next))

@mainController.after_app_request
def afterRequest(response):
	db.session.close()
	return response
