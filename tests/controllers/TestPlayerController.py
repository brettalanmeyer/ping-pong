from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService
import uuid

playerService = PlayerService()

class TestPlayerController(BaseTest):

	playerName = str(uuid.uuid4())

	def create_player(self):
		return playerService.create({
			"name": self.playerName
		})

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

	def test_players_edit_not_found(self):
		with self.ctx:
			rv = self.app.get("/players/{}/edit".format(0))
			assert rv.status == self.notFound

	def test_players_update(self):
		with self.ctx:
			newName = str(uuid.uuid4())
			player = self.create_player()

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

	def test_players_enable_unauthenticated(self):
		rv = self.app.post("/players/{}/enable".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_players_disable_unauthenticated(self):
		rv = self.app.post("/players/{}/disable".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_players_delete_unauthenticated(self):
		rv = self.app.post("/players/{}/delete".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_players_enable(self):
		with self.ctx:
			self.authenticate()

			player = self.create_player()
			playerService.disable(player)
			assert not player.enabled

			rv = self.app.post("/players/{}/enable".format(player.id), follow_redirects = True)
			assert rv.status == self.ok
			assert player.enabled

	def test_players_disabled(self):
		with self.ctx:
			self.authenticate()

			player = self.create_player()
			assert player.enabled

			rv = self.app.post("/players/{}/disable".format(player.id), follow_redirects = True)
			assert rv.status == self.ok
			assert not player.enabled

	def test_players_delete(self):
		with self.ctx:
			self.authenticate()

			originalCount = playerService.select().count()

			player = self.create_player()

			createdCount = playerService.select().count()
			assert createdCount == originalCount + 1

			rv = self.app.post("/players/{}/delete".format(player.id), follow_redirects = True)
			assert rv.status == self.ok

			deletedCount = playerService.select().count()
			assert originalCount == deletedCount