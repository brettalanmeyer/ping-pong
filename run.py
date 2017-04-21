from pingpong import create_app, socketio
import sys

app = create_app(debug = True)

def setEncoding():
	reload(sys)
	sys.setdefaultencoding("UTF8")

if __name__ == "__main__":
	setEncoding()
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
