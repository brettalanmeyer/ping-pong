from flask import Flask, send_from_directory, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pingpong.utils import assets, logger
from pingpong.controllers.MainController import mainController
from pingpong.controllers.PlayerController import playerController
from pingpong.controllers.IsmController import ismController
from pingpong.controllers.MatchController import matchController
from pingpong.controllers.LeaderboardController import leaderboardController
from pingpong.controllers.RulesController import rulesController
from pingpong.controllers.ButtonsController import buttonsController

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db = SQLAlchemy(app, session_options = { "autocommit": False, "autoflush": False })

logger.setupLogging(app)
assets.setupAssets(app)

app.url_map.strict_slashes = False

app.register_blueprint(mainController)
app.register_blueprint(playerController)
app.register_blueprint(ismController)
app.register_blueprint(matchController)
app.register_blueprint(leaderboardController)
app.register_blueprint(rulesController)
app.register_blueprint(buttonsController)

@app.before_request
def beforeRequest():
	app.logger.access("%s \"%s %s\"", request.remote_addr, request.environ["REQUEST_METHOD"], request.url)

@app.after_request
def afterRequest(response):
	db.session.close()
	return response

@app.errorhandler(404)
def not_found(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error(error):
	app.logger.error(error)
	app.logger.error(request.url)
	return render_template("errors/500.html"), 500
