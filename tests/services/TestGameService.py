from BaseTest import BaseTest
from pingpong.services.GameService import GameService
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.TeamService import TeamService

gameService = GameService()
matchService = MatchService()
playerService = PlayerService()
teamService = TeamService()

class TestGameService(BaseTest):

	def createGame(self):
		match = matchService.create("singles")
		return match, gameService.create(match.id, 1, None, None, None, None)

	def test_select(self):
		with self.ctx:
			self.createGame()
			self.createGame()
			games = gameService.select()
			assert games.count() >= 2

	def test_selectCount(self):
		with self.ctx:
			self.createGame()
			self.createGame()
			assert gameService.selectCount() >= 2

	def test_create(self):
		with self.ctx:
			match = matchService.create("singles")
			green = playerService.create({ "name": "Joe" })
			yellow = playerService.create({ "name": "Matt" })
			blue = playerService.create({ "name": "Greg" })
			red = playerService.create({ "name": "Jesus" })
			game = gameService.create(match.id, 1, green.id, yellow.id, blue.id, red.id)

			assert game.match.id == match.id
			assert game.green == green.id
			assert game.yellow == yellow.id
			assert game.blue == blue.id
			assert game.red == red.id
			assert game.completedAt == None
			assert game.winner == None
			assert game.winnerScore == None
			assert game.loser == None
			assert game.loserScore == None

	def test_complete(self):
		with self.ctx:
			match, game = self.createGame()
			team1 = teamService.create(match.id)
			team2 = teamService.create(match.id)
			gameService.complete(match.id, 1, team1.id, 21, team2.id, 8)

			assert game.winner == team1.id
			assert game.winnerScore == 21
			assert game.loser == team2.id
			assert game.loserScore == 8

			resetGame = gameService.resetGame(match.id, 1)

			assert resetGame != None
			assert resetGame.winner == None
			assert resetGame.winnerScore == None
			assert resetGame.loser == None
			assert resetGame.loserScore == None

	def test_getTeamWins(self):
		with self.ctx:
			wins = gameService.getTeamWins(0, 0)
			assert wins == 0

	def test_getTeamWins(self):
		with self.ctx:
			match = matchService.create("singles")
			gameService.create(match.id, 1, None, None, None, None)
			gameService.create(match.id, 2, None, None, None, None)
			gameService.create(match.id, 3, None, None, None, None)

			team1 = teamService.create(match.id)
			team2 = teamService.create(match.id)

			gameService.complete(match.id, 1, team1.id, 21, team2.id, 8)
			gameService.complete(match.id, 2, team2.id, 21, team1.id, 5)
			gameService.complete(match.id, 3, team1.id, 21, team2.id, 19)

			assert gameService.getTeamWins(match.id, team1.id) == 2
			assert gameService.getTeamWins(match.id, team2.id) == 1
