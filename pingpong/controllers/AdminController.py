from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.matchtypes.MatchType import MatchType
from pingpong.services.MatchService import MatchService
from pingpong.services.OfficeService import OfficeService
from pingpong.utils import notifications
from pingpong.utils import util

adminController = Blueprint("adminController", __name__)

matchService = MatchService()
officeService = OfficeService()

@adminController.route("/admin", methods = ["GET"])
@loginRequired()
def index():
	offices = officeService.select()

	matchData = None
	match = matchService.selectActiveMatch(session["office"]["id"])
	if match != None:
		matchData = MatchType(match).matchData()

	return render_template("admin/index.html", matchData = matchData, offices = offices)

@adminController.route("/admin/send-message", methods = ["POST"])
@loginRequired("adminController.index")
def send_message():
	message = util.paramForm("message")

	if message != None and len(message) > 0:
		notifications.send(message)
		flash("Message has been sent.", "success")
	else:
		flash("Message was malformed and was not be sent.", "danger")

	return redirect(url_for("adminController.index"))
