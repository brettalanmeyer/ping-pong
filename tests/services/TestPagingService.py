from BaseTest import BaseTest
from pingpong.services.PagingService import PagingService
from pingpong.services.PlayerService import PlayerService
import uuid

playerService = PlayerService()

class TestPagingService(BaseTest):

	def test_defaultLimit(self):
		pagingService = PagingService()
		assert pagingService.limit == 20

	def test_limit(self):
		pagingService = PagingService(17)
		assert pagingService.limit == 17

	def test_pagerSmall(self):
		office = self.office()

		with self.ctx:
			pagingService = PagingService(2)

			name = "Player {}".format(str(uuid.uuid4()))
			for i in range(0, 10):
				playerService.create(office["id"], { "name": name })

			players = playerService.selectByName(office["id"], name)

			pagePlayers = pagingService.pager(players, 1)

			assert len(pagePlayers) == 2
			assert pagingService.total == 10
			assert pagingService.page == 1
			assert pagingService.limit == 2
			assert pagingService.pages == 5

	def test_pagerLarge(self):
		office = self.office()

		with self.ctx:
			pagingService = PagingService(12)

			name = "Player {}".format(str(uuid.uuid4()))
			for i in range(0, 77):
				playerService.create(office["id"], { "name": name })

			players = playerService.selectByName(office["id"], name)

			pagePlayers = pagingService.pager(players, 2)

			assert len(pagePlayers) == 12
			assert pagingService.total == 77
			assert pagingService.page == 2
			assert pagingService.limit == 12
			assert pagingService.pages == 7

	def test_data(self):
		pagingService = PagingService()
		data = pagingService.data()
		assert data["total"] == pagingService.total
		assert data["page"] == pagingService.page
		assert data["limit"] == pagingService.limit
		assert data["pages"] == pagingService.pages
