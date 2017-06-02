from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import abort
from flask import current_app as app
from pingpong.models.PlayerModel import PlayerModel
from pingpong.services.OfficeService import OfficeService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import text
import math

playerService = PlayerService()
officeService = OfficeService()

class LeaderboardService(Service):

	def matchTypeStats(self, officeId, matchType, season):
		app.logger.info("Querying Leaderboard Statistics by matchType=%s and season=%s", matchType, season)

		players = playerService.select(officeId)
		seasons, season, start, end = self.seasons(season, officeId)

		matches = self.matchesByMatchType(officeId, matchType, start, end)
		times = self.times(officeId, matchType, start, end)
		pointsFor = self.pointsForByMatchType(officeId, matchType, start, end)
		pointsAgainst = self.pointsAgainstByMatchType(officeId, pointsFor, matchType, start, end)
		pointStreakData = self.selectMatchScoresByMatchType(officeId, matchType, start, end)
		currentStreakData = self.selectTeamResultsByMatchType(officeId, matchType, start, end)
		elo = self.elo(officeId, start, end)

		stats = {
			"matchType": matchType,
			"season": season,
			"seasons": seasons,
			"start": start,
			"end": end,
			"players": [],
			"totals": {}
		}

		for player in players:

			playerElo = elo["players"][player.id]

			currentStreak, winStreak, lossStreak = self.winLossStreakByPlayer(currentStreakData, player.id)

			stats["players"].append({
				"playerId": player.id,
				"playerName": player.name,
				"playerAvatar": player.avatar,
				"matches": matches[player.id]["matches"] if player.id in matches else 0,
				"percentage": float(matches[player.id]["wins"]) / float(matches[player.id]["matches"]) * 100 if player.id in matches else 0,
				"pointsFor": pointsFor[player.id] if player.id in pointsFor else 0,
				"pointsAgainst": pointsAgainst[player.id] if player.id in pointsAgainst else 0,
				"wins": matches[player.id]["wins"] if player.id in matches else 0,
				"losses": matches[player.id]["losses"] if player.id in matches else 0,
				"seconds": times[player.id] if player.id in matches else 0,
				"time": util.formatTime(times[player.id]) if player.id in times else 0,
				"pointStreak": self.pointStreakByPlayer(pointStreakData, player.id),
				"streaks": {
					"current": currentStreak,
					"wins": winStreak,
					"losses": lossStreak
				},
				"elo": {
					"current": playerElo["current"],
					"previous": playerElo["previous"],
					"change": playerElo["change"]
				}
			})

		stats["totals"] = self.totals(stats["players"])

		return stats

	def playerStats(self, player, season):
		app.logger.debug("Querying player stats: playerId=%s season=%s", player.id, season)

		seasons, season, start, end = self.seasons(season, player.officeId)

		matches = self.matchesByPlayer(player.id, start, end)
		pointsFor = self.pointsForByPlayer(player.id, start, end)
		pointsAgainst = self.pointsAgainstByPlayer(pointsFor, player.id, start, end)
		winStreakData = self.selectTeamResultsByPlayer(player.id, start, end)

		stats = {
			"playerId": player.id,
			"playerName": player.name,
			"playerAvatar": player.avatar,
			"season": season,
			"seasons": seasons,
			"start": start,
			"end": end

		}

		for matchType in self.matchTypes:

			currentStreak, winStreak, lossStreak = self.currentStreakByMatchType(winStreakData, matchType)

			stats[matchType] = {
				"matches": 0,
				"wins": 0,
				"losses": 0,
				"percentage": 0,
				"pointsFor": 0,
				"pointsAgainst": 0,
				"matchups": [],
				"streaks": {
					"current": currentStreak,
					"wins": winStreak,
					"losses":  lossStreak
				}
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

		results = self.matchups(player.id, start, end)

		for result in results:
			pointsFor = self.pointsForByOpponent(player.id, result.playerId, start, end)
			pointsAgainst = self.pointsAgainstByOpponent(pointsFor, player.id, result.playerId, start, end)
			currentStreakData = self.selectTeamResultsByOpponent(player.id, result.playerId, start, end)

			# points and win/loss are inverted because these stats show the player vs this opponent
			stats[result.matchType]["matchups"].append({
				"playerId": result.playerId,
				"playerName": result.playerName,
				"playerAvatar": result.playerAvatar,
				"numOfMatches": int(result.numOfMatches),
				"pointsFor": pointsAgainst[result.matchType],
				"pointsAgainst": pointsFor[result.matchType],
				"wins": int(result.losses),
				"losses": int(result.wins),
				"percentage": float(result.losses) / float(result.numOfMatches) * 100,
				"streaks": {
					"current": currentStreakData[result.matchType]["current"],
					"wins": currentStreakData[result.matchType]["wins"],
					"losses": currentStreakData[result.matchType]["losses"]
				}
			})

		return stats

	def matchesByMatchType(self, officeId, matchType, start, end):
		app.logger.debug("Querying matches by matchType=%s start=%s end=%s", matchType, start, end)

		query = "\
			SELECT players.id AS playerId, COUNT(*) AS matches, SUM(teams.win = 1) AS wins, SUM(teams.win = 0) AS losses\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
				AND matches.matchType = :matchType\
				AND matches.officeId = :officeId\
		"
		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY players.id "

		connection = db.session.connection()
		matches = connection.execute(text(query), officeId = officeId, matchType = matchType, start = start, end = end)

		data = {}

		for match in matches:
			data[int(match.playerId)] = {
				"matches": int(match.matches),
				"wins": int(match.wins),
				"losses": int(match.losses)
			}

		return data

	def matchesByPlayer(self, playerId, start, end):
		app.logger.debug("Querying matches by playerId=%d start=%s end=%s", playerId, start, end)

		query = "\
			SELECT players.id AS playerId, matches.matchType, COUNT(*) AS matches, SUM(teams.win = 1) AS wins, SUM(teams.win = 0) AS losses\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
				AND players.id = :playerId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY matches.matchType "

		connection = db.session.connection()
		matches = connection.execute(text(query), playerId = playerId, start = start, end = end)

		data = {}

		for match in matches:
			data[match.matchType] = {
				"matches": int(match.matches),
				"wins": int(match.wins),
				"losses": int(match.losses),
				"percentage": float(match.wins) / float(match.matches) * 100
			}

		return data

	def times(self, officeId, matchType, start, end):
		app.logger.debug("Querying time played by matchType=%s start=%s end=%s", matchType, start, end)

		query = "\
			SELECT DISTINCT players.id as playerId, UNIX_TIMESTAMP(matches.createdAt) as gameTime, UNIX_TIMESTAMP(matches.completedAt) as resultTime\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
				AND matches.matchType = :matchType\
				AND matches.officeId = :officeId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		connection = db.session.connection()
		times = connection.execute(text(query), officeId = officeId, matchType = matchType, start = start, end = end)

		data = {}

		for time in times:
			if time.playerId not in data:
				data[time.playerId] = 0

			data[time.playerId] = data[time.playerId] + time.resultTime - time.gameTime

		return data

	def pointsForByMatchType(self, officeId, matchType, start, end):
		app.logger.debug("Querying points for by matchType=%s start=%s end=%s", matchType, start, end)

		query = "\
			SELECT players.id AS playerId, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE matches.complete = 1\
				AND matches.matchType = :matchType\
				AND matches.officeId = :officeId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY players.id "

		connection = db.session.connection()
		points = connection.execute(text(query), officeId = officeId, matchType = matchType, start = start, end = end)

		data = {}

		for point in points:
			data[point.playerId] = point.points

		return data

	def pointsForByPlayer(self, playerId, start, end):
		app.logger.debug("Querying points for by playerId=%d start=%s end=%s", playerId, start, end)

		query = "\
			SELECT players.id AS playerId, matches.matchType, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE matches.complete = 1\
				AND players.id = :playerId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY matches.matchType "

		connection = db.session.connection()
		points = connection.execute(text(query), playerId = playerId, start = start, end = end)

		data = {}

		for point in points:
			data[point.matchType] = point.points

		return data

	def pointsForByOpponent(self, playerId, opponentId, start, end):
		app.logger.debug("Querying points for by opponentId=%d playerId=%d start=%s end=%s", opponentId, playerId, start, end)

		query = "\
			SELECT players.id AS playerId, matches.matchType, COUNT(scores.id) as points\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			LEFT JOIN scores ON teams.id = scores.teamId AND matches.id = scores.matchId\
			WHERE players.id = :opponentId\
				AND matches.id IN (\
					SELECT matches.id AS matchIds\
					FROM matches\
					LEFT JOIN teams ON matches.id = teams.matchId\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE teams_players.playerId = :playerId\
						AND matches.complete = 1\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += "\
				)\
			GROUP BY matches.matchType\
		"

		connection = db.session.connection()
		points = connection.execute(text(query), playerId = playerId, opponentId = opponentId, start = start, end = end)

		data = {}

		for point in points:
			data[point.matchType] = point.points

		return data

	def pointsAgainstByMatchType(self, officeId, pointsFor, matchType, start, end):
		app.logger.debug("Querying points against by matchType=%s start=%s end=%s", matchType, start, end)

		query = "\
			SELECT players.id as playerId, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
				AND matches.matchType = :matchType\
				AND matches.officeId = :officeId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY players.id "

		connection = db.session.connection()
		matches = connection.execute(text(query), officeId = officeId, matchType = matchType, start = start, end = end)

		data = {}

		for match in matches:
			matchIds = map(int, match.matchIds.split(","))
			matchIds.append(0)

			query = "\
				SELECT COUNT(*) as points\
				FROM scores\
				WHERE matchId IN :matchIds\
			"
			connection = db.session.connection()
			points = connection.execute(text(query), matchIds = matchIds).first()

			data[match.playerId] = points.points - pointsFor[match.playerId]

		return data

	def pointsAgainstByPlayer(self, pointsFor, playerId, start, end):
		app.logger.debug("Querying points against by playerId=%d start=%s end=%s", playerId, start, end)

		query = "\
			SELECT players.id as playerId, matches.matchType, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
				AND players.id = :playerId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY matches.matchType "

		connection = db.session.connection()
		matches = connection.execute(text(query), playerId = playerId, start = start, end = end)

		data = {}

		for match in matches:
			matchIds = map(int, match.matchIds.split(","))
			matchIds.append(0)

			query = "\
				SELECT COUNT(*) as points\
				FROM scores\
				WHERE matchId IN :matchIds\
			"
			connection = db.session.connection()
			points = connection.execute(text(query), matchIds = matchIds).first()

			data[match.matchType] = points.points - pointsFor[match.matchType]

		return data

	def pointsAgainstByOpponent(self, pointsFor, playerId, opponentId, start, end):
		app.logger.debug("Querying points against by opponent=%d playerId=%d start=%s end=%s", opponentId, playerId, start, end)

		query = "\
			SELECT players.id as playerId, matches.matchType, GROUP_CONCAT(teams.matchId) as matchIds\
			FROM players\
			LEFT JOIN teams_players ON players.id = teams_players.playerId\
			LEFT JOIN teams ON teams_players.teamId = teams.id\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE players.id = :opponentId\
				AND matches.id IN (\
					SELECT matches.id AS matchIds\
					FROM matches\
					LEFT JOIN teams ON matches.id = teams.matchId\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE teams_players.playerId = :playerId\
						AND matches.complete = 1\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += "\
				)\
			GROUP BY matches.matchType\
		"
		connection = db.session.connection()
		matches = connection.execute(text(query), playerId = playerId, opponentId = opponentId, start = start, end = end)

		data = {}

		for match in matches:
			matchIds = map(int, match.matchIds.split(","))
			matchIds.append(0)

			query = "\
				SELECT COUNT(*) as points\
				FROM scores\
				WHERE matchId IN :matchIds\
			"
			connection = db.session.connection()
			points = connection.execute(text(query), matchIds = matchIds).first()

			data[match.matchType] = points.points - pointsFor[match.matchType]

		return data

	def selectTeamResultsByOpponent(self, playerId, opponentId, start, end):
		app.logger.debug("Querying team results by playerId=%d opponent=%d start=%s end=%s", playerId, opponentId, start, end)

		query = "\
			SELECT teams.id, teams.win, matches.matchType, GROUP_CONCAT(teams_players.playerId) AS playerIds\
			FROM teams\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE teams_players.playerId = :opponentId\
				AND matches.id IN (\
					SELECT matches.id AS matchIds\
					FROM matches\
					LEFT JOIN teams ON matches.id = teams.matchId\
					LEFT JOIN teams_players ON teams.id = teams_players.teamId\
					WHERE teams_players.playerId = :playerId\
						AND matches.complete = 1\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += "\
				)\
			GROUP BY teams.id\
		"

		connection = db.session.connection()
		results = connection.execute(text(query), playerId = playerId, opponentId = opponentId, start = start, end = end)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"result": row.win,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		streaks = {}
		for matchType in self.matchTypes:
			streaks[matchType] = {}
			streaks[matchType]["current"], streaks[matchType]["wins"], streaks[matchType]["losses"] = self.currentStreakByMatchType(data, matchType)

			# invert due to opponent's streak
			if matchType != "nines":
				streaks[matchType]["current"] *= -1
				streaks[matchType]["wins"] *= -1
				streaks[matchType]["losses"] *= -1

		return streaks

	def totals(self, rows):
		app.logger.debug("Calculating totals")

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

		totals["time"] = util.formatTime(totals["seconds"])

		return totals

	def matchups(self, playerId, start, end):
		app.logger.debug("Calculating matchups for playerId=%d start=%s end=%s", playerId, start, end)

		query = "\
			SELECT\
				players.id as playerId,\
				players.name as playerName,\
				players.avatar as playerAvatar,\
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
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += "\
						)\
						AND teams_players.playerId != :playerId\
				)\
			GROUP BY players.id, matches.matchType\
		"

		connection = db.session.connection()
		return connection.execute(text(query), playerId = playerId, start = start, end = end)

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

		if longestStreak == -1:
			return 0

		return longestStreak

	def winLossStreakByPlayer(self, streakData, playerId):
		streak = 0
		wins = 0
		losses = 0
		result = None

		for item in streakData:
			if playerId not in item["playerIds"]:
				continue

			if result != item["result"]:
				streak = 0
				result = item["result"]

			if result == 1:
				streak += 1
			elif result == 0:
				streak -= 1

			if streak > wins:
				wins = streak
			if streak < losses:
				losses = streak

		return streak, wins, abs(losses)

	def currentStreakByMatchType(self, streakData, matchType):
		streak = 0
		wins = 0
		losses = 0
		result = None

		for item in streakData:
			if item["matchType"] != matchType:
				continue

			if result != item["result"]:
				streak = 0
				result = item["result"]

			if result == 1:
				streak += 1
			elif result == 0:
				streak -= 1

			if streak > wins:
				wins = streak
			if streak < losses:
				losses = streak

		return streak, wins, abs(losses)

	def selectMatchScoresByMatchType(self, officeId, matchType, start, end):
		app.logger.debug("Querying match scores by matchType=%s start=%s end=%s", matchType, start, end)

		query = "\
			SELECT scores.id, scores.matchId, scores.teamId, scores.game, matches.matchType, group_concat(teams_players.playerId) as playerIds\
			FROM scores\
			LEFT JOIN teams_players ON scores.teamId = teams_players.teamId\
			LEFT JOIN matches ON scores.matchId = matches.id\
			WHERE matches.complete = 1\
				AND matches.matchType = :matchType\
				AND matches.officeId = :officeId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY scores.id "

		connection = db.session.connection()
		results = connection.execute(text(query), officeId = officeId, matchType = matchType, start = start, end = end)

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

	def selectTeamResultsByMatchType(self, officeId, matchType, start, end):
		app.logger.debug("Querying team results by matchType=%s start=%s end=%s", matchType, start, end)

		query  = "\
			SELECT teams.id, teams.win, matches.matchType, GROUP_CONCAT(teams_players.playerId) AS playerIds\
			FROM teams\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.matchType = :matchType\
				AND matches.complete = 1\
				AND matches.officeId = :officeId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += " GROUP BY teams.id "

		connection = db.session.connection()
		results = connection.execute(text(query), officeId = officeId, matchType = matchType, start = start, end = end)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"result": row.win,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		return data

	def selectTeamResultsByPlayer(self, playerId, start, end):
		app.logger.debug("Querying team results by playerId=%d start=%s end=%s", playerId, start, end)

		query  = "\
			SELECT teams.id, teams.win, matches.matchType, GROUP_CONCAT(teams_players.playerId) AS playerIds\
			FROM teams\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN matches ON teams.matchId = matches.id\
			WHERE matches.complete = 1\
				AND teams_players.playerId = :playerId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += "\
			GROUP BY teams.id\
			ORDER BY matches.matchType\
		"
		connection = db.session.connection()
		results = connection.execute(text(query), playerId = playerId, start = start, end = end)

		data = []

		for row in results:
			data.append({
				"id": row.id,
				"result": row.win,
				"matchType": row.matchType,
				"playerIds": map(int, row.playerIds.split(","))
			})

		return data

	def singlesResults(self, officeId, start, end):
		app.logger.debug("Querying singles results start=%s end=%s", start, end)

		query  = "\
			SELECT matches.id AS matchId, GROUP_CONCAT(players.id, ',', IF(teams.win = 1, 'win', 'loss')) AS record\
			FROM matches\
			LEFT JOIN teams ON matches.id = teams.matchId\
			LEFT JOIN teams_players ON teams.id = teams_players.teamId\
			LEFT JOIN players ON teams_players.playerId = players.id\
			WHERE matches.matchType = 'singles'\
				AND matches.complete = 1\
				AND matches.officeId = :officeId\
		"

		if start != None:
			query += " AND matches.completedAt >= :start "
		if end != None:
			query += " AND matches.completedAt < :end "

		query += "\
			GROUP BY matches.id\
			ORDER BY matches.id\
		"
		connection = db.session.connection()
		results = connection.execute(text(query), officeId = officeId, start = start, end = end)

		data = []

		for result in results:
			if result.record != None:
				id1, result1, id2, result2 = result.record.split(",")

				winner = int(id1)
				loser = int(id2)

				if result2 == "win":
					winner = int(id2)
					loser = int(id1)

				data.append({
					"matchId": result.matchId,
					"winner": winner,
					"loser": loser
				})

		return data

	def elo(self, officeId, start, end):
		app.logger.debug("Calculating ELO start=%s end=%s", start, end)

		# ELO rating system
		# https://en.wikipedia.org/wiki/Elo_rating_system
		# https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/

		results = self.singlesResults(officeId, start, end)
		players = playerService.select(officeId)

		data = {
			"matches": {},
			"players": {}
		}

		# inital performance rating
		for player in players:
			data["players"][player.id] = {
				"current": app.config["ELO_PERFORMANCE_RATING"],
				"previous": 0,
				"change": 0
			}

		KVALUE = app.config["ELO_K_VALUE"]

		for result in results:

			winner = data["players"][result["winner"]]
			loser = data["players"][result["loser"]]

			# current performance rating
			r1 = float(winner["current"])
			r2 = float(loser["current"])

			R1 = math.pow(10, r1 / 400L)
			R2 = math.pow(10, r2 / 400L)

			E1 = R1 / (R1 + R2)
			E2 = R2 / (R1 + R2)

			S1 = 1L # 1 points for win
			S2 = 0L # 0 points for loss

			r1p = r1 + KVALUE * (S1 - E1)
			r2p = r2 + KVALUE * (S2 - E2)

			# set previous to current before updating
			winner["previous"] = winner["current"]
			loser["previous"] = loser["current"]

			# new performance rating
			winner["current"] = r1p
			loser["current"] = r2p

			winner["change"] = winner["current"] - winner["previous"]
			loser["change"] = loser["current"] - loser["previous"]

			data["matches"][result["matchId"]] = {}
			data["matches"][result["matchId"]][result["winner"]] = {
				"current": winner["current"],
				"previous": winner["previous"],
				"change": winner["change"]
			}
			data["matches"][result["matchId"]][result["loser"]] = {
				"current": loser["current"],
				"previous": loser["previous"],
				"change": loser["change"]
			}

		return data

	def eloResult(self, officeId, matchId, playerId):
		seasons, season, start, end = self.seasons(None, officeId)
		elo = self.elo(officeId, start, end)

		# return specific elo for that match
		if matchId in elo["matches"] and playerId in elo["matches"][matchId]:
			return elo["matches"][matchId][playerId]

		# if match is not found, return current player elo
		if playerId in elo["players"]:
			return elo["players"][playerId]

		return None

	def seasons(self, season, officeId):
		app.logger.debug("Generating seasons with default season=%s", season)

		office = officeService.selectById(officeId)
		begin = datetime(office.seasonYear, office.seasonMonth, 1)

		index = 0
		seasons = []
		dateFormat = "{:%b %d, %Y}"

		while True:
			start = begin + relativedelta(months = 3 * index)
			end = start + relativedelta(months = 3)
			last = start + relativedelta(months = 3, days = -1)

			seasons.append({
				"id": index + 1,
				"label": "Season {}".format(index + 1),
				"start": start,
				"end": end,
				"last": last
			})

			if (end > datetime.now()):
				break

			index += 1

		# default to latest or current season
		if season == None:
			return seasons, len(seasons), seasons[len(seasons) - 1]["start"], seasons[len(seasons) - 1]["end"]

		# specified season
		elif season > 0 and season <= len(seasons):
			return seasons, season, seasons[season - 1]["start"], seasons[season - 1]["end"]

		# all seasons
		elif season == 0:
			return seasons, 0, None, None

		# invalid parameter
		else:
			abort(404)
