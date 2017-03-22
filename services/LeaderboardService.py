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
		points = self.points()

		stats = []

		for player in players:
			stats.append({
				"playerId": player.id,
				"playerName": player.name,
				"matches": matches[player.id]["matches"] if player.id in matches else 0,
				"percentage": float(matches[player.id]["wins"]) / float(matches[player.id]["matches"]) * 100 if player.id in matches else 0,
				"points": points[player.id] if player.id in points else 0,
				"wins": matches[player.id]["wins"] if player.id in matches else 0,
				"losses": matches[player.id]["losses"] if player.id in matches else 0,
				"time": self.formatTime(times[player.id]) if player.id in times else 0,
			})

		return stats

	def matches(self):
		query = "\
			SELECT p.id AS playerId, COUNT(*) AS matches, SUM(t.win = 1) AS wins, SUM(t.loss = 1) AS losses\
			FROM players p\
			LEFT JOIN teams_players tp ON p.id = tp.playerId\
			LEFT JOIN teams t ON tp.teamId = t.id\
			LEFT JOIN matches m ON t.matchId = m.id\
			WHERE m.complete = 1\
			GROUP BY p.id\
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
			SELECT DISTINCT p.id as playerId, UNIX_TIMESTAMP(m.createdAt) as gameTime, UNIX_TIMESTAMP(m.completedAt) as resultTime\
			FROM players p\
			LEFT JOIN teams_players tp ON p.id = tp.playerId\
			LEFT JOIN teams t ON tp.teamId = t.id\
			LEFT JOIN matches m ON t.matchId = m.id\
			WHERE m.complete = 1\
		"

		connection = self.session.connection()
		times = connection.execute(text(query))

		data = {}

		for time in times:
			if time.playerId not in data:
				data[time.playerId] = 0

			data[time.playerId] = data[time.playerId] + time.resultTime - time.gameTime

		return data

	def points(self):
		query = "\
			SELECT p.id AS playerId, COUNT(s.id) as points\
			FROM players p\
			LEFT JOIN teams_players tp ON p.id = tp.playerId\
			LEFT JOIN teams t ON tp.teamId = t.id\
			LEFT JOIN matches m ON t.matchId = m.id\
			LEFT JOIN scores s ON t.id = s.teamId AND m.id = s.matchId\
			WHERE m.complete = 1\
			GROUP BY p.id\
		"

		connection = self.session.connection()
		points = connection.execute(text(query))

		data = {}

		for point in points:
			data[point.playerId] = point.points

		return data

	def formatTime(self, seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return "%02d:%02d:%02d" % (h, m, s)
