from datetime import datetime
from flask import current_app as app
from pingpong.models.TeamModel import TeamModel
from pingpong.services.Service import Service
from pingpong.services import PlayerService
from pingpong.utils import database as db
from pingpong.utils import util
import json

playerService = PlayerService.PlayerService()

class TeamService(Service):

	def select(self):
		app.logger.info("Selecting teams")

		return db.session.query(TeamModel)

	def selectById(self, id):
		app.logger.info("Selecting team=%d", id)

		return db.session.query(TeamModel).filter(TeamModel.id == id).one()

	def selectByMatch(self, match):
		return self.selectByMatchId(match.id)

	def selectByMatchId(self, id):
		app.logger.info("Selecting teams by matchId=%d", id)

		return db.session.query(TeamModel).filter(TeamModel.matchId == id)

	def create(self, matchId):
		team = TeamModel(matchId, datetime.now(), datetime.now())
		db.session.add(team)
		db.session.commit()

		app.logger.info("Creating team=%d match=%d", team.id, team.matchId)

		return team

	def createOnePlayer(self, matchId, playerId):
		team = self.create(matchId)
		team.players.append(playerService.selectById(playerId))

		app.logger.info("Creating single player team=%d match=%d player=%d", team.id, matchId, playerId)

		return team

	def createTwoPlayer(self, matchId, player1Id, player2Id):
		team = self.create(matchId)
		team.players.append(playerService.selectById(player1Id))
		team.players.append(playerService.selectById(player2Id))
		db.session.commit()

		app.logger.info("Creating two player team=%d match=%d player1=%d player2=%d", team.id, matchId, player1Id, player2Id)

		return team

	def win(self, team):
		self.status(team, True)

	def lose(self, team):
		self.status(team, False)

	def status(self, team, win):
		team.win = win
		team.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Team win=%s team=%d", win, team.id)

	def serialize(self, teams):
		app.logger.info("Serializing teams")

		data = []

		for team in teams:
			teamData = {
				"id": team.id,
				"matchId": team.matchId,
				"win": team.hasWon(),
				"players": []
			}

			for player in team.players:
				teamData["players"].append(player.id)

			data.append(teamData)

		return json.dumps(data, default = util.jsonSerial)