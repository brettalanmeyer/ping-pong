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

	def createMatch(self, officeId):
		with self.request:
			player1 = playerService.create(officeId, { "name": "Fry" })
			player2 = playerService.create(officeId, { "name": "Bender" })

			match = matchService.create(officeId, "singles")
			matchService.updateGames(match.id, 1)

			singles.createTeams(match, [player1.id, player2.id], True)
			singles.play(match)

			return match

	def createPlayer(self, officeId):
		return playerService.create(officeId, {
			"name": self.playerName
		})

	def test_players(self):
		self.office()
		rv = self.app.get("/players")
		assert rv.status == self.ok

	def test_playersNew(self):
		self.office()
		rv = self.app.get("/players/new")
		assert rv.status == self.ok

	def test_playersCreate(self):
		self.office()
		rv = self.app.post("/players", data = {
			"name": self.playerName
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_playersCreateMatch(self):
		office = self.office()
		match = self.createMatch(office["id"])

		rv = self.app.post("/players/matches/{}".format(match.id), data = {
			"name": str(uuid.uuid4())
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_playersCreateDuplicate(self):
		self.office()
		rv = self.app.post("/players", data = {
			"name": self.playerName
		}, follow_redirects = True)
		assert rv.status == self.badRequest

	def test_playersCreateEmpty(self):
		self.office()
		rv = self.app.post("/players", data = {
			"name": ""
		})
		assert rv.status == self.badRequest

	def test_playersEdit(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])

			rv = self.app.get("/players/{}/edit".format(player.id))
			assert rv.status == self.ok

	def test_playersEditDisabled(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			playerService.disable(player)

			rv = self.app.get("/players/{}/edit".format(player.id))
			assert rv.status == self.notFound

	def test_playersEditNotFound(self):
		self.office()
		with self.ctx:
			rv = self.app.get("/players/{}/edit".format(0))
			assert rv.status == self.notFound

	def test_playersUpdate(self):
		office = self.office()
		with self.ctx:
			newName = str(uuid.uuid4())
			player = self.createPlayer(office["id"])

			rv = self.app.post("/players/{}".format(player.id), data = {
				"name": newName
			}, follow_redirects = True)

			updatedPlayer = playerService.selectById(player.id)
			assert rv.status == self.ok
			assert newName == updatedPlayer.name

	def test_playersUpdateNotFound(self):
		self.office()
		with self.ctx:
			rv = self.app.post("/players/{}".format(0), data = {})
			assert rv.status == self.notFound

	def test_playersUpdateEmpty(self):
		office = self.office()
		with self.ctx:
			player = self.createPlayer(office["id"])
			rv = self.app.post("/players/{}".format(player.id), data = {
				"name": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_playersEnableUnauthenticated(self):
		self.office()
		rv = self.app.post("/players/{}/enable".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_playersDisableUnauthenticated(self):
		self.office()
		rv = self.app.post("/players/{}/disable".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_playersDeleteUnauthenticated(self):
		self.office()
		rv = self.app.post("/players/{}/delete".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_playersEnable(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			player = self.createPlayer(office["id"])
			playerService.disable(player)
			assert not player.enabled

			rv = self.app.post("/players/{}/enable".format(player.id), follow_redirects = True)
			assert rv.status == self.ok
			assert player.enabled

	def test_playersEnableNotFound(self):
		self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/players/{}/enable".format(0))
			assert rv.status == self.notFound

	def test_playersDisabled(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			player = self.createPlayer(office["id"])
			assert player.enabled

			rv = self.app.post("/players/{}/disable".format(player.id), follow_redirects = True)
			assert rv.status == self.ok
			assert not player.enabled

	def test_playersDisableNotFound(self):
		self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/players/{}/disable".format(0))
			assert rv.status == self.notFound

	def test_playersDelete(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			originalCount = playerService.select(office["id"]).count()

			player = self.createPlayer(office["id"])

			createdCount = playerService.select(office["id"]).count()
			assert createdCount == originalCount + 1

			rv = self.app.post("/players/{}/delete".format(player.id), follow_redirects = True)
			assert rv.status == self.ok

			deletedCount = playerService.select(office["id"]).count()
			assert originalCount == deletedCount

	def test_playersDeleteNotFound(self):
		self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/players/{}/delete".format(0))
			assert rv.status == self.notFound
