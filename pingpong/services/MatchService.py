from datetime import datetime
from flask import current_app as app
from pingpong.models.GameModel import GameModel
from pingpong.models.MatchModel import MatchModel
from pingpong.models.PlayerModel import PlayerModel
from pingpong.models.TeamModel import TeamModel
from pingpong.services.Service import Service
from pingpong.utils import database as db
from pingpong.utils import util
from sqlalchemy import or_
import json

class MatchService(Service):

	def select(self, officeId):
		app.logger.info("Selecting matches")

		return db.session.query(MatchModel).filter(MatchModel.officeId == officeId)

	def selectCount(self, officeId):
		app.logger.info("Selecting number of matches")

		return self.select(officeId).count()

	def selectById(self, id):
		app.logger.info("Selecting match=%d", id)

		matches = db.session.query(MatchModel).filter(MatchModel.id == id)

		if matches.count() == 1:
			return matches.one()

		return None

	def selectNotById(self, id, officeId):
		app.logger.info("Selecting matches excluding match=%d", id)

		return db.session.query(MatchModel).filter(MatchModel.id != id, MatchModel.officeId == officeId)

	def selectComplete(self, officeId = None):
		app.logger.info("Selecting completed matches")

		matches = db.session.query(MatchModel).filter(MatchModel.complete == True).order_by(MatchModel.id.desc())

		if officeId != None:
			matches = matches.filter(MatchModel.officeId == officeId)

		return matches

	def selectCompleteOrReady(self, officeId, playerId = None, opponentId = None, matchType = None, start = None, end = None):
		app.logger.info("Selecting complete or ready for play matches")

		matches = db.session.query(MatchModel).filter(MatchModel.officeId == officeId, or_(MatchModel.complete == True, MatchModel.ready == True)).order_by(MatchModel.id.desc())

		if playerId != None:
			matches = matches.join(MatchModel.teams).join(TeamModel.players).filter(PlayerModel.id == playerId)

			if opponentId != None:
				ids = []
				for match in matches:
					if self.hasOpponent(match, opponentId):
						ids.append(match.id)

				matches = db.session.query(MatchModel).filter(MatchModel.id.in_(ids)).order_by(MatchModel.id.desc())

		if matchType != None:
			matches = matches.filter(MatchModel.matchType == matchType)

		if start != None:
			matches = matches.filter(MatchModel.createdAt >= start)

		if end != None:
			matches = matches.filter(MatchModel.createdAt < end)

		return matches

	def hasOpponent(self, match, opponentId):
		for team in match.teams:
			for player in team.players:
				if player.id == opponentId:
					return True

		return False

	def selectActiveMatch(self, officeId):
		app.logger.info("Selecting active match")

		matches = db.session.query(MatchModel).filter(MatchModel.ready == True, MatchModel.complete == False, MatchModel.officeId == officeId).order_by(MatchModel.id.desc())

		if matches.count() == 0:
			return None

		return matches.first()

	def selectLatestMatch(self, officeId):
		app.logger.info("Selecting latest completed match")

		matches = db.session.query(MatchModel).filter(MatchModel.complete == True, MatchModel.officeId == officeId).order_by(MatchModel.id.desc())

		if matches.count() == 0:
			return None

		return matches.first()

	def setAsNotReady(self, id):
		app.logger.info("Updateing all matches except current one to not ready")

		update(MatchModel).where(MatchModel.id != id).values(ready = False)
		db.session.commit()

	def create(self, officeId, matchType):
		playTo = 21
		if matchType == "nines":
			playTo = 9

		match = MatchModel(officeId, matchType, playTo, 0, False, False, datetime.now(), datetime.now())
		db.session.add(match)
		db.session.commit()

		app.logger.info("Creating match=%d", match.id)

		return match

	def updateGames(self, id, numOfGames):
		match = self.selectById(id)
		match.numOfGames = numOfGames
		match.game = 1
		match.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating match=%d numOfGames=%d game=%d", match.id, match.numOfGames, match.game)

		return match

	def updateGame(self, id, game):
		match = self.selectById(id)
		match.game = game
		match.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating match=%d game=%d", match.id, match.game)

		return match

	def play(self, match):
		matches = self.selectNotById(match.id, match.officeId)
		for item in matches:
			item.ready = False

		match.ready = True
		match.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Play match=%d", match.id)

	def incomplete(self, match):
		match.complete = False
		match.modifiedAt = datetime.now()
		match.completedAt = None
		db.session.commit()

		app.logger.info("Incompleting match=%d", match.id)

	def complete(self, match):
		match.complete = True
		match.modifiedAt = datetime.now()
		match.completedAt = datetime.now()
		db.session.commit()

		app.logger.info("Completing match=%d", match.id)

	def deleteById(self, id):
		app.logger.info("Deleting match by id=%d", id)
		match = self.selectById(id)
		return self.delete(match)

	def delete(self, match):
		app.logger.info("Deleting match=%d", match.id)

		try:
			db.session.delete(match)
			db.session.commit()
			return match, True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return match, False

	def deleteAll(self):
		app.logger.info("Deleting all matches")

		try:
			db.session.query(MatchModel).delete()
			db.session.commit()
			return True

		except exc.SQLAlchemyError, error:
			db.session.rollback()
			return False

	def serializeMatch(self, match):
		app.logger.info("Serializing matchId=%d", match.id)

		data = {
			"id": match.id,
			"matchType": match.matchType,
			"playTo": match.playTo,
			"numOfGames": match.numOfGames,
			"game": match.game,
			"ready": match.ready,
			"complete": match.complete,
			"createdAt": match.createdAt,
			"modifiedAt": match.modifiedAt,
			"completedAt": match.completedAt,
			"teams": [],
			"games": []
		}

		for team in match.teams:
			teamData = {
				"id": team.id,
				"win": team.hasWon(),
				"createdAt": team.createdAt,
				"modifiedAt": team.modifiedAt,
				"players": []
			}

			for player in team.players:
				teamData["players"].append({
					"id": player.id,
					"name": player.name
				})

			data["teams"].append(teamData)

		for game in match.games:
			gameData = {
				"id": game.id,
				"game": game.game,
				"green": None,
				"yellow": None,
				"blue": None,
				"red": None,
				"winner": game.winner,
				"winnerScore": game.winnerScore,
				"loser": game.loser,
				"loserScore": game.loserScore,
				"createdAt": game.createdAt,
				"modifiedAt": game.modifiedAt,
				"completedAt": game.completedAt,
				"scores": []
			}

			if game.green != None:
				gameData["green"] = {
					"id": game.green.id,
					"name": game.green.name
				}

			if game.yellow != None:
				gameData["yellow"] = {
					"id": game.yellow.id,
					"name": game.yellow.name
				}

			if game.blue != None:
				gameData["blue"] = {
					"id": game.blue.id,
					"name": game.blue.name
				}

			if game.red != None:
				gameData["red"] = {
					"id": game.red.id,
					"name": game.red.name
				}

			data["games"].append(gameData)

		for score in match.scores:
			data["games"][score.game - 1]["scores"].append({
				"id": score.id,
				"createdAt": score.createdAt
			})

		return json.dumps(data, default = util.jsonSerial)

	def serializeMatches(self, matches):
		app.logger.info("Serializing matches")

		data = []

		for match in matches:
			data.append({
				"id": match.id,
				"matchType": match.matchType,
				"playTo": match.playTo,
				"numOfGames": match.numOfGames,
				"game": match.game,
				"ready": match.ready,
				"complete": match.complete,
				"createdAt": match.createdAt,
				"modifiedAt": match.modifiedAt,
				"completedAt": match.completedAt,
			})

		return json.dumps(data, default = util.jsonSerial)
