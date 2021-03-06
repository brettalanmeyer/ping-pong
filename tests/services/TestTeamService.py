from BaseTest import BaseTest
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.TeamService import TeamService
import json

matchService = MatchService()
playerService = PlayerService()
teamService = TeamService()

class TestTeamService(BaseTest):

	def createMatch(self, officeId):
		return matchService.create(officeId, "singles")

	def createTeam(self, officeId):
		match = self.createMatch(officeId);
		return teamService.create(match.id)

	def test_select(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			teams = teamService.select()
			assert teams.count() > 0

	def test_selectById(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			newTeam = teamService.selectById(team.id)
			assert team == newTeam

	def test_selectByMatch(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			teams = teamService.selectByMatch(team.match)
			assert teams.count() == 1

	def test_selectByMatchId(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			teams = teamService.selectByMatchId(team.match.id)
			assert teams.count() == 1

	def test_create(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			team = teamService.create(match.id)
			assert len(match.teams) == 1
			assert match.teams[0].id == team.id
			assert team != None

	def test_createOnePlayer(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			player = playerService.create(office["id"], { "name": "Jerry" })
			team = teamService.createOnePlayer(match.id, player.id)
			assert team.match.id == match.id
			assert len(team.players) == 1
			assert team.players[0].id == player.id

	def test_createTwoPlayer(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			player1 = playerService.create(office["id"], { "name": "Jerry" })
			player2 = playerService.create(office["id"], { "name": "Tom" })
			team = teamService.createTwoPlayer(match.id, player1.id, player2.id)
			assert team.match.id == match.id
			assert len(team.players) == 2

	def test_win(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			teamService.win(team)
			assert team.win

	def test_lose(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			teamService.lose(team)
			assert not team.win

	def test_serialize(self):
		office = self.office()

		with self.ctx:
			team = self.createTeam(office["id"])
			teams = teamService.select()
			data = json.loads(teamService.serialize(teams))
			assert teams.count() == len(data)

