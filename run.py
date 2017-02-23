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

@app.route("/games/new", methods = ["GET"])
def games_new():
	return render_template("games-new.html")

@app.route("/games", methods = ["POST"])
def games_create():
	id = GameService().create(request.form["gametype"])
	return redirect("/games/%d/play-to" % id)

@app.route("/games/<int:id>/play-to", methods = ["GET"])
def games_play_to(id):
	game = GameService().selectById(id)
	title, template, default = GameService().getGameTypeAttributes(game)
	return render_template("games-play-to.html", game = game, default = default)

@app.route("/games/<int:id>/play-to", methods = ["POST"])
def games_play_to_update(id):
	GameService().updatePlayTo(id, request.form["playTo"])
	return redirect("/games/%d/players" % id)

@app.route("/games/<int:id>/players", methods = ["GET"])
def games_players(id):
	game = GameService().selectById(id)
	title, template, default = GameService().getGameTypeAttributes(game)
	players = PlayerService().select()
	return render_template(template, title = title, game = game, players = players)

@app.route("/games/<int:id>", methods = ["POST"])
def games_play(id):
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

class GameService():

	def selectById(self, id):
		return session.query(GameModel).filter(GameModel.id == id).one()

	def create(self, gameType):
		game = GameModel(gameType, datetime.now(), datetime.now())
		session.add(game)
		session.commit()

		return game.id

	def updatePlayTo(self, id, playTo):
		game = self.selectById(id)
		game.playTo = playTo
		game.updatedAt = datetime.now()
		session.commit()

	def getGameTypeAttributes(self, game):
		if game.gameType == "singles":
			return "Singles", "two-player.html", 21

		if game.gameType == "nines":
			return "9s", "four-player.html", 9

		if game.gameType == "doubles":
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

class GameModel(Base):
	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	gameType = Column(String)
	playTo = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)
	completedAt = Column(DateTime)

	def __init__(self, gameType, createdAt, modifiedAt):
		self.gameType = gameType
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
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"])
