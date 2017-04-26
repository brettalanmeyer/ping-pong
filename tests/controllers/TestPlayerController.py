from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService
import uuid

playerService = PlayerService()

class TestPlayerController(BaseTest):

	playerName = str(uuid.uuid4())

	def test_players(self):
		rv = self.app.get("/players")
		assert rv.status == self.ok

	def test_players_new(self):
		rv = self.app.get("/players/new")
		assert rv.status == self.ok

	def test_players_create(self):
		rv = self.app.post("/players", data = {
			"name": self.playerName
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_players_create_duplicate(self):
		rv = self.app.post("/players", data = {
			"name": self.playerName
		}, follow_redirects = True)
		assert rv.status == self.badRequest

	def test_players_create_empty(self):
		rv = self.app.post("/players", data = {
			"name": ""
		})
		assert rv.status == self.badRequest

	def test_players_edit(self):
		with self.ctx:
			player = playerService.select().first()

			rv = self.app.get("/players/{}/edit".format(player.id))
			assert rv.status == self.ok

	def test_players_update(self):
		with self.ctx:
			newName = str(uuid.uuid4())
			player = playerService.select().first()
			rv = self.app.post("/players/{}".format(player.id), data = {
				"name": newName
			}, follow_redirects = True)

			updatedPlayer = playerService.selectById(player.id)
			assert rv.status == self.ok
			assert newName == updatedPlayer.name

	def test_players_update_empty(self):
		with self.ctx:
			player = playerService.select().first()
			rv = self.app.post("/players/{}".format(player.id), data = {
				"name": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest
