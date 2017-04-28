from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService
import uuid

playerService = PlayerService()

class TestPlayerService(BaseTest):

	def test_select(self):
		with self.ctx:
			playerService.create({
				"name": "Bob"
			})

			players = playerService.select()
			assert players.count() > 0

	def test_selectCount(self):
		with self.ctx:
			players = playerService.selectCount()
			assert players >= 0

	def test_selectById(self):
		with self.ctx:
			playerOne = playerService.select().first()
			playerTwo = playerService.selectById(playerOne.id)
			assert playerOne == playerTwo

	def test_selectActive(self):
		with self.ctx:
			players = playerService.selectActive()

			for player in players:
				assert player.enabled

	def test_selectByName(self):
		with self.ctx:
			players = playerService.selectByName("Bob")
			assert players.count() > 0

			for player in players:
				assert player.name == "Bob"

	def test_selectByNameExcludingPlayer(self):
		name = str(uuid.uuid4())

		with self.ctx:
			p1 = playerService.create({ "name": name })
			p2 = playerService.create({ "name": name })
			p3 = playerService.create({ "name": name })

			players = playerService.selectByNameExcludingPlayer(p1.id, name)

			assert players.count() == 2

			for player in players:
				assert player.name == name

	def test_new(self):
		with self.ctx:
			player = playerService.new()
			assert player.id == None
			assert player.name == ""
			assert player.enabled == True
			assert player.createdAt == None
			assert player.modifiedAt == None

	def test_create(self):
		name = "This is a name"

		with self.ctx:
			player = playerService.create({
				"name": name
			})

			assert player.id != None
			assert player.name == name

			anotherPlayer = playerService.selectById(player.id)

			assert anotherPlayer.id == player.id
			assert anotherPlayer.name == name

	def test_update(self):
		name = str(uuid.uuid4())

		with self.ctx:
			player = playerService.select().first()
			oldName = player.name

			updatedPlayer = playerService.update(player.id, {
				"name": name
			})

			assert updatedPlayer.name == name
			assert updatedPlayer.name != oldName

	def test_delete(self):
		with self.ctx:
			player = playerService.create({ "name": "Bob" })
			playerService.delete(player)
			deletedPlayer = playerService.selectById(player.id)
			assert deletedPlayer == None

	def test_deleteById(self):
		with self.ctx:
			player = playerService.create({ "name": "Bob" })
			playerService.deleteById(player.id)
			deletedPlayer = playerService.selectById(player.id)
			assert deletedPlayer == None
