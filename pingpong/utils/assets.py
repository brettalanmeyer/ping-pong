from flask_assets import Environment
from flask_assets import Bundle
import os

def setupAssets(app):
	createStorage()
	assets = Environment(app)
	assets.init_app(app)
	assets.register("js_all", bundleJavascripts())
	assets.register("css_all", bundleStylesheets())

def bundleJavascripts():
	return Bundle(
		"libraries/jquery.min.js",
		"libraries/socket.io.min.js",
		"libraries/stupidtable.min.js",
		"libraries/moment/moment.min.js",
		"libraries/bootstrap/js/bootstrap.min.js",
		"libraries/bootstrap-datetimepicker/bootstrap-datetimepicker.js",
		"javascripts/app.js",
		"javascripts/hash-manager.js",
		"javascripts/ping-pong-sound.js",
		"javascripts/isms.js",
		"javascripts/singles.js",
		"javascripts/doubles.js",
		"javascripts/nines.js",
		"javascripts/players.js",
		"javascripts/smack-talk.js",
		"javascripts/scoring-tools.js",
		"javascripts/leaderboard.js",
		"javascripts/match-entry.js",
		"javascripts/courtesies.js",
		filters = "jsmin",
		output = ".webassets-cache/ping-pong.min.js"
	)

def bundleStylesheets():
	return Bundle(
		"libraries/bootstrap-datetimepicker/bootstrap-datetimepicker.css",
		"stylesheets/app.css",
		"stylesheets/singles.css",
		"stylesheets/doubles.css",
		"stylesheets/nines.css",
		"stylesheets/leaderboard.css",
		"stylesheets/debug.css",
		"stylesheets/players.css",
		"stylesheets/scoring-tools.css",
		"stylesheets/match-entry.css",
		filters = "cssmin",
		output = ".webassets-cache/ping-pong.min.css"
	)

def createStorage():
	dirs = [
		"avatars",
		"logs",
		"sessions"
	]
	createDirectories(dirs)

def createDirectories(directories):
	for directory in directories:
		path = "pingpong/storage/{}".format(directory)
		if not os.path.exists(path):
			os.makedirs(path)
