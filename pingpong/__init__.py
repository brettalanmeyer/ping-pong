import os
from flask import Flask, request, render_template
from flask.ext.assets import Environment, Bundle
from flask_mail import Mail

app = Flask(__name__)
assets = Environment(app)

app.config["MAIL_SERVER"] = ""
app.config["MAIL_PORT"] = ""
app.config["MAIL_USE_SSL"] = ""
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""

app.config.from_pyfile("config_mail.cfg")

mail = Mail(app)

from pingpong.controllers import main
from pingpong.controllers import players
from pingpong.controllers import games

@app.errorhandler(404)
def not_found(error):
    return render_template("main/404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("main/500.html"), 500

@app.after_request
def beforeRequest(response):
	try:
		model.Model().close()
	except:
		print("cannot close model")
	return response

if __name__ == "__main__":
	app.run()
