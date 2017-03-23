import Service, logging, json
from datetime import datetime
from sqlalchemy import text
from models import PlayerModel
from sqlalchemy import text
from flask import current_app as app

class LeaderboardService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, None)

	def stats(self):
		app.logger.info("Querying Leaderboard Statistics")

		players = self.session.query(PlayerModel.PlayerModel).order_by(PlayerModel.PlayerModel.name)

		matches = self.matches()
		times = self.times()
		pointsFor = self.pointsFor()
		pointsAgainst = self.pointsAgainst(pointsFor)

		stats = []

		for player in players:
			stats.append({
				"playerId": player.id,
				"playerName": player.name,
				"matches": matches[player.id]["matches"] if player.id in matches else 0,
				"percentage": float(matches[player.id]["wins"]) / float(matches[player.id]["matches"]) * 100 if player.id in matches else 0,
				"pointsFor": pointsFor[player.id] if player.id in pointsFor else 0,
				"pointsAgainst": pointsAgainst[player.id] if player.id in pointsAgainst else 0,
				"wins": matches[player.id]["wins"] if player.id in matches else 0,
				"losses": matches[player.id]["losses"] if player.id in matches else 0,
				"seconds": times[player.id] if player.id in matches else 0,
				"time": self.formatTime(times[player.id]) if player.id in times else 0
			})

		return stats

	def matches(self):
		query = "\
			SELECT players.id AS playerId, COUNT(*) AS matches, SUM(teams.win = 1) AS wins, SUM(teams.loss = 1) AS losses\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
			GROUP BY players.id\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query))

		data = {}

		for match in matches:
			data[int(match.playerId)] = {
				"matches": int(match.matches),
				"wins": int(match.wins),
				"losses": int(match.losses)
			}

		return data

	def times(self):
		query = "\
			SELECT DISTINCT players.id as playerId, UNIX_TIMESTAMP(matches.createdAt) as gameTime, UNIX_TIMESTAMP(matches.completedAt) as resultTime\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
		"
		connection = self.session.connection()
		times = connection.execute(text(query))

		data = {}

		for time in times:
			if time.playerId not in data:
				data[time.playerId] = 0

			data[time.playerId] = data[time.playerId] + time.resultTime - time.gameTime

		return data

	def pointsFor(self):
		query = "\
			SELECT players.id AS playerId, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE matches.complete = 1\
			GROUP BY players.id\
		"

		connection = self.session.connection()
		points = connection.execute(text(query))

		data = {}

		for point in points:
			data[point.playerId] = point.points

		return data

	def pointsAgainst(self, pointsFor):
		query = "\
			SELECT players.id as playerId, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
			GROUP BY players.id\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query))

		data = {}

		for match in matches:
			matchIds = map(int, match.matchIds.split(","))
			matchIds.append(0)

			query = "\
				SELECT COUNT(*) as points\
				FROM scores\
				WHERE matchId IN :matchIds\
			"
			connection = self.session.connection()
			points = connection.execute(text(query), matchIds = matchIds).first()

			data[match.playerId] = points.points - pointsFor[match.playerId]

		return data

	def formatTime(self, seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return "%02d:%02d:%02d" % (h, m, s)
