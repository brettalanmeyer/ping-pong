from flask_socketio import SocketIO
from pingpong import app

socketio = SocketIO(app)

if __name__ == "__main__":
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
