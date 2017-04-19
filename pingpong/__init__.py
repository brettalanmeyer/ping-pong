from flask import Flask
from flask_socketio import SocketIO
from pingpong.controllers.ButtonController import buttonController
from pingpong.controllers.IsmController import ismController
from pingpong.controllers.LeaderboardController import leaderboardController
from pingpong.controllers.MainController import mainController
from pingpong.controllers.MatchController import matchController
from pingpong.controllers.PlayerController import playerController
from pingpong.controllers.RuleController import ruleController
from pingpong.utils import assets
from pingpong.utils import logger
from pingpong.utils.cache import cache

socketio = SocketIO()

def create_app(debug = False):
	app = Flask(__name__)
	app.config.from_pyfile("../config.cfg")

	logger.setupLogging(app)
	assets.setupAssets(app)
	cache.init_app(app)

	app.url_map.strict_slashes = False

	app.register_blueprint(mainController)
	app.register_blueprint(playerController)
	app.register_blueprint(ismController)
	app.register_blueprint(matchController)
	app.register_blueprint(leaderboardController)
	app.register_blueprint(ruleController)
	app.register_blueprint(buttonController)

	socketio.init_app(app)

	app.socketio = socketio

	return app
