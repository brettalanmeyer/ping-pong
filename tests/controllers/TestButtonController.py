from BaseTest import BaseTest
from pingpong.matchtypes.Singles import Singles
from pingpong.matchtypes.Doubles import Doubles
from pingpong.matchtypes.Nines import Nines
from pingpong.services.MatchService import MatchService
from pingpong.services.PlayerService import PlayerService
from pingpong.services.MatchService import MatchService

singles = Singles()
doubles = Doubles()
nines = Nines()
matchService = MatchService()
playerService = PlayerService()

class TestButtonController(BaseTest):

	def createSingles(self):
		with self.request:
			player1 = playerService.create({ "name": "Han" })
			player2 = playerService.create({ "name": "Chewie" })

			match = matchService.create("singles")
			matchService.updateGames(match.id, 1)

			singles.createTeams(match, [player1.id, player2.id], True)
			singles.play(match)

			return match

	def createDoubles(self):
		with self.request:
			player1 = playerService.create({ "name": "Han" })
			player2 = playerService.create({ "name": "Chewie" })
			player3 = playerService.create({ "name": "Luke" })
			player4 = playerService.create({ "name": "Leia" })

			match = matchService.create("doubles")
			matchService.updateGames(match.id, 1)

			doubles.createTeams(match, [player1.id, player2.id, player3.id, player4.id], True)
			doubles.play(match)

			return match

	def createNines(self):
		with self.request:
			player1 = playerService.create({ "name": "Han" })
			player2 = playerService.create({ "name": "Chewie" })
			player3 = playerService.create({ "name": "Luke" })
			player4 = playerService.create({ "name": "Leia" })

			match = matchService.create("nines")
			nines.createTeams(match, [player1.id, player2.id, player3.id, player4.id], True)
			nines.play(match)

			return match

	def test_buttons_score(self):
		match = self.createSingles()

		for color in matchService.colors:
			rv = self.app.post("/buttons/{}/score".format(color))
			assert rv.status == self.ok
			assert rv.data == color

	def test_buttons_undo(self):
		match = self.createSingles()

		for color in matchService.colors:
			rv = self.app.post("/buttons/{}/undo".format(color))
			assert rv.status == self.ok
			assert rv.data == color

	def test_buttons_score_invalid(self):
		rv = self.app.post("/buttons/black/score")
		assert rv.status == self.badRequest

	def test_buttons_undo_invalid(self):
		rv = self.app.post("/buttons/black/undo")
		assert rv.status == self.badRequest

	def test_buttons_score_singles(self):
		match = self.createSingles()

		with self.ctx:
			for i in range(0,21):
				rv = self.app.post("/buttons/green/score")
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete

			rv = self.app.post("/buttons/green/score")
			assert rv.status == self.ok

	def test_buttons_score_singles(self):
		match = self.createSingles()

		with self.ctx:
			for i in range(0,21):
				rv = self.app.post("/buttons/green/score")
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete == 1

			rv = self.app.post("/buttons/green/score")
			assert rv.status == self.ok

	def test_buttons_score_doubles(self):
		match = self.createDoubles()

		with self.ctx:
			for i in range(0,21):
				rv = self.app.post("/buttons/green/score")
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete

			rv = self.app.post("/buttons/green/score")
			assert rv.status == self.ok

	def test_buttons_score_nines(self):
		match = self.createNines()

		with self.ctx:
			for i in range(0,9):
				rv = self.app.post("/buttons/green/score")
				assert rv.status == self.ok

				rv = self.app.post("/buttons/yellow/score")
				assert rv.status == self.ok

				rv = self.app.post("/buttons/red/score")
				assert rv.status == self.ok

			updatedMatch = matchService.selectById(match.id)
			assert updatedMatch.complete

			# starts a new game
			rv = self.app.post("/buttons/green/score")
			assert rv.status == self.ok

			activeMatch = matchService.selectActiveMatch()
			assert activeMatch.ready == 1
			assert activeMatch.complete == 0
			assert activeMatch.id != match.id
