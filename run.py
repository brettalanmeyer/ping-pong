from flask import Flask, render_template, Response,redirect, request
from flask.ext.assets import Environment, Bundle
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
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

@app.route("/relationships", methods = ["GET"])
def relationships():
	matches = session.query(MatchModel)
	print(matches.count())
	for match in matches:
		print("matchId: " + str(match.id))
		teams = match.teams
		len(teams)
		for team in teams:
			print("teamId: " + str(team.id))

			for teamPlayer in team.teamPlayers:
				print("player: " + teamPlayer.player.name)
	return "relationships"

@app.route("/", methods = ["GET"])
def index():
	return render_template("main/index.html")

@app.route("/matches", methods = ["GET"])
def matches_index():
	matches = MatchService().select()
	return render_template("matches/index.html", matches = matches)

@app.route("/matches/new", methods = ["GET"])
def matches_new():
	return render_template("matches/new.html")

@app.route("/matches", methods = ["POST"])
def matches_create():
	match = MatchService().create(request.form["matchType"])
	return redirect("/matches/%d/play-to" % match.id)

@app.route("/matches/<int:id>/play-to", methods = ["GET"])
def matches_play_to(id):
	match = MatchService().selectById(id)
	title, template, default = MatchService().getMatchTypeAttributes(match)
	return render_template("matches/play-to.html", match = match, default = default)

@app.route("/matches/<int:id>/play-to", methods = ["POST"])
def matches_play_to_update(id):
	match = MatchService().updatePlayTo(id, request.form["playTo"])

	if match.matchType == "nines":
		return redirect("/matches/%d/players" % id)

	return redirect("/matches/%d/games" % id)

@app.route("/matches/<int:id>/games", methods = ["GET"])
def matches_games(id):
	match = MatchService().selectById(id)
	return render_template("matches/games.html", match = match)

@app.route("/matches/<int:id>/games", methods = ["POST"])
def matches_games_update(id):
	MatchService().updateGames(id, request.form["games"])
	return redirect("/matches/%d/players" % id)

@app.route("/matches/<int:id>/players", methods = ["GET"])
def matches_players(id):
	match = MatchService().selectById(id)
	title, template, default = MatchService().getMatchTypeAttributes(match)
	players = PlayerService().select()
	return render_template(template, title = title, match = match, players = players)

@app.route("/matches/<int:id>", methods = ["POST"])
def matches_play(id):
	MatchService().createTeams(id, request.form)
	return Response(json.dumps(request.form), status = 200, mimetype = "application/json")

@app.route("/players", methods = ["GET"])
def players():
	return render_template("players/index.html", players = PlayerService().select())

@app.route("/players/new", methods = ["GET"])
def players_new():
	return render_template("players/new.html")

@app.route("/players", methods = ["POST"])
def players_create():
	name = request.form["name"]

	players = session.query(PlayerModel).filter_by(name = name)
	if players.count() > 0:
		return render_template("players/new.html", name = name, error = True)

	PlayerService().create(name)

	return redirect("/players")

@app.route("/players/<int:id>/edit", methods = ["GET"])
def players_edit(id):
	player = session.query(PlayerModel).filter(PlayerModel.id == id).one()
	return render_template("players/edit.html", player = player)

@app.route("/players/<int:id>", methods = ["POST"])
def players_update(id):
	name = request.form["name"]
	player = PlayerService().selectById(id)
	player.name = name

	players = session.query(PlayerModel).filter(PlayerModel.id != id, PlayerModel.name == name)
	if players.count() > 0:
		return render_template("players/edit.html", player = player, error = True)

	PlayerService().update(id, name)

	return redirect("/players")

@app.route("/leaderboard", methods = ["GET"])
def leaderboard_index():
	return render_template("leaderboard/index.html")

# FOR TESTING
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
# FOR TESTING


@app.after_request
def afterRequest(response):
	session.close()
	return response

@app.errorhandler(404)
def not_found(error):
	return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error(error):
	return render_template("errors/500.html"), 500

class MatchService():

	def selectById(self, id):
		return session.query(MatchModel).filter(MatchModel.id == id).one()

	def select(self):
		return session.query(MatchModel)

	def create(self, matchType):
		match = MatchModel(matchType, False, False, datetime.now(), datetime.now())
		session.add(match)
		session.commit()

		return match

	def updatePlayTo(self, id, playTo):
		match = self.selectById(id)
		match.playTo = playTo
		match.updatedAt = datetime.now()
		session.commit()

		return match

	def updateGames(self, id, games):
		match = self.selectById(id)
		match.games = games
		match.updatedAt = datetime.now()
		session.commit()

		return match

	def createTeams(self, id, data):
		match = self.selectById(id)

		if match.matchType == "singles":
			team1 = TeamService().createOnePlayer(match.id, data["yellow"])
			team2 = TeamService().createOnePlayer(match.id, data["green"])

		elif match.matchType == "doubles":
			team1 = TeamService().createTwoPlayer(match.id, data["yellow"], data["blue"])
			team2 = TeamService().createTwoPlayer(match.id, data["green"], data["red"])

		elif match.matchType == "nines":
			team1 = TeamService().createOnePlayer(match.id, data["yellow"])
			team2 = TeamService().createOnePlayer(match.id, data["green"])
			team3 = TeamService().createOnePlayer(match.id, data["blue"])
			team4 = TeamService().createOnePlayer(match.id, data["red"])

	def getMatchTypeAttributes(self, match):
		if match.matchType == "singles":
			return "Singles", "matches/two-player.html", 21

		if match.matchType == "nines":
			return "9s", "matches/four-player.html", 9

		if match.matchType == "doubles":
			return "Doubles", "matches/four-player.html", 21

class TeamService():

	def create(self, matchId):
		team = TeamModel(matchId, datetime.now(), datetime.now())
		session.add(team)
		session.commit()
		return team

	def createOnePlayer(self, matchId, playerId):
		team = self.create(matchId)
		teamPlayer = TeamPlayerService().create(team.id, playerId)
		return team

	def createTwoPlayer(self, matchId, player1Id, player2Id):
		team = self.create(matchId)
		teamPlayer1 = TeamPlayerService().create(team.id, player1Id)
		teamPlayer2 = TeamPlayerService().create(team.id, player2Id)

		return team

class TeamPlayerService():

	def create(self, teamId, playerId):
		teamPlayer = TeamPlayerModel(teamId, playerId)
		session.add(teamPlayer)
		session.commit()

		return teamPlayer

class PlayerService():

	def select(self):
		return session.query(PlayerModel).order_by(PlayerModel.name)

	def selectById(self, id):
		return session.query(PlayerModel).filter(PlayerModel.id == id).one()

	def create(self, name):
		player = PlayerModel(name, datetime.now(), datetime.now())
		session.add(player)
		session.commit()

		return player

	def update(self, id, name):
		player = self.selectById(id)
		player.name = name
		player.updatedAt = datetime.now()
		session.commit()

		return player

class MatchModel(Base):

	__tablename__ = "matches"

	id = Column(Integer, primary_key = True)
	matchType = Column(String)
	playTo = Column(Integer)
	games = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)
	completedAt = Column(DateTime)

	teams = relationship("TeamModel", back_populates = "match")

	def __init__(self, matchType, ready, complete, createdAt, modifiedAt):
		self.matchType = matchType
		self.ready = ready
		self.complete = complete
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

class TeamModel(Base):

	__tablename__ = "teams"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	win = Column(Integer)
	loss = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	match = relationship("MatchModel")
	teamPlayers = relationship("TeamPlayerModel", back_populates = "team")

	def __init__(self, matchId, createdAt, modifiedAt):
		self.matchId = matchId
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class TeamPlayerModel(Base):

	__tablename__ = "teams_players"

	id = Column(Integer, primary_key = True)
	teamId = Column(Integer, ForeignKey("teams.id"))
	playerId = Column(Integer, ForeignKey("players.id"))

	team = relationship("TeamModel")
	player = relationship("PlayerModel")

	def __init__(self, teamId, playerId):
		self.teamId = teamId
		self.playerId = playerId


if __name__ == "__main__":
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
