from BaseTest import BaseTest
from datetime import datetime
from pingpong.services.MatchService import MatchService

matchService = MatchService()

class TestMatchService(BaseTest):

	def createMatch(self, officeId):
		return matchService.create(officeId, "singles")

	def test_select(self):
		office = self.office()

		with self.ctx:
			self.createMatch(office["id"])
			matches = matchService.select(office["id"])
			assert matches.count() > 0

	def test_selectCount(self):
		office = self.office()

		with self.ctx:
			self.createMatch(office["id"])
			matches = matchService.selectCount(office["id"])
			assert matches > 0

	def test_selectById(self):
		office = self.office()

		with self.ctx:
			match1 = self.createMatch(office["id"])
			match2 = matchService.selectById(match1.id)
			assert match1 == match2

	def test_selectByIdNotExists(self):
		with self.ctx:
			match = matchService.selectById(0)
			assert match == None

	def test_selectNotById(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			matches = matchService.selectNotById(office["id"], match.id)

			for item in matches:
				assert item.id != match.id

	def test_selectComplete(self):
		office = self.office()

		with self.ctx:
			matches = matchService.selectComplete(office["id"])

			for match in matches:
				assert match.complete

	def test_selectCompleteOrReady(self):
		office = self.office()

		with self.ctx:
			matches = matchService.selectCompleteOrReady(office["id"])

			for match in matches:
				assert match.complete or match.ready

	def test_selectActiveMatch(self):
		office = self.office()

		with self.ctx:
			match = matchService.selectActiveMatch(office["id"])

			if match != None:
				assert match.ready and not match.complete

	def test_selectLatestMatch(self):
		office = self.office()

		with self.ctx:
			match = matchService.selectLatestMatch(office["id"])

			if match != None:
				assert match.complete

	def test_create(self):
		office = self.office()

		with self.ctx:
			singles = matchService.create(office["id"], "singles")
			assert singles.matchType == "singles"
			assert singles.playTo == 21
			assert singles.game == 0
			assert not singles.ready
			assert not singles.complete

			doubles = matchService.create(office["id"], "doubles")
			assert doubles.matchType == "doubles"
			assert doubles.playTo == 21
			assert doubles.game == 0
			assert not doubles.ready
			assert not doubles.complete

			nines = matchService.create(office["id"], "nines")
			assert nines.matchType == "nines"
			assert nines.playTo == 9
			assert nines.game == 0
			assert not nines.ready
			assert not nines.complete

	def test_updateGames(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			assert match.numOfGames == None

			matchService.updateGames(match.id, 5)
			assert match.numOfGames == 5

	def test_updateGame(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			assert match.game == 0

			matchService.updateGame(match.id, 3)
			assert match.game == 3

	def test_play(self):
		office = self.office()

		with self.ctx:
			match1 = self.createMatch(office["id"])

			match2 = self.createMatch(office["id"])
			match2.ready = True

			match3 = self.createMatch(office["id"])
			match3.ready = True

			assert not match1.ready
			assert match2.ready
			assert match3.ready

			matchService.play(match1)

			assert match1.ready
			assert not match2.ready
			assert not match3.ready

	def test_incomplete(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			match.complete = True
			match.completedAt = datetime.now()

			assert match.complete
			assert match.completedAt != None

			matchService.incomplete(match)

			assert not match.complete
			assert match.completedAt == None

	def test_complete(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])

			assert not match.complete
			assert match.completedAt == None

			matchService.complete(match)

			assert match.complete
			assert match.completedAt != None

	def test_deleteById(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			matchService.deleteById(match.id)
			assert matchService.selectById(match.id) == None

	def test_delete(self):
		office = self.office()

		with self.ctx:
			match = self.createMatch(office["id"])
			matchService.delete(match)
			assert matchService.selectById(match.id) == None

	def test_deleteAll(self):
		office = self.office()

		with self.ctx:
			matchService.deleteAll()
			assert matchService.selectCount(office["id"]) == 0
