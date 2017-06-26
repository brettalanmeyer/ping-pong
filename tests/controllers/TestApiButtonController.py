from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.MatchService import MatchService
import json

singles = Singles()
doubles = Doubles()
nines = Nines()
matchService = MatchService()
playerService = PlayerService()

class TestApiButtonController(BaseTest):

	def createSingles(self, officeId):
		with self.request:
			player1 = playerService.create(officeId, { "name": "Han" })
			player2 = playerService.create(officeId, { "name": "Chewie" })

			match = matchService.create(officeId, "singles")
			matchService.updateGames(match.id, 1)
			matchService.updatePlayTo(match.id, 21)

			singles.createTeams(match, [player1.id, player2.id], True)
			singles.play(match)

			return match

	def createDoubles(self, officeId):
		with self.request:
			player1 = playerService.create(officeId, { "name": "Han" })
			player2 = playerService.create(officeId, { "name": "Chewie" })
			player3 = playerService.create(officeId, { "name": "Luke" })
			player4 = playerService.create(officeId, { "name": "Leia" })

			match = matchService.create(officeId, "doubles")
			matchService.updateGames(match.id, 1)
			matchService.updatePlayTo(match.id, 21)

			doubles.createTeams(match, [player1.id, player2.id, player3.id, player4.id], True)
			doubles.play(match)

			return match

	def createNines(self, officeId):
		with self.request:
			player1 = playerService.create(officeId, { "name": "Han" })
			player2 = playerService.create(officeId, { "name": "Chewie" })
			player3 = playerService.create(officeId, { "name": "Luke" })
			player4 = playerService.create(officeId, { "name": "Leia" })

			match = matchService.create(officeId, "nines")
			nines.createTeams(match, [player1.id, player2.id, player3.id, player4.id], True)
			nines.play(match)

			return match

	def test_buttons_score(self):
		office = self.office()
		match = self.createSingles(office["id"])

		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/score".format(color), data = { "key": office["key"] })
			assert rv.status == self.ok
			data = json.loads(rv.data)
			assert data["button"] == color

	def test_buttons_undo(self):
		office = self.office()
		match = self.createSingles(office["id"])

		for color in matchService.colors:
			rv = self.app.post("/api/buttons/{}/undo".format(color), data = { "key": office["key"] })
			assert rv.status == self.ok
			data = json.loads(rv.data)
			assert data["button"] == color

	def test_buttons_score_invalid(self):
		office = self.office()
		rv = self.app.post("/api/buttons/black/score", data = { "key": office["key"] })
		assert rv.status == self.badRequest

	def test_buttons_undo_invalid(self):
		office = self.office()
		rv = self.app.post("/api/buttons/black/undo", data = { "key": office["key"] })
		assert rv.status == self.badRequest

	def test_buttons_score_singles(self):
		office = self.office()
		match = self.createSingles(office["id"])

		with self.ctx:
			for i in range(0,21):
				rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete

			rv = self.app.post("/api/buttons/green/score")
			assert rv.status == self.ok

	def test_buttons_score_singles(self):
		office = self.office()
		match = self.createSingles(office["id"])

		with self.ctx:
			for i in range(0,21):
				rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete == 1

			rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
			assert rv.status == self.ok

	def test_buttons_score_doubles(self):
		office = self.office()
		match = self.createDoubles(office["id"])

		with self.ctx:
			for i in range(0,21):
				rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete

			rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
			assert rv.status == self.ok

	def test_buttons_score_nines(self):
		office = self.office()
		match = self.createNines(office["id"])

		with self.ctx:
			for i in range(0,9):
				rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
				assert rv.status == self.ok

				rv = self.app.post("/api/buttons/yellow/score", data = { "key": office["key"] })
				assert rv.status == self.ok

				rv = self.app.post("/api/buttons/red/score", data = { "key": office["key"] })
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete

			# starts a new game
			rv = self.app.post("/api/buttons/green/score", data = { "key": office["key"] })
			assert rv.status == self.ok

			activeMatch = matchService.selectActiveMatch(office["id"])
			assert activeMatch.ready == 1
			assert activeMatch.complete == 0
			assert activeMatch.id != match.id
