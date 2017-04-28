from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request

errorController = Blueprint("errorController", __name__)

@errorController.app_errorhandler(400)
def errors_bad_request(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/400.html"), 400

@errorController.route("/errors/bad-request", methods = ["GET"])
def errors_bad_request_show():
	return render_template("errors/400.html"), 400

@errorController.app_errorhandler(404)
def errors_not_found(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/404.html"), 404

@errorController.route("/errors/not-found", methods = ["GET"])
def errors_not_found_show():
	return render_template("errors/404.html"), 404

@errorController.app_errorhandler(500)
def errors_server_error(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/500.html"), 500

@errorController.route("/errors/server-error", methods = ["GET"])
def errors_server_error_show():
	return render_template("errors/500.html"), 500
