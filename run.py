from gevent.wsgi import WSGIServer
from pingpong import app
app.config["DEBUG"] = False
app.config["PORT"] = 5000
app.config.from_pyfile("config_file.cfg")

if app.config["DEBUG"]:
	app.run(debug = True, host = "0.0.0.0", port = app.config["PORT"])
else:
	http_server = WSGIServer(('', app.config["PORT"]), app)
	http_server.serve_forever()