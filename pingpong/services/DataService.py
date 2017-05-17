from flask import current_app as app
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import scoped_session, sessionmaker
import urllib

class DataService():

	def isConfigured(self):
		if not util.hasConfig("MYSQL_REMOTE_USERNAME"):
			return False
		if not util.hasConfig("MYSQL_REMOTE_PASSWORD"):
			return False
		if not util.hasConfig("MYSQL_REMOTE_HOST"):
			return False
		if not util.hasConfig("MYSQL_REMOTE_DATABASE"):
			return False

		return True

	def db(self):
		username = app.config["MYSQL_REMOTE_USERNAME"]
		password = app.config["MYSQL_REMOTE_PASSWORD"]
		host = app.config["MYSQL_REMOTE_HOST"]
		database = app.config["MYSQL_REMOTE_DATABASE"]

		url = "mysql+mysqldb://{}:{}@{}/{}?use_unicode=1&charset=utf8".format(username, password, host, database)

		engine = create_engine(url, pool_recycle = 3600)
		return scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))

	def selectRemoteData(self, query):
		remoteSession = self.db()
		remoteConnection = remoteSession.connection()
		data = remoteConnection.execute(text(query))
		remoteSession.close()
		return data

	def copyPlayers(self):
		players = self.selectRemoteData("SELECT * FROM players")

		insertPlayer = "\
			INSERT INTO players\
			SET\
				`id` = :id,\
				`name` = :name,\
				`avatar` = :avatar,\
				`extension` = :extension,\
				`enabled` = :enabled,\
				`createdAt` = :createdAt,\
				`modifiedAt` = :modifiedAt;\
		"

		connection = db.session.connection()

		for player in players:
			connection.execute(
				text(insertPlayer),
				id = player.id,
				name = player.name,
				avatar = player.avatar,
				extension = player.extension,
				enabled = player.enabled,
				createdAt = player.createdAt,
				modifiedAt = player.modifiedAt
			)

			if player.avatar != None:
				urllib.urlretrieve ("http://10.9.0.230:5010/players/{}/avatar/{}".format(player.id, player.avatar), "{}/avatars/{}".format(app.root_path, player.avatar))

		db.session.commit()

	def copyIsms(self):
		isms = self.selectRemoteData("SELECT * FROM isms")

		insertIsm = "\
			INSERT INTO isms\
			SET\
				`id` = :id,\
				`left` = :left,\
				`right` = :right,\
				`saying` = :saying,\
				`approved` = :approved,\
				`createdAt` = :createdAt,\
				`modifiedAt` = :modifiedAt;\
		"

		connection = db.session.connection()

		for ism in isms:
			connection.execute(
				text(insertIsm),
				id = ism.id,
				left = ism.left,
				right = ism.right,
				saying = ism.saying,
				approved = ism.approved,
				createdAt = ism.createdAt,
				modifiedAt = ism.modifiedAt
			)

		db.session.commit()

	def copyMatches(self):
		matches = self.selectRemoteData("SELECT * FROM matches")

		insertMatch = "\
			INSERT INTO matches\
			SET\
				`id` = :id,\
				`matchType` = :matchType,\
				`playTo` = :playTo,\
				`numOfGames` = :numOfGames,\
				`game` = :game,\
				`ready` = :ready,\
				`complete` = :complete,\
				`createdAt` = :createdAt,\
				`modifiedAt` = :modifiedAt,\
				`completedAt` = :completedAt;\
		"

		connection = db.session.connection()

		for match in matches:
			connection.execute(
				text(insertMatch),
				id = match.id,
				matchType = match.matchType,
				playTo = match.playTo,
				numOfGames = match.numOfGames,
				game = match.game,
				ready = match.ready,
				complete = match.complete,
				createdAt = match.createdAt,
				modifiedAt = match.modifiedAt,
				completedAt = match.completedAt
			)

		db.session.commit()

	def copyTeams(self):
		teams = self.selectRemoteData("SELECT * FROM teams")

		insertTeam = "\
			INSERT INTO teams\
			SET\
				`id` = :id,\
				`matchId` = :matchId,\
				`win` = :win,\
				`createdAt` = :createdAt,\
				`modifiedAt` = :modifiedAt;\
		"

		connection = db.session.connection()

		for team in teams:
			connection.execute(
				text(insertTeam),
				id = team.id,
				matchId = team.matchId,
				win = team.win,
				createdAt = team.createdAt,
				modifiedAt = team.modifiedAt
			)

		db.session.commit()

	def copyTeamsPlayers(self):
		teamPlayers = self.selectRemoteData("SELECT * FROM teams_players")

		insertTeamPlayer = "\
			INSERT INTO teams_players\
			SET\
				`teamId` = :teamId,\
				`playerId` = :playerId;\
		"

		connection = db.session.connection()

		for teamPlayer in teamPlayers:
			connection.execute(
				text(insertTeamPlayer),
				teamId = teamPlayer.teamId,
				playerId = teamPlayer.playerId
			)

		db.session.commit()

	def copyGames(self):
		games = self.selectRemoteData("SELECT * FROM games")

		insertGame = "\
			INSERT INTO games\
			SET\
				`id` = :id,\
				`matchId` = :matchId,\
				`game` = :game,\
				`greenId` = :greenId,\
				`yellowId` = :yellowId,\
				`blueId` = :blueId,\
				`redId` = :redId,\
				`winner` = :winner,\
				`winnerScore` = :winnerScore,\
				`loser` = :loser,\
				`loserScore` = :loserScore,\
				`createdAt` = :createdAt,\
				`modifiedAt` = :modifiedAt,\
				`completedAt` = :completedAt;\
		"

		connection = db.session.connection()

		for game in games:
			connection.execute(
				text(insertGame),
				id = game.id,
				matchId = game.matchId,
				game = game.game,
				greenId = game.greenId,
				yellowId = game.yellowId,
				blueId = game.blueId,
				redId = game.redId,
				winner = game.winner,
				winnerScore = game.winnerScore,
				loser = game.loser,
				loserScore = game.loserScore,
				createdAt = game.createdAt,
				modifiedAt = game.modifiedAt,
				completedAt = game.completedAt
			)

		db.session.commit()

	def copyScores(self):
		scores = self.selectRemoteData("SELECT * FROM scores")

		insertTeam = "\
			INSERT INTO scores\
			SET\
				`id` = :id,\
				`matchId` = :matchId,\
				`teamId` = :teamId,\
				`game` = :game,\
				`createdAt` = :createdAt;\
		"

		connection = db.session.connection()

		for score in scores:
			connection.execute(
				text(insertTeam),
				id = score.id,
				matchId = score.matchId,
				teamId = score.teamId,
				game = score.game,
				createdAt = score.createdAt
			)

		db.session.commit()
