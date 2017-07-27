from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session

from pingpong.utils import assets
from pingpong.utils import logger

app = Flask(__name__)
app.config.from_pyfile("../config.cfg")

logger.setupLogging(app)

assets.setupAssets(app)

login_manager = LoginManager()
login_manager.init_app(app)

if app.config["DEBUG"]:
	from flask_socketio import SocketIO
	socketio = SocketIO()
	socketio.init_app(app)
else:
	import socketio as SocketIO
	socketio = SocketIO.Server()

mail = Mail()
mail.init_app(app)

sess = Session()
sess.init_app(app)

app.url_map.strict_slashes = False

from pingpong.controllers.AdminController import adminController
from pingpong.controllers.ApiController import apiController
from pingpong.controllers.AuthenticationController import authenticationController
from pingpong.controllers.ErrorController import errorController
from pingpong.controllers.IsmController import ismController
from pingpong.controllers.LeaderboardController import leaderboardController
from pingpong.controllers.MainController import mainController
from pingpong.controllers.MatchController import matchController
from pingpong.controllers.OfficeController import officeController
from pingpong.controllers.PlayerController import playerController

app.register_blueprint(adminController)
app.register_blueprint(apiController)
app.register_blueprint(authenticationController)
app.register_blueprint(errorController)
app.register_blueprint(ismController)
app.register_blueprint(leaderboardController)
app.register_blueprint(mainController)
app.register_blueprint(matchController)
app.register_blueprint(officeController)
app.register_blueprint(playerController)
