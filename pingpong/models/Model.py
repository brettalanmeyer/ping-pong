from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PlayerModel(db.Model):

	__tablename__ = "players"

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	enabled = db.Column(db.Integer)
	createdAt = db.Column(db.DateTime)
	modifiedAt = db.Column(db.DateTime)

	def __init__(self, name, enabled, createdAt, modifiedAt):
		self.name = name
		self.enabled = enabled
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class IsmModel(db.Model):

	__tablename__ = "isms"

	id = db.Column(db.Integer, primary_key = True)
	left = db.Column(db.Integer)
	right = db.Column(db.Integer)
	saying = db.Column(db.String)
	approved = db.Column(db.Integer)
	createdAt = db.Column(db.DateTime)
	modifiedAt = db.Column(db.DateTime)

	def __init__(self, left, right, saying, approved, createdAt, modifiedAt):
		self.left = left
		self.right = right
		self.saying = saying
		self.approved = approved
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class MatchModel(db.Model):

	__tablename__ = "matches"

	id = db.Column(db.Integer, primary_key = True)
	matchType = db.Column(db.String)
	playTo = db.Column(db.Integer)
	numOfGames = db.Column(db.Integer)
	game = db.Column(db.Integer)
	ready = db.Column(db.Integer)
	complete = db.Column(db.Integer)
	createdAt = db.Column(db.DateTime)
	modifiedAt = db.Column(db.DateTime)
	completedAt = db.Column(db.DateTime)

	teams = db.relationship("TeamModel")
	games = db.relationship("GameModel")

	def __init__(self, matchType, playTo, game, ready, complete, createdAt, modifiedAt):
		self.matchType = matchType
		self.playTo = playTo
		self.game = game
		self.ready = ready
		self.complete = complete
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class GameModel(db.Model):

	__tablename__ = "games"

	id = db.Column(db.Integer, primary_key = True)
	matchId = db.Column(db.Integer, db.ForeignKey("matches.id"))
	game = db.Column(db.Integer)
	green = db.Column(db.Integer, db.ForeignKey("players.id"))
	yellow = db.Column(db.Integer, db.ForeignKey("players.id"))
	blue = db.Column(db.Integer, db.ForeignKey("players.id"))
	red = db.Column(db.Integer, db.ForeignKey("players.id"))
	winner = db.Column(db.Integer, db.ForeignKey("teams.id"))
	winnerScore = db.Column(db.Integer)
	loser = db.Column(db.Integer, db.ForeignKey("teams.id"))
	loserScore = db.Column(db.Integer)
	completedAt = db.Column(db.DateTime)
	createdAt = db.Column(db.DateTime)
	modifiedAt = db.Column(db.DateTime)

	match = db.relationship("MatchModel")

	def __init__(self, matchId, game, green, yellow, blue, red, createdAt, modifiedAt):
		self.matchId = matchId
		self.game = game
		self.green = green
		self.yellow = yellow
		self.blue = blue
		self.red = red
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt


class TeamModel(db.Model):

	__tablename__ = "teams"

	associationTable = db.Table("teams_players",
		db.Column("teamId", db.Integer, db.ForeignKey("teams.id"), primary_key = True),
		db.Column("playerId", db.Integer, db.ForeignKey("players.id"), primary_key = True)
	)

	id = db.Column(db.Integer, primary_key = True)
	matchId = db.Column(db.Integer, db.ForeignKey("matches.id"))
	win = db.Column(db.Integer)
	createdAt = db.Column(db.DateTime)
	modifiedAt = db.Column(db.DateTime)

	match = db.relationship("MatchModel")
	players = db.relationship("PlayerModel", secondary = associationTable)

	def __init__(self, matchId, createdAt, modifiedAt):
		self.matchId = matchId
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

class ScoreModel(db.Model):

	__tablename__ = "scores"

	id = db.Column(db.Integer, primary_key = True)
	matchId = db.Column(db.Integer)
	matchId = db.Column(db.Integer, db.ForeignKey("matches.id"))
	teamId = db.Column(db.Integer, db.ForeignKey("teams.id"))
	game = db.Column(db.Integer)
	createdAt = db.Column(db.DateTime)

	def __init__(self, matchId, teamId, game, createdAt):
		self.matchId = matchId
		self.teamId = teamId
		self.game = game
		self.createdAt = createdAt
