import Service, logging, json
from datetime import datetime
from sqlalchemy import text
from models import PlayerModel
from sqlalchemy import text
from flask import current_app as app

class LeaderboardService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, None)

	def matchTypeStats(self, matchType):
		app.logger.info("Querying Leaderboard Statistics")

		players = self.session.query(PlayerModel.PlayerModel).order_by(PlayerModel.PlayerModel.name)

		matches = self.matchesByMatchType(matchType)
		times = self.times(matchType)
		pointsFor = self.pointsForByMatchType(matchType)
		pointsAgainst = self.pointsAgainstByMatchType(pointsFor, matchType)

		stats = {
			"labels": self.labels(),
			"matchType": matchType,
			"rows": [],
			"totals": {}
		}

		for player in players:
			stats["rows"].append({
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

		stats["totals"] = self.totals(stats["rows"])

		return stats

	def playerStats(self, player):

		matches = self.matchesByPlayer(player.id)
		pointsFor = self.pointsForByPlayer(player.id)
		pointsAgainst = self.pointsAgainstByPlayer(pointsFor, player.id)

		stats = {
			"playerId": player.id,
			"playerName": player.name,
			"singles": {},
			"doubles": {},
			"nines": {}
		}

		stats["singles"] = matches["singles"]
		stats["doubles"] = matches["doubles"]
		stats["nines"] = matches["nines"]

		stats["singles"]["pointsFor"] = pointsFor["singles"]
		stats["doubles"]["pointsFor"] = pointsFor["doubles"]
		stats["nines"]["pointsFor"] = pointsFor["nines"]

		stats["singles"]["pointsAgainst"] = pointsAgainst["singles"]
		stats["doubles"]["pointsAgainst"] = pointsAgainst["doubles"]
		stats["nines"]["pointsAgainst"] = pointsAgainst["nines"]

		return stats

	def labels(self):
		return [{
			"sort": "string",
			"name": "Player"
		}, {
			"sort": "int",
			"name": "Matches"
		}, {
			"sort": "float",
			"name": "Win %"
		}, {
			"sort": "int",
			"name": "Points For"
		}, {
			"sort": "int",
			"name": "Points Against"
		}, {
			"sort": "int",
			"name": "Wins"
		}, {
			"sort": "int",
			"name": "Losses"
		}]

	def matchesByMatchType(self, matchType):
		query = "\
			SELECT players.id AS playerId, COUNT(*) AS matches, SUM(teams.win = 1) AS wins, SUM(teams.win = 0) AS losses\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND matches.matchType = :matchType\
			GROUP BY players.id\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query), matchType = matchType)

		data = {}

		for match in matches:
			data[int(match.playerId)] = {
				"matches": int(match.matches),
				"wins": int(match.wins),
				"losses": int(match.losses)
			}

		return data

	def matchesByPlayer(self, playerId):
		query = "\
			SELECT players.id AS playerId, matches.matchType, COUNT(*) AS matches, SUM(teams.win = 1) AS wins, SUM(teams.win = 0) AS losses\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND players.id = :playerId\
			GROUP BY matches.matchType\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query), playerId = playerId)

		data = {}

		for match in matches:
			data[match.matchType] = {
				"matches": int(match.matches),
				"wins": int(match.wins),
				"losses": int(match.losses),
				"percentage": float(match.wins) / float(match.matches) * 100
			}

		return data

	def times(self, matchType):
		query = "\
			SELECT DISTINCT players.id as playerId, UNIX_TIMESTAMP(matches.createdAt) as gameTime, UNIX_TIMESTAMP(matches.completedAt) as resultTime\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND matches.matchType = :matchType\
		"
		connection = self.session.connection()
		times = connection.execute(text(query), matchType = matchType)

		data = {}

		for time in times:
			if time.playerId not in data:
				data[time.playerId] = 0

			data[time.playerId] = data[time.playerId] + time.resultTime - time.gameTime

		return data

	def pointsForByMatchType(self, matchType):
		query = "\
			SELECT players.id AS playerId, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE matches.complete = 1 AND matches.matchType = :matchType\
			GROUP BY players.id\
		"

		connection = self.session.connection()
		points = connection.execute(text(query), matchType = matchType)

		data = {}

		for point in points:
			data[point.playerId] = point.points

		return data

	def pointsForByPlayer(self, playerId):
		query = "\
			SELECT players.id AS playerId, matches.matchType, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE matches.complete = 1 AND players.id = :playerId\
			GROUP BY players.id, matches.matchType\
		"

		connection = self.session.connection()
		points = connection.execute(text(query), playerId = playerId)

		data = {}

		for point in points:
			data[point.matchType] = point.points

		return data

	def pointsAgainstByMatchType(self, pointsFor, matchType):
		query = "\
			SELECT players.id as playerId, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND matches.matchType = :matchType\
			GROUP BY players.id\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query), matchType = matchType)

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

	def pointsAgainstByPlayer(self, pointsFor, playerId):
		query = "\
			SELECT players.id as playerId, matches.matchType, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND players.id = :playerId\
			GROUP BY matches.matchType\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query), playerId = playerId)

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

			data[match.matchType] = points.points - pointsFor[match.matchType]

		return data

	def totals(self, rows):
		totals = {
			"matches": 0,
			"pointsFor": 0,
			"pointsAgainst": 0,
			"seconds": 0,
			"wins": 0,
			"losses": 0
		}

		for row in rows:
			totals["matches"] += row["matches"]
			totals["pointsFor"] += row["pointsFor"]
			totals["pointsAgainst"] += row["pointsAgainst"]
			totals["seconds"] += row["seconds"]
			totals["wins"] += row["wins"]
			totals["losses"] += row["losses"]

		totals["time"] = self.formatTime(totals["seconds"])

		return totals

	def formatTime(self, seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return "%02d:%02d:%02d" % (h, m, s)
