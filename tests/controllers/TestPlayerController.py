from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
import uuid

matchService = MatchService()
playerService = PlayerService()
singles = Singles()

class TestPlayerController(BaseTest):

	playerName = str(uuid.uuid4())

	def createMatch(self):
		with self.request:
			player1 = playerService.create({ "name": "Fry" })
			player2 = playerService.create({ "name": "Bender" })

			match = matchService.create("singles")
			matchService.updateGames(match.id, 1)

			singles.createTeams(match, [player1.id, player2.id], True)
			singles.play(match)

			return match

	def createPlayer(self):
		return playerService.create({
			"name": self.playerName
		})

	def test_players(self):
		rv = self.app.get("/players")
		assert rv.status == self.ok

	def test_playersNew(self):
		rv = self.app.get("/players/new")
		assert rv.status == self.ok

	def test_playersCreate(self):
		rv = self.app.post("/players", data = {
			"name": self.playerName
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_playersCreateMatch(self):
		match = self.createMatch()

		rv = self.app.post("/players/matches/{}".format(match.id), data = {
			"name": str(uuid.uuid4())
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_playersCreateDuplicate(self):
		rv = self.app.post("/players", data = {
			"name": self.playerName
		}, follow_redirects = True)
		assert rv.status == self.badRequest

	def test_playersCreateEmpty(self):
		rv = self.app.post("/players", data = {
			"name": ""
		})
		assert rv.status == self.badRequest

	def test_playersEdit(self):
		with self.ctx:
			player = self.createPlayer()

			rv = self.app.get("/players/{}/edit".format(player.id))
			assert rv.status == self.ok

	def test_playersEditDisabled(self):
		with self.ctx:
			player = self.createPlayer()
			playerService.disable(player)

			rv = self.app.get("/players/{}/edit".format(player.id))
			assert rv.status == self.notFound

	def test_playersEditNotFound(self):
		with self.ctx:
			rv = self.app.get("/players/{}/edit".format(0))
			assert rv.status == self.notFound

	def test_playersUpdate(self):
		with self.ctx:
			newName = str(uuid.uuid4())
			player = self.createPlayer()

			rv = self.app.post("/players/{}".format(player.id), data = {
				"name": newName
			}, follow_redirects = True)

			updatedPlayer = playerService.selectById(player.id)
			assert rv.status == self.ok
			assert newName == updatedPlayer.name

	def test_playersUpdateNotFound(self):
		with self.ctx:
			rv = self.app.post("/players/{}".format(0), data = {})
			assert rv.status == self.notFound

	def test_playersUpdateEmpty(self):
		with self.ctx:
			player = self.createPlayer()
			rv = self.app.post("/players/{}".format(player.id), data = {
				"name": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_playersEnableUnauthenticated(self):
		rv = self.app.post("/players/{}/enable".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_playersDisableUnauthenticated(self):
		rv = self.app.post("/players/{}/disable".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_playersDeleteUnauthenticated(self):
		rv = self.app.post("/players/{}/delete".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_playersEnable(self):
		with self.ctx:
			self.authenticate()

			player = self.createPlayer()
			playerService.disable(player)
			assert not player.enabled

			rv = self.app.post("/players/{}/enable".format(player.id), follow_redirects = True)
			assert rv.status == self.ok
			assert player.enabled

	def test_playersEnableNotFound(self):
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/players/{}/enable".format(0))
			assert rv.status == self.notFound

	def test_playersDisabled(self):
		with self.ctx:
			self.authenticate()

			player = self.createPlayer()
			assert player.enabled

			rv = self.app.post("/players/{}/disable".format(player.id), follow_redirects = True)
			assert rv.status == self.ok
			assert not player.enabled

	def test_playersDisableNotFound(self):
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/players/{}/disable".format(0))
			assert rv.status == self.notFound

	def test_playersDelete(self):
		with self.ctx:
			self.authenticate()

			originalCount = playerService.select().count()

			player = self.createPlayer()

			createdCount = playerService.select().count()
			assert createdCount == originalCount + 1

			rv = self.app.post("/players/{}/delete".format(player.id), follow_redirects = True)
			assert rv.status == self.ok

			deletedCount = playerService.select().count()
			assert originalCount == deletedCount

	def test_playersDeleteNotFound(self):
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/players/{}/delete".format(0))
			assert rv.status == self.notFound
