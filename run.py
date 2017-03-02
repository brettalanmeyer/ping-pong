from flask import Flask, render_template, Response, redirect, request
from flask.ext.assets import Environment, Bundle
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, text, func, Column, Integer, DateTime, String, ForeignKey
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

@app.route("/matches/delete", methods = ["POST"])
def matches_delete():
	MatchService().deleteAll()
	return redirect("/")

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

	return redirect("/matches/%d/num-of-games" % id)

@app.route("/matches/<int:id>/num-of-games", methods = ["GET"])
def matches_games(id):
	match = MatchService().selectById(id)
	return render_template("matches/num-of-games.html", match = match)

@app.route("/matches/<int:id>/num-of-games", methods = ["POST"])
def matches_games_update(id):
	MatchService().updateGames(id, request.form["numOfGames"])
	return redirect("/matches/%d/players" % id)

@app.route("/matches/<int:id>/players", methods = ["GET"])
def matches_players(id):
	match = MatchService().selectById(id)
	title, template, default = MatchService().getMatchTypeAttributes(match)
	players = PlayerService().select()
	return render_template(template, title = title, match = match, players = players)

@app.route("/matches/<int:id>/players", methods = ["POST"])
def matches_players_create(id):
	MatchService().createTeams(id, request.form)
	MatchService().play(id)
	return redirect("/matches/%d" % id)

@app.route("/matches/<int:id>", methods = ["GET"])
def matches(id):
	data = MatchService().matchData(id)
	return render_template(data["template"], data = data)

@app.route("/matches/<int:id>.json", methods = ["GET"])
def matches_json(id):
	data = MatchService().matchData(id)
	return Response(json.dumps(data), status = 200, mimetype = "application/json")

@app.route("/players", methods = ["GET"])
def players():
	return render_template("players/index.html", players = PlayerService().select())

@app.route("/players/new", methods = ["GET"])
def players_new():
	player = PlayerService().new()
	return render_template("players/new.html", player = player)

@app.route("/players", methods = ["POST"])
def players_create():
	name = request.form["name"]

	players = session.query(PlayerModel).filter_by(name = name)
	if players.count() > 0:
		player = PlayerService().new()
		player.name = name
		return render_template("players/new.html", player = player, error = True)

	PlayerService().create(request.form)

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

	players = PlayerService().excludeByName(id, name)
	if players.count() > 0:
		return render_template("players/edit.html", player = player, error = True)

	PlayerService().update(id, name)

	return redirect("/players")

@app.route("/isms", methods = ["GET"])
def isms():
	return render_template("isms/index.html", isms = IsmService().select())

@app.route("/isms/new", methods = ["GET"])
def isms_new():
	ism = IsmService().new()
	return render_template("isms/new.html", ism = ism)

@app.route("/isms", methods = ["POST"])
def isms_create():
	IsmService().create(request.form)
	return redirect("/isms")

@app.route("/isms/<int:id>/edit", methods = ["GET"])
def isms_edit(id):
	ism = IsmService().selectById(id)
	return render_template("isms/edit.html", ism = ism)

@app.route("/isms/<int:id>", methods = ["POST"])
def isms_update(id):
	IsmService().update(id, request.form)
	return redirect("/isms")

@app.route("/isms/<int:id>/delete", methods = ["POST"])
def isms_delete(id):
	IsmService().delete(id)
	return redirect("/isms")

@app.route("/leaderboard", methods = ["GET"])
def leaderboard_index():
	return render_template("leaderboard/index.html")

@app.route("/buttons", methods = ["GET"])
def buttons():
	return render_template("buttons.html")

@app.route("/buttons/<path:button>/score", methods = ["POST"])
def buttons_score(button):
	MatchService().score(button)
	return button

@app.route("/buttons/<path:button>/undo", methods = ["POST"])
def buttons_undo(button):
	MatchService().undo(button)
	return button

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

	def selectActiveMatch(self):
		return session.query(MatchModel).filter(MatchModel.ready == True, MatchModel.complete == False).order_by(MatchModel.id.desc()).first()

	def create(self, matchType):
		match = MatchModel(matchType, False, False, datetime.now(), datetime.now())
		session.add(match)
		session.commit()

		return match

	def updatePlayTo(self, id, playTo):
		match = self.selectById(id)
		match.playTo = playTo
		match.modifiedAt = datetime.now()
		session.commit()

		return match

	def updateGames(self, id, numOfGames):
		match = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		session.commit()

		return match

	def createTeams(self, id, data):
		match = self.selectById(id)

		if Singles().isMatchType(match.matchType):
			Singles().createTeams(match, data)

		elif Doubles().isMatchType(match.matchType):
			Doubles().createTeams(match, data)

		elif Nines().isMatchType(match.matchType):
			pass

	def getMatchTypeAttributes(self, match):
		if Singles().isMatchType(match.matchType):
			return "Singles", "matches/two-player.html", 21

		if Doubles().isMatchType(match.matchType):
			return "9s", "matches/four-player.html", 9

		if Nines().isMatchType(match.matchType):
			return "Doubles", "matches/four-player.html", 21

	def matchData(self, id):

		match = self.selectById(id)

		if Singles().isMatchType(match.matchType):
			return Singles().matchData(match)

		elif Doubles().isMatchType(match.matchType):
			return Doubles().matchData(match)

		elif Nines().isMatchType(match.matchType):
			pass

	def score(self, button):
		match = self.selectActiveMatch()

		if Singles().isMatchType(match.matchType):
			Singles().score(match, button)

		elif Doubles().isMatchType(match.matchType):
			pass

		elif Nines().isMatchType(match.matchType):
			pass

	def undo(self, button):
		match = self.selectActiveMatch()

		if Singles().isMatchType(match.matchType):
			return Singles().undo(match, button)

		elif Doubles().isMatchType(match.matchType):
			pass

		elif Nines().isMatchType(match.matchType):
			pass

	def play(self, id):
		match = self.selectById(id)
		match.ready = True
		match.modifiedAt = datetime.now()
		session.commit()

	def deleteAll(self):
		session.query(MatchModel).delete()
		session.commit()

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

	def new(self):
		return PlayerModel("", None, None)

	def create(self, form):
		player = PlayerModel(form["name"], datetime.now(), datetime.now())
		session.add(player)
		session.commit()

		return player

	def update(self, id, name):
		player = self.selectById(id)
		player.name = name
		player.modifiedAt = datetime.now()
		session.commit()

		return player

	def excludeByName(self, id, name):
		return session.query(PlayerModel).filter(PlayerModel.id != id, PlayerModel.name == name)

class ScoreService():

	def score(self, matchId, teamId, game):
		score = ScoreModel(matchId, teamId, game, datetime.now())
		session.add(score)
		session.commit()

	def undo(self, matchId):
		score = session.query(ScoreModel).filter(MatchModel.id == matchId).order_by(ScoreModel.id.desc()).first()
		if score != None:
			session.query(ScoreModel).filter(ScoreModel.id == score.id).delete()
			session.commit()

	def getScore(self, matchId, teamId, game):
		query = "\
			SELECT COUNT(*) as points\
			FROM scores\
			WHERE matchId = :matchId AND teamId = :teamId AND game = :game\
			GROUP BY matchId, teamId, game\
		"
		connection = session.connection()
		data = connection.execute(text(query), matchId = matchId, teamId = teamId, game = game).first()

		if data == None:
			return 0

		return int(data.points)

class GameService():

	def create(self, matchId, game, green, yellow, blue, red):
		game = GameModel(matchId, game, green, yellow, blue, red, datetime.now())
		session.add(game)
		session.commit()

		return game

class IsmService():

	def select(self):
		return session.query(IsmModel).filter(IsmModel.approved == True)

	def selectById(self, id):
		return session.query(IsmModel).filter(IsmModel.id == id).one()

	def new(self):
		return IsmModel(0, 0, "", False, None, None)

	def create(self, form):
		ism = IsmModel(form["left"], form["right"], form["saying"], False, datetime.now(), datetime.now())
		session.add(ism)
		session.commit()

		return ism

	def update(self, id, form):
		ism = self.selectById(id)
		ism.left = form["left"]
		ism.right = form["right"]
		ism.saying = form["saying"]
		ism.approved = False
		ism.modifiedAt = datetime.now()
		session.commit()

		return ism

	def delete(self, id):
		ism = self.selectById(id)
		session.delete(ism)
		session.commit()

		return ism

class MatchModel(Base):

	__tablename__ = "matches"

	id = Column(Integer, primary_key = True)
	matchType = Column(String)
	playTo = Column(Integer)
	numOfGames = Column(Integer)
	game = Column(Integer)
	ready = Column(Integer)
	complete = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)
	completedAt = Column(DateTime)

	teams = relationship("TeamModel", back_populates = "match")
	games = relationship("GameModel", back_populates = "match")

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

class ScoreModel(Base):

	__tablename__ = "scores"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	teamId = Column(Integer, ForeignKey("teams.id"))
	game = Column(Integer)
	createdAt = Column(DateTime)

	def __init__(self, matchId, teamId, game, createdAt):
		self.matchId = matchId
		self.teamId = teamId
		self.game = game
		self.createdAt = createdAt

class GameModel(Base):

	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	matchId = Column(Integer, ForeignKey("matches.id"))
	game = Column(Integer)
	green = Column(Integer, ForeignKey("players.id"))
	yellow = Column(Integer, ForeignKey("players.id"))
	blue = Column(Integer, ForeignKey("players.id"))
	red = Column(Integer, ForeignKey("players.id"))
	winner = Column(Integer, ForeignKey("teams.id"))
	winnerScore = Column(Integer)
	loser = Column(Integer, ForeignKey("teams.id"))
	loserScore = Column(Integer)
	createdAt = Column(DateTime)
	completedAt = Column(DateTime)

	match = relationship("MatchModel")

	def __init__(self, matchId, game, green, yellow, blue, red, createdAt):
		self.matchId = matchId
		self.game = game
		self.green = green
		self.yellow = yellow
		self.blue = blue
		self.red = red
		self.createdAt = createdAt

class IsmModel(Base):

	__tablename__ = "isms"

	id = Column(Integer, primary_key = True)
	left = Column(Integer)
	right = Column(Integer)
	saying = Column(String)
	approved = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, left, right, saying, approved, createdAt, modifiedAt):
		self.left = left
		self.right = right
		self.saying = saying
		self.approved = approved
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class Singles():

	label = "Singles"
	matchType = "singles"
	template = "matches/singles.html"

	def isMatchType(self, matchType):
		return self.matchType == matchType

	def matchData(self, match):
		game = match.games[match.game - 1]

		data = {
			"matchId": match.id,
			"matchType": "singles",
			"playTo": match.playTo,
			"numOfGames": match.numOfGames,
			"games": [],
			"game": match.game,
			"template": self.template,
			"complete": False,
			"teams": {
				"green": {
					"teamId": None,
					"playerId": game.green,
					"playerName": None,
					"points": None,
					"serving": False
				},
				"yellow": {
					"teamId": None,
					"playerId": game.yellow,
					"playerName": None,
					"points": None,
					"serving": False
				}
			},
			"points": 0
		}

		for team in match.teams:
			for teamPlayer in team.teamPlayers:
				color = "green"

				if data["teams"]["yellow"]["playerId"] == teamPlayer.player.id:
					color = "yellow"

				data["teams"][color]["playerName"] = teamPlayer.player.name
				data["teams"][color]["points"] = ScoreService().getScore(match.id, team.id, match.game)
				data["teams"][color]["teamId"] = team.id

				data["games"].append({
					"teamId": team.id,
					"name": teamPlayer.player.name,
					"games": []
				})

		for color in data["teams"]:
			data["points"] += data["teams"][color]["points"]


		for game in match.games:
			for team in data["games"]:
				if game.winner == team["teamId"]:
					team["games"].append({
						"win": True,
						"score": game.winnerScore
					})
				elif game.loser == team["teamId"]:
					team["games"].append({
						"win": False,
						"score": game.loserScore
					})

		self.determineServe(data)

		return data

	def determineServe(self, data):

		if data["points"] % 10 < 5:
			data["teams"]["green"]["serving"] = True
		else:
			data["teams"]["yellow"]["serving"] = True

	def score(self, match, button):
		data = self.matchData(match)

		if button == "green" or button == "red":
			ScoreService().score(match.id, data["teams"]["green"]["teamId"], match.game)

		elif button == "yellow" or button == "blue":
			ScoreService().score(match.id, data["teams"]["yellow"]["teamId"], match.game)

	def undo(self, match, button):
		ScoreService().undo(match.id)

	def createTeams(self, match, data):
		team1 = TeamService().createOnePlayer(match.id, data["green"])
		team2 = TeamService().createOnePlayer(match.id, data["yellow"])

		for i in range(1, match.numOfGames + 1):

			if i % 2 == 1:
				green = data["green"]
				yellow = data["yellow"]
			else:
				green = data["yellow"]
				yellow = data["green"]

			GameService().create(match.id, i, green, yellow, None, None)

class Doubles():

	label = "Doubles"
	matchType = "doubles"
	template = "matches/doubles.html"

	def isMatchType(self, matchType):
		return self.matchType == matchType

	def matchData(self, match):
		game = match.games[match.game - 1]

		data = {
			"matchId": match.id,
			"matchType": "doubles",
			"playTo": match.playTo,
			"numOfGames": match.numOfGames,
			"games": [],
			"game": match.game,
			"template": self.template,
			"complete": False,
			"teams": [],
			"players": {
				"green": {
					"teamId": None,
					"playerId": game.green,
					"playerName": None,
					"serving": False
				},
				"yellow": {
					"teamId": None,
					"playerId": game.yellow,
					"playerName": None,
					"serving": False
				},
				"blue": {
					"teamId": None,
					"playerId": game.blue,
					"playerName": None,
					"serving": False
				},
				"red": {
					"teamId": None,
					"playerId": game.red,
					"playerName": None,
					"serving": False
				}
			},
			"points": 0
		}

		for team in match.teams:

			points = ScoreService().getScore(match.id, team.id, match.game)
			data["points"] += points

			data["teams"].append({
				"teamId": team.id,
				"points": points
			})

			for teamPlayer in team.teamPlayers:
				if data["players"]["green"]["playerId"] == teamPlayer.player.id:
					color = "green"
				elif data["players"]["yellow"]["playerId"] == teamPlayer.player.id:
					color = "yellow"
				elif data["players"]["blue"]["playerId"] == teamPlayer.player.id:
					color = "blue"
				elif data["players"]["red"]["playerId"] == teamPlayer.player.id:
					color = "red"

				data["players"][color]["playerName"] = teamPlayer.player.name
				data["players"][color]["teamId"] = team.id

		for game in match.games:
			data["games"].append({
				"winner": game.winner,
				"winnerScore": game.winnerScore,
				"loser": game.loser,
				"loserScore": game.loserScore
			})

		self.determineServe(data)

		return data

	def determineServe(self, data):

		if data["points"] % 10 < 5:
			data["players"]["green"]["serving"] = True
		else:
			data["players"]["yellow"]["serving"] = True

	def createTeams(self, match, data):
		green = data["green"]
		yellow = data["yellow"]
		blue = data["blue"]
		red = data["red"]

		team1 = TeamService().createTwoPlayer(match.id, green, red)
		team2 = TeamService().createTwoPlayer(match.id, yellow, blue)

		for i in range(0, match.numOfGames):

			# Game 1
			# B  A
			# C  D
			if i % 4 == 0:
				a = green
				b = yellow
				c = blue
				d = red

			# Game 2
			# A  B
			# D  C
			elif i % 4 == 1:
				a = yellow
				b = green
				c = red
				d = blue

			# Game 3
			# C  D
			# B  A
			elif i % 4 == 2:
				a = red
				b = blue
				c = yellow
				d = green

			# Game 4
			# D  C
			# A  B
			elif i % 4 == 3:
				a = blue
				b = red
				c = green
				d = yellow

			GameService().create(match.id, i + 1, a, b, c, d)

class Nines():

	label = "9s"
	matchType = "nines"
	template = "matches/nines.html"

	def isMatchType(self, matchType):
		return self.matchType == matchType


if __name__ == "__main__":
	socketio.run(app, host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
