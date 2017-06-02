from flask_assets import Environment, Bundle

def setupAssets(app):
	assets = Environment(app)
	assets.init_app(app)
	assets.register("js_all", bundleJavascripts())
	assets.register("css_all", bundleStylesheets())

def bundleJavascripts():
	return Bundle(
		"libraries/jquery.min.js",
		"libraries/socket.io.min.js",
		"libraries/stupidtable.min.js",
		"javascripts/app.js",
		"javascripts/hash-manager.js",
		"javascripts/isms.js",
		"javascripts/singles.js",
		"javascripts/doubles.js",
		"javascripts/nines.js",
		"javascripts/players.js",
		"javascripts/smack-talk.js",
		"javascripts/scoring-tools.js",
		"javascripts/leaderboard.js",
		filters = "jsmin",
		output = ".webassets-cache/ping-pong.min.js"
	)

def bundleStylesheets():
	return Bundle(
		"stylesheets/app.css",
		"stylesheets/singles.css",
		"stylesheets/doubles.css",
		"stylesheets/nines.css",
		"stylesheets/leaderboard.css",
		"stylesheets/debug.css",
		"stylesheets/players.css",
		"stylesheets/scoring-tools.css",
		filters = "cssmin",
		output = ".webassets-cache/ping-pong.min.css"
	)
