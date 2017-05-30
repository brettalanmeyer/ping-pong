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

	def test_isms_json(self):
		self.office()
		rv = self.app.get("/isms.json")
		assert rv.status == self.ok

	def test_isms_new(self):
		self.office()
		rv = self.app.get("/isms/new")
		assert rv.status == self.ok

	def test_isms_create(self):
		self.office()
		rv = self.app.post("/isms", data = {
			"saying": "A New Saying",
			"left": 9,
			"right": 11
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_isms_create_empty(self):
		self.office()
		rv = self.app.post("/isms", data = {
			"saying": "",
			"left": "",
			"right": ""
		})
		assert rv.status == self.badRequest

	def test_isms_create_null(self):
		self.office()
		rv = self.app.post("/isms", data = {})
		assert rv.status == self.badRequest

	def test_isms_edit(self):
		office = self.office()
		with self.ctx:
			ism = ismService.select(office["id"]).first()

			rv = self.app.get("/isms/{}/edit".format(ism.id))
			assert rv.status == self.ok

	def test_isms_edit_not_found(self):
		self.office()
		with self.ctx:
			rv = self.app.get("/isms/{}/edit".format(0))
			assert rv.status == self.notFound

	def test_isms_update(self):
		office = self.office()
		newSaying = "Another Saying"
		newLeft = 4
		newRight = 342

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

	def test_isms_update_not_found(self):
		self.office()
		with self.ctx:
			rv = self.app.post("/isms/{}".format(0), data = {})
			assert rv.status == self.notFound

	def test_isms_update_empty(self):
		office = self.office()
		with self.ctx:
			ism = ismService.select(office["id"]).first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {
				"saying": "",
				"left": "",
				"right": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_isms_update_null(self):
		office = self.office()
		with self.ctx:
			ism = ismService.select(office["id"]).first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_isms_approve_unauthenticated(self):
		self.office()
		rv = self.app.post("/isms/{}/approve".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_isms_reject_unauthenticated(self):
		self.office()
		rv = self.app.post("/isms/{}/reject".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_isms_delete_unauthenticated(self):
		self.office()
		rv = self.app.post("/isms/{}/delete".format(0), follow_redirects = False)
		assert rv.status == self.found

	def test_isms_approve(self):
		office = self.office()
		with self.ctx:
			self.authenticate()

			ism = self.create_ism(office["id"])
			ismService.reject(ism)
			assert not ism.isApproved()

			rv = self.app.post("/isms/{}/approve".format(ism.id), follow_redirects = True)
			assert rv.status == self.ok
			assert ism.isApproved()

	def test_isms_approve_not_found(self):
		self.office()
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/isms/{}/approve".format(0))
			assert rv.status == self.notFound

	def test_isms_reject(self):
		office = self.office()
		with self.ctx:
			self.authenticate()

			ism = self.create_ism(office["id"])
			assert ism.isApproved()

			rv = self.app.post("/isms/{}/reject".format(ism.id), follow_redirects = True)
			assert rv.status == self.ok
			assert not ism.isApproved()

	def test_isms_reject_not_found(self):
		self.office()
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/isms/{}/reject".format(0))
			assert rv.status == self.notFound

	def test_isms_delete(self):
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

	def test_isms_delete_not_found(self):
		self.office()
		with self.ctx:
			self.authenticate()
			rv = self.app.post("/isms/{}/delete".format(0))
			assert rv.status == self.notFound
