from Service import Service
from datetime import datetime
from sqlalchemy import text
from models.PlayerModel import PlayerModel
from sqlalchemy import text
from flask import current_app as app

class LeaderboardService(Service):

	def __init__(self, session):
		Service.__init__(self, session)

	def matchTypeStats(self, matchType):
		app.logger.info("Querying Leaderboard Statistics")

		players = self.session.query(PlayerModel).order_by(PlayerModel.name)

		matches = self.matchesByMatchType(matchType)
		times = self.times(matchType)
		pointsFor = self.pointsForByMatchType(matchType)
		pointsAgainst = self.pointsAgainstByMatchType(pointsFor, matchType)
		pointStreakData = self.selectMatchScoresByMatchType(matchType)
		winStreakData = self.selectTeamResultsByMatchType(matchType)

		stats = {
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
				"time": self.formatTime(times[player.id]) if player.id in times else 0,
				"pointStreak": self.pointStreakByPlayer(pointStreakData, player.id),
				"winStreak": self.winStreakByPlayer(winStreakData, player.id)
			})

		stats["totals"] = self.totals(stats["rows"])

		return stats

	def playerStats(self, player):

		matches = self.matchesByPlayer(player.id)
		pointsFor = self.pointsForByPlayer(player.id)
		pointsAgainst = self.pointsAgainstByPlayer(pointsFor, player.id)
		winStreakData = self.selectTeamResultsByPlayer(player.id)

		stats = {
			"playerId": player.id,
			"playerName": player.name
		}

		for matchType in self.matchTypes:
			stats[matchType] = {
				"matches": 0,
				"wins": 0,
				"losses": 0,
				"percentage": 0,
				"pointsFor": 0,
				"pointsAgainst": 0,
				"matchups": [],
				"winStreak": self.winStreakByMatchType(winStreakData, matchType)
			}

			if matchType in matches:
				stats[matchType]["matches"] = matches[matchType]["matches"]
				stats[matchType]["wins"] = matches[matchType]["wins"]
				stats[matchType]["losses"] = matches[matchType]["losses"]
				stats[matchType]["percentage"] = matches[matchType]["percentage"]

			if matchType in pointsFor:
				stats[matchType]["pointsFor"] = pointsFor[matchType]

			if matchType in pointsAgainst:
				stats[matchType]["pointsAgainst"] = pointsAgainst[matchType]

		results = self.matchups(player.id)

		for result in results:
			pointsFor = self.pointsForByOpponent(player.id, result.playerId)
			pointsAgainst = self.pointsAgainstByOpponent(pointsFor, player.id, result.playerId)
			winStreakData = self.selectTeamResultsByOpponent(player.id, result.playerId)

			# points and win/loss are inverted because these stats show the player vs this opponent
			stats[result.matchType]["matchups"].append({
				"playerId": result.playerId,
				"playerName": result.playerName,
				"numOfMatches": int(result.numOfMatches),
				"pointsFor": pointsAgainst[result.matchType],
				"pointsAgainst": pointsFor[result.matchType],
				"wins": int(result.losses),
				"losses": int(result.wins),
				"percentage": float(result.losses) / float(result.numOfMatches) * 100,
				"winStreak": winStreakData[result.matchType]
			})

		return stats

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
			GROUP BY matches.matchType\
		"

		connection = self.session.connection()
		points = connection.execute(text(query), playerId = playerId)

		data = {}

		for point in points:
			data[point.matchType] = point.points

		return data

	def pointsForByOpponent(self, playerId, opponentId):
		query = "\
			SELECT players.id AS playerId, matches.matchType, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE matches.complete = 1 AND players.id = :opponentId\
				AND matches.id IN (\
					SELECT matches.id AS matchIds\
					FROM matches\
					LEFT JOIN teams ON matches.id = teams.matchId\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE teams_players.playerId = :playerId\
						AND matches.complete = 1\
				)\
			GROUP BY matches.matchType\
		"

		connection = self.session.connection()
		points = connection.execute(text(query), playerId = playerId, opponentId = opponentId)

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

	def pointsAgainstByOpponent(self, pointsFor, playerId, opponentId):
		query = "\
			SELECT players.id as playerId, matches.matchType, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND players.id = :opponentId\
				AND matches.id IN (\
					SELECT matches.id AS matchIds\
					FROM matches\
					LEFT JOIN teams ON matches.id = teams.matchId\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE teams_players.playerId = :playerId\
						AND matches.complete = 1\
				)\
			GROUP BY matches.matchType\
		"
		connection = self.session.connection()
		matches = connection.execute(text(query), playerId = playerId, opponentId = opponentId)

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

	def selectTeamResultsByOpponent(self, playerId, opponentId):
		query = "\
			SELECT teams.id, teams.win, matches.matchType, GROUP_CONCAT(teams_players.playerId) AS playerIds\
			FROM teams\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND teams_players.playerId = :opponentId\
				AND matches.id IN (\
					SELECT matches.id AS matchIds\
					FROM matches\
					LEFT JOIN teams ON matches.id = teams.matchId\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE teams_players.playerId = :playerId\
						AND matches.complete = 1\
				)\
			GROUP BY teams.id\
			ORDER BY matches.matchType, teams.id DESC\
		"

		connection = self.session.connection()
		results = connection.execute(text(query), playerId = playerId, opponentId = opponentId)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"win": row.win,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		streaks = {}
		for matchType in self.matchTypes:
			streaks[matchType] = self.winStreakByMatchType(data, matchType)

			# invert due to opponent's streak
			if matchType != "nines":
				streaks[matchType] *= -1

		return streaks

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

	def matchups(self, playerId):
		query = "\
			SELECT\
				players.id as playerId,\
				players.name as playerName,\
				matches.matchType,\
				COUNT(players.id) AS numOfMatches,\
				SUM(teams.win = 1) AS wins,\
				SUM(teams.win = 0) AS losses\
			FROM matches\
			LEFT JOIN teams ON matches.id = teams.matchId\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN players ON teams_players.playerId = players.id\
			WHERE teams.id IN (\
					SELECT teams.id\
					FROM teams\
					LEFT JOIN matches ON teams.matchId = matches.id\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE matches.id IN (\
							SELECT matches.id AS matchIds\
							FROM matches\
							LEFT JOIN teams ON matches.id = teams.matchId\
							LEFT JOIN teams_players ON teams.id = teams_players.teamId\
							WHERE teams_players.playerId = :playerId\
								AND matches.complete = 1\
						)\
						AND teams_players.playerId != :playerId\
				)\
			GROUP BY players.id, matches.matchType\
		"

		connection = self.session.connection()
		return connection.execute(text(query), playerId = playerId)

	def pointStreakByPlayer(self, streakData, playerId):
		currentStreak = -1
		longestStreak = -1

		matchId = None
		game = None

		for item in streakData:
			if matchId != item["matchId"]:
				matchId = item["matchId"]
				currentStreak = -1
			if game != item["game"]:
				game = item["game"]
				currentStreak = -1
			if playerId not in item["playerIds"]:
				currentStreak = -1

			currentStreak += 1

			longestStreak = max(currentStreak, longestStreak)

		return longestStreak

	def winStreakByPlayer(self, streakData, playerId):

		streak = 0
		value = None

		for item in streakData:
			if playerId not in item["playerIds"]:
				continue

			if value == None:
				value = item["win"]
				streak = 1 if value == 1 else -1
				continue

			if value == 1 and item["win"] == 1:
				streak += 1
			elif value == 0 and item["win"] == 0:
				streak -= 1
			elif value != item["win"]:
				return streak

		return streak

	def winStreakByMatchType(self, streakData, matchType):

		streak = 0
		value = None

		for item in streakData:
			if item["matchType"] != matchType:
				continue

			if value == None:
				value = item["win"]
				streak = 1 if value == 1 else -1
				continue

			if value == 1 and item["win"] == 1:
				streak += 1
			elif value == 0 and item["win"] == 0:
				streak -= 1
			elif value != item["win"]:
				return streak

		return streak

	def selectMatchScoresByMatchType(self, matchType):
		query = "\
			SELECT scores.id, scores.matchId, scores.teamId, scores.game, matches.matchType, group_concat(teams_players.playerId) as playerIds\
			FROM scores\
			LEFT JOIN teams_players ON scores.teamId = teams_players.teamId\
			LEFT JOIN matches ON scores.matchId = matches.id\
			WHERE matches.complete = 1 AND matches.matchType = :matchType\
			GROUP BY scores.id\
		"

		connection = self.session.connection()
		results = connection.execute(text(query), matchType = matchType)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"matchId": row.matchId,
				"teamId": row.teamId,
				"game": row.game,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		return data

	def selectTeamResultsByMatchType(self, matchType):
		query  = "\
			SELECT teams.id, teams.win, matches.matchType, GROUP_CONCAT(teams_players.playerId) AS playerIds\
			FROM teams\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.matchType = :matchType AND matches.complete = 1\
			GROUP BY teams.id\
			ORDER BY teams.id DESC\
		"

		connection = self.session.connection()
		results = connection.execute(text(query), matchType = matchType)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"win": row.win,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		return data

	def selectTeamResultsByPlayer(self, playerId):
		query  = "\
			SELECT teams.id, teams.win, matches.matchType, GROUP_CONCAT(teams_players.playerId) AS playerIds\
			FROM teams\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1 AND teams_players.playerId = :playerId\
			GROUP BY teams.id\
			ORDER BY matches.matchType, teams.id DESC\
		"
		connection = self.session.connection()
		results = connection.execute(text(query), playerId = playerId)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"win": row.win,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		return data

	def formatTime(self, seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return "%02d:%02d:%02d" % (h, m, s)
