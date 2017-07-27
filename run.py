from pingpong.app import app
from pingpong.app import socketio
import sys

def setEncoding():
	reload(sys)
	sys.setdefaultencoding("UTF8")

if __name__ == "__main__":
	setEncoding()
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
