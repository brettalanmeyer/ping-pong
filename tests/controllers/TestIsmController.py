from BaseTest import BaseTest
from pingpong.services.IsmService import IsmService

ismService = IsmService()

class TestIsmController(BaseTest):

	def create_ism(self, officeId):
		return ismService.create(officeId, {
			"saying": "A new ism",
			"left": 1,
			"right": 2
		})

	def test_isms(self):
		self.office()
		rv = self.app.get("/isms")
		assert rv.status == self.ok

	def test_ismsJson(self):
		self.office()
		rv = self.app.get("/isms.json")
		assert rv.status == self.ok

	def test_ismsNew(self):
		self.office()
		rv = self.app.get("/isms/new")
		assert rv.status == self.ok

	def test_ismsCreate(self):
		self.office()
		rv = self.app.post("/isms", data = {
			"saying": "A New Saying",
			"left": 9,
			"right": 11
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_ismsCreateEmpty(self):
		self.office()
		rv = self.app.post("/isms", data = {
			"saying": "",
			"left": "",
			"right": ""
		})
		assert rv.status == self.badRequest

	def test_ismsCreateNull(self):
		self.office()
		rv = self.app.post("/isms", data = {})
		assert rv.status == self.badRequest

	def test_ismsEdit(self):
		office = self.office()
		with self.ctx:
			ism = ismService.select(office["id"]).first()

			rv = self.app.get("/isms/{}/edit".format(ism.id))
			assert rv.status == self.ok

	def test_ismsEditNotFound(self):
		self.office()
		with self.ctx:
			rv = self.app.get("/isms/{}/edit".format(0))
			assert rv.status == self.notFound

	def test_ismsUpdate(self):
		office = self.office()
		newSaying = "Another Saying"
		newLeft = 4
		newRight = 42

		with self.ctx:
			ism = ismService.select(office["id"]).first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {
				"saying": newSaying,
				"left": newLeft,
				"right": newRight
			}, follow_redirects = True)

			updatedIsm = ismService.selectById(ism.id)

			assert rv.status == self.ok
			assert newSaying == updatedIsm.saying
			assert newLeft == updatedIsm.left
			assert newRight == updatedIsm.right

	def test_ismsUpdateNotFound(self):
		self.office()
		with self.ctx:
			rv = self.app.post("/isms/{}".format(0), data = {})
			assert rv.status == self.notFound

	def test_ismsUpdateEmpty(self):
		office = self.office()
		with self.ctx:
			ism = ismService.select(office["id"]).first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {
				"saying": "",
				"left": "",
				"right": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_ismsUpdateNull(self):
		office = self.office()
		with self.ctx:
			ism = ismService.select(office["id"]).first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_ismsApproveUnauthenticated(self):
		self.office()
		rv = self.app.post("/isms/{}/approve".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_ismsRejectUnauthenticated(self):
		self.office()
		rv = self.app.post("/isms/{}/reject".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_ismsDeleteUnauthenticated(self):
		self.office()
		rv = self.app.post("/isms/{}/delete".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_ismsApprove(self):
		office = self.office()
		with self.ctx:
			self.authenticate()

			ism = self.create_ism(office["id"])
			ismService.reject(ism)
			assert not ism.isApproved()

			rv = self.app.post("/isms/{}/approve".format(ism.id), follow_redirects = True)
			assert rv.status == self.ok
			assert ism.isApproved()

	def test_ismsApproveNotFound(self):
		self.office()
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/isms/{}/approve".format(0))
			assert rv.status == self.notFound

	def test_ismsReject(self):
		office = self.office()
		with self.ctx:
			self.authenticate()

			ism = self.create_ism(office["id"])
			assert ism.isApproved()

			rv = self.app.post("/isms/{}/reject".format(ism.id), follow_redirects = True)
			assert rv.status == self.ok
			assert not ism.isApproved()

	def test_ismsRejectNotFound(self):
		self.office()
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/isms/{}/reject".format(0))
			assert rv.status == self.notFound

	def test_ismsDelete(self):
		office = self.office()
		with self.ctx:
			self.authenticate()

			originalCount = ismService.select(office["id"]).count()

			ism = self.create_ism(office["id"])

			createdCount = ismService.select(office["id"]).count()
			assert createdCount == originalCount + 1

			rv = self.app.post("/isms/{}/delete".format(ism.id), follow_redirects = True)
			assert rv.status == self.ok

			deletedCount = ismService.select(office["id"]).count()
			assert originalCount == deletedCount

	def test_ismsDeleteNotFound(self):
		self.office()
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/isms/{}/delete".format(0))
			assert rv.status == self.notFound
