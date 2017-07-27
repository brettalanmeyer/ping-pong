from pingpong.app import app
from pingpong.app import socketio
import sys

def setEncoding():
	reload(sys)
	sys.setdefaultencoding("UTF8")

if __name__ == "__main__":
	setEncoding()

	if app.config["DEBUG"]:
		socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = True)
	else:
		import eventlet
		import socketio as SocketIO
		pingpongapp = SocketIO.Middleware(socketio, app)
		eventlet.wsgi.server(eventlet.listen((app.config["HOST"], app.config["PORT"])), pingpongapp, debug = False)
