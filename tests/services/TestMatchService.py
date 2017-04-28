from BaseTest import BaseTest
from datetime import datetime
from pingpong.services.MatchService import MatchService

matchService = MatchService()

class TestMatchService(BaseTest):

	def createMatch(self):
		return matchService.create("singles")

	def test_select(self):
		with self.ctx:
			self.createMatch()
			matches = matchService.select()
			assert matches.count() > 0

	def test_selectCount(self):
		with self.ctx:
			self.createMatch()
			matches = matchService.selectCount()
			assert matches > 0

	def test_selectById(self):
		with self.ctx:
			match1 = self.createMatch()
			match2 = matchService.selectById(match1.id)
			assert match1 == match2

	def test_selectByIdNotExists(self):
		with self.ctx:
			match = matchService.selectById(0)
			assert match == None

	def test_selectNotById(self):
		with self.ctx:
			match = self.createMatch()
			matches = matchService.selectNotById(match.id)

			for item in matches:
				assert item.id != match.id

	def test_selectComplete(self):
		with self.ctx:
			matches = matchService.selectComplete()

			for match in matches:
				assert match.complete

	def test_selectCompleteOrReady(self):
		with self.ctx:
			matches = matchService.selectCompleteOrReady()

			for match in matches:
				assert match.complete or match.ready

	def test_selectActiveMatch(self):
		with self.ctx:
			match = matchService.selectActiveMatch()

			if match != None:
				assert match.ready and not match.complete

	def test_selectLatestMatch(self):
		with self.ctx:
			match = matchService.selectLatestMatch()

			if match != None:
				assert match.complete

	def test_create(self):
		with self.ctx:
			singles = matchService.create("singles")
			assert singles.matchType == "singles"
			assert singles.playTo == 21
			assert singles.game == 0
			assert not singles.ready
			assert not singles.complete

			doubles = matchService.create("doubles")
			assert doubles.matchType == "doubles"
			assert doubles.playTo == 21
			assert doubles.game == 0
			assert not doubles.ready
			assert not doubles.complete

			nines = matchService.create("nines")
			assert nines.matchType == "nines"
			assert nines.playTo == 9
			assert nines.game == 0
			assert not nines.ready
			assert not nines.complete

	def test_updateGames(self):
		with self.ctx:
			match = self.createMatch()
			assert match.numOfGames == None

			matchService.updateGames(match.id, 5)
			assert match.numOfGames == 5

	def test_updateGame(self):
		with self.ctx:
			match = self.createMatch()
			assert match.game == 0

			matchService.updateGame(match.id, 3)
			assert match.game == 3

	def test_play(self):
		with self.ctx:
			match1 = self.createMatch()

			match2 = self.createMatch()
			match2.ready = True

			match3 = self.createMatch()
			match3.ready = True

			assert not match1.ready
			assert match2.ready
			assert match3.ready

			matchService.play(match1)

			assert match1.ready
			assert not match2.ready
			assert not match3.ready

	def test_incomplete(self):
		with self.ctx:
			match = self.createMatch()
			match.complete = True
			match.completedAt = datetime.now()

			assert match.complete
			assert match.completedAt != None

			matchService.incomplete(match)

			assert not match.complete
			assert match.completedAt == None

	def test_complete(self):
		with self.ctx:
			match = self.createMatch()

			assert not match.complete
			assert match.completedAt == None

			matchService.complete(match)

			assert match.complete
			assert match.completedAt != None

	def test_deleteById(self):
		with self.ctx:
			match = self.createMatch()
			matchService.deleteById(match.id)
			assert matchService.selectById(match.id) == None

	def test_delete(self):
		with self.ctx:
			match = self.createMatch()
			matchService.delete(match)
			assert matchService.selectById(match.id) == None

	def test_deleteAll(self):
		with self.ctx:
			matchService.deleteAll()
			assert matchService.selectCount() == 0
