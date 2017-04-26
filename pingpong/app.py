from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO

from pingpong.utils import assets
from pingpong.utils import logger

app = Flask(__name__)
app.config.from_pyfile("../config.cfg")

logger.setupLogging(app)
assets.setupAssets(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authenticationController.login"

app.url_map.strict_slashes = False

socketio = SocketIO()
socketio.init_app(app)

from pingpong.controllers.AuthenticationController import authenticationController
from pingpong.controllers.ButtonController import buttonController
from pingpong.controllers.ErrorController import errorController
from pingpong.controllers.IsmController import ismController
from pingpong.controllers.LeaderboardController import leaderboardController
from pingpong.controllers.MainController import mainController
from pingpong.controllers.MatchController import matchController
from pingpong.controllers.PlayerController import playerController
from pingpong.controllers.RuleController import ruleController

app.register_blueprint(authenticationController)
app.register_blueprint(buttonController)
app.register_blueprint(errorController)
app.register_blueprint(ismController)
app.register_blueprint(leaderboardController)
app.register_blueprint(mainController)
app.register_blueprint(matchController)
app.register_blueprint(playerController)
app.register_blueprint(ruleController)
