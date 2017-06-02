from BaseTest import BaseTest
from pingpong.services.PlayerService import PlayerService
import uuid

playerService = PlayerService()

class TestPlayerService(BaseTest):

	def test_select(self):
		office = self.office()

		with self.ctx:
			playerService.create(office["id"], {
				"name": "Bob"
			})

			players = playerService.select(office["id"])
			assert players.count() > 0

	def test_selectCount(self):
		office = self.office()

		with self.ctx:
			players = playerService.selectCount(office["id"])
			assert players >= 0

	def test_selectById(self):
		office = self.office()

		with self.ctx:
			playerOne = playerService.select(office["id"]).first()
			playerTwo = playerService.selectById(playerOne.id)
			assert playerOne == playerTwo

	def test_selectActive(self):
		office = self.office()

		with self.ctx:
			players = playerService.selectActive(office["id"])

			for player in players:
				assert player.enabled

	def test_selectByName(self):
		office = self.office()

		with self.ctx:
			players = playerService.selectByName(office["id"], "Bob")
			assert players.count() > 0

			for player in players:
				assert player.name == "Bob"

	def test_selectByNameExcludingPlayer(self):
		office = self.office()
		name = str(uuid.uuid4())

		with self.ctx:
			p1 = playerService.create(office["id"], { "name": name })
			p2 = playerService.create(office["id"], { "name": name })
			p3 = playerService.create(office["id"], { "name": name })

			players = playerService.selectByNameExcludingPlayer(office["id"], p1.id, name)

			assert players.count() == 2

			for player in players:
				assert player.name == name

	def test_new(self):
		with self.ctx:
			player = playerService.new()
			assert player.id == None
			assert player.officeId == None
			assert player.name == ""
			assert player.enabled == True
			assert player.createdAt == None
			assert player.modifiedAt == None

	def test_create(self):
		office = self.office()

		name = "This is a name"

		with self.ctx:
			player = playerService.create(office["id"], {
				"name": name
			})

			assert player.id != None
			assert player.name == name

			anotherPlayer = playerService.selectById(player.id)

			assert anotherPlayer.id == player.id
			assert anotherPlayer.name == name

	def test_update(self):
		office = self.office()
		name = str(uuid.uuid4())

		with self.ctx:
			player = playerService.select(office["id"]).first()
			oldName = player.name

			updatedPlayer = playerService.update(player.id, {
				"name": name
			})

			assert updatedPlayer.name == name
			assert updatedPlayer.name != oldName

	def test_delete(self):
		office = self.office()

		with self.ctx:
			player = playerService.create(office["id"], { "name": "Bob" })
			playerService.delete(player)
			deletedPlayer = playerService.selectById(player.id)
			assert deletedPlayer == None

	def test_deleteById(self):
		office = self.office()

		with self.ctx:
			player = playerService.create(office["id"], { "name": "Bob" })
			playerService.deleteById(player.id)
			deletedPlayer = playerService.selectById(player.id)
			assert deletedPlayer == None
