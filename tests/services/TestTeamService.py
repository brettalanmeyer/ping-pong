from BaseTest import BaseTest
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.TeamService import TeamService

matchService = MatchService()
playerService = PlayerService()
teamService = TeamService()

class TestTeamService(BaseTest):

	def createMatch(self):
		return matchService.create("singles")

	def createTeam(self):
		match = self.createMatch();
		return teamService.create(match.id)

	def test_selectById(self):
		with self.ctx:
			team = self.createTeam()
			newTeam = teamService.selectById(team.id)
			assert team == newTeam

	def test_create(self):
		with self.ctx:
			match = self.createMatch()
			team = teamService.create(match.id)
			assert len(match.teams) == 1
			assert match.teams[0].id == team.id
			assert team != None

	def test_createOnePlayer(self):
		with self.ctx:
			match = self.createMatch()
			player = playerService.create({ "name": "Jerry" })
			team = teamService.createOnePlayer(match.id, player.id)
			assert team.match.id == match.id
			assert len(team.players) == 1
			assert team.players[0].id == player.id

	def test_createTwoPlayer(self):
		with self.ctx:
			match = self.createMatch()
			player1 = playerService.create({ "name": "Jerry" })
			player2 = playerService.create({ "name": "Tom" })
			team = teamService.createTwoPlayer(match.id, player1.id, player2.id)
			assert team.match.id == match.id
			assert len(team.players) == 2

	def test_win(self):
		with self.ctx:
			team = self.createTeam()
			teamService.win(team)
			assert team.win

	def test_lose(self):
		with self.ctx:
			team = self.createTeam()
			teamService.lose(team)
			assert not team.win
