from pingpong.app import app
from pingpong.app import sio
import sys
import eventlet
import socketio

def setEncoding():
	reload(sys)
	sys.setdefaultencoding("UTF8")

if __name__ == "__main__":
	setEncoding()

	pingpongapp = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen((app.config["HOST"], app.config["PORT"])), pingpongapp, debug = app.config["DEBUG"])

	# socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
