from flask import Flask, render_template, Response,redirect, request
from flask.ext.assets import Environment, Bundle
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import random, json

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
assets = Environment(app)
socketio = SocketIO(app)

def makeDatabaseConnection():
	engine = create_engine("mysql+mysqldb://" + app.config["MYSQL_USERNAME"] + ":" + app.config["MYSQL_PASSWORD"] + "@" + app.config["MYSQL_HOST"] + "/" + app.config["MYSQL_DATABASE"], pool_recycle = 3600)
	db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
	Session = sessionmaker(bind = engine)
	session = Session()
	Base = declarative_base()

	return session, Base

session, Base = makeDatabaseConnection()

@app.route("/", methods = ["GET"])
def index():
	return render_template("index.html")

@app.route("/matches/new", methods = ["GET"])
def matches_new():
	return render_template("matches-new.html")

@app.route("/matches", methods = ["POST"])
def matches_create():
	id = MatchService().create(request.form["matchType"])
	return redirect("/matches/%d/play-to" % id)

@app.route("/matches/<int:id>/play-to", methods = ["GET"])
def matches_play_to(id):
	match = MatchService().selectById(id)
	title, template, default = MatchService().getMatchTypeAttributes(match)
	return render_template("matches-play-to.html", match = match, default = default)

@app.route("/matches/<int:id>/play-to", methods = ["POST"])
def matches_play_to_update(id):
	MatchService().updatePlayTo(id, request.form["playTo"])
	return redirect("/matches/%d/players" % id)

@app.route("/matches/<int:id>/players", methods = ["GET"])
def matches_players(id):
	match = MatchService().selectById(id)
	title, template, default = MatchService().getMatchTypeAttributes(match)
	players = PlayerService().select()
	return render_template(template, title = title, match = match, players = players)

@app.route("/matches/<int:id>", methods = ["POST"])
def matches_play(id):
	return Response(json.dumps(request.form), status = 200, mimetype = "application/json")

@app.route("/players", methods = ["GET"])
def players():
	return render_template("players.html", players = PlayerService().select())

@app.route("/players/new", methods = ["GET"])
def players_new():
	return render_template("players-new.html")

@app.route("/players", methods = ["POST"])
def players_create():
	name = request.form["name"]

	players = session.query(PlayerModel).filter_by(name = name)
	if players.count() > 0:
		return render_template("players-new.html", name = name, error = True)

	PlayerService().create(name)

	return redirect("/players")

@app.route("/players/<int:id>/edit", methods = ["GET"])
def players_edit(id):
	player = session.query(PlayerModel).filter(PlayerModel.id == id).one()
	return render_template("players-edit.html", player = player)

@app.route("/players/<int:id>", methods = ["POST"])
def players_update(id):
	name = request.form["name"]
	player = PlayerService().selectById(id)
	player.name = name

	players = session.query(PlayerModel).filter(PlayerModel.id != id, PlayerModel.name == name)
	if players.count() > 0:
		return render_template("players-edit.html", player = player, error = True)

	PlayerService().update(id, name)

	return redirect("/players")

@app.route("/buttons", methods = ["GET"])
def buttons():
	return render_template("buttons.html")

@app.route("/buttons/score", methods = ["POST"])
def buttons_score():
	print("buttons score: ")
	print(request.form["button"])
	return "buttons score"

@app.route("/buttons/undo", methods = ["POST"])
def buttons_undo():
	print("buttons undo")
	return "buttons undo"

@app.route("/buttons/new", methods = ["POST"])
def buttons_new():
	print("buttons new")
	return "buttons new"

@app.after_request
def afterRequest(response):
	session.close()
	return response

@app.errorhandler(404)
def not_found(error):
	return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
	return render_template("500.html"), 500

class MatchService():

	def selectById(self, id):
		return session.query(MatchModel).filter(MatchModel.id == id).one()

	def create(self, matchType):
		match = MatchModel(matchType, datetime.now(), datetime.now())
		session.add(match)
		session.commit()

		return match.id

	def updatePlayTo(self, id, playTo):
		match = self.selectById(id)
		match.playTo = playTo
		match.updatedAt = datetime.now()
		session.commit()

	def getMatchTypeAttributes(self, match):
		if match.matchType == "singles":
			return "Singles", "two-player.html", 21

		if match.matchType == "nines":
			return "9s", "four-player.html", 9

		if match.matchType == "doubles":
			return "Doubles", "four-player.html", 21

class PlayerService():

	def select(self):
		return session.query(PlayerModel).order_by(PlayerModel.name)

	def selectById(self, id):
		return session.query(PlayerModel).filter(PlayerModel.id == id).one()

	def create(self, name):
		player = PlayerModel(name, datetime.now(), datetime.now())
		session.add(player)
		session.commit()

	def update(self, id, name):
		player = self.selectById(id)
		player.name = name
		player.updatedAt = datetime.now()
		session.commit()

class MatchModel(Base):

	__tablename__ = "matches"

	id = Column(Integer, primary_key = True)
	matchType = Column(String)
	playTo = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)
	completedAt = Column(DateTime)

	def __init__(self, matchType, createdAt, modifiedAt):
		self.matchType = matchType
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class PlayerModel(Base):

	__tablename__ = "players"

	id = Column(Integer, primary_key = True)
	name = Column(String)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, name, createdAt, modifiedAt):
		self.name = name
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

if __name__ == "__main__":
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
