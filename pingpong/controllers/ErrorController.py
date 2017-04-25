from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request

errorController = Blueprint("errorController", __name__)

@errorController.app_errorhandler(400)
def bad_request(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/400.html"), 400

@errorController.app_errorhandler(404)
def not_found(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/404.html"), 404

@errorController.app_errorhandler(500)
def server_error(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/500.html"), 500
