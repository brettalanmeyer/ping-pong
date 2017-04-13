from pingpong import create_app, socketio

app = create_app(debug = True)

if __name__ == "__main__":
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
