from BaseTest import BaseTest
from pingpong.services.OfficeService import OfficeService
import uuid

officeService = OfficeService()

class TestOfficeController(BaseTest):

	def createOffice(self):
		with self.ctx:
			return officeService.create({
				"city": str(uuid.uuid4()),
				"state": str(uuid.uuid4()),
				"skypeChatId": str(uuid.uuid4())
			})

	def test_officesSelect(self):
		rv = self.app.get("/offices/select")
		assert rv.status == self.ok

	def test_officesSet(self):
		office = self.createOffice()
		rv = self.app.post("/offices", data = { "officeId": office.id }, follow_redirects = True)
		assert rv.status == self.ok

	def test_officesClear(self):
		rv = self.app.get("/offices/clear", follow_redirects = True)
		assert rv.status == self.ok

	def test_officesAuthenticated(self):
		self.office()
		self.authenticate()
		rv = self.app.get("/offices")
		assert rv.status == self.ok

	def test_officesAuthenticated(self):
		self.office()
		self.authenticate()
		rv = self.app.get("/offices")
		assert rv.status == self.ok

	def test_officesUnauthenticated(self):
		self.office()
		rv = self.app.get("/offices")
		assert rv.status == self.found

		rv = self.app.get("/offices/new")
		assert rv.status == self.found

		rv = self.app.post("/offices")
		assert rv.status == self.found

		rv = self.app.get("/offices/0/edit")
		assert rv.status == self.found

		rv = self.app.post("/offices/0")
		assert rv.status == self.found

		rv = self.app.post("/offices/0/enable")
		assert rv.status == self.found

		rv = self.app.post("/offices/0/disable")
		assert rv.status == self.found

		rv = self.app.post("/offices/0/delete")
		assert rv.status == self.found

	def test_officesNoSelectedOffice(self):
		rv = self.app.get("/offices")
		assert rv.status == self.found

	def test_officesNew(self):
		self.office()
		self.authenticate()
		rv = self.app.get("/offices/new")
		assert rv.status == self.ok

	def test_officesCreate(self):
		self.office()
		self.authenticate()
		rv = self.app.post("/offices", data = {
			"city": str(uuid.uuid4()),
			"state": str(uuid.uuid4()),
			"skypeChatId": str(uuid.uuid4())
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_officesCreateEmpty(self):
		self.office()
		self.authenticate()
		rv = self.app.post("/offices", data = {
			"city": "",
			"state": "",
			"skypeChatId": ""
		},)
		assert rv.status == self.badRequest

	def test_officesCreateNull(self):
		self.office()
		self.authenticate()
		rv = self.app.post("/offices", data = {})
		assert rv.status == self.badRequest

	def test_officesEdit(self):
		office = self.office()
		self.authenticate()
		with self.ctx:
			rv = self.app.get("/offices/{}/edit".format(office["id"]))
			assert rv.status == self.ok

	def test_officedEditNotFound(self):
		office = self.office()
		self.authenticate()
		with self.ctx:
			rv = self.app.get("/offices/{}/edit".format(0))
			assert rv.status == self.notFound

	def test_officesUpdate(self):
		office = self.office()
		self.authenticate()

		newCity = str(uuid.uuid4())
		newState = str(uuid.uuid4())
		newSkypeChatId = str(uuid.uuid4())

		with self.ctx:
			rv = self.app.post("/offices/{}".format(office["id"]), data = {
				"city": newCity,
				"state": newState,
				"skypeChatId": newSkypeChatId
			}, follow_redirects = True)

			updatedOffice = officeService.selectById(office["id"])

			assert rv.status == self.ok
			assert newCity == updatedOffice.city
			assert newState == updatedOffice.state
			assert newSkypeChatId == updatedOffice.skypeChatId

	def test_officesUpdateNotFound(self):
		self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/offices/{}".format(0), data = {})
			assert rv.status == self.notFound

	def test_isms_update_empty(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/offices/{}".format(office["id"]), data = {
				"city": "",
				"state": "",
				"skypeChatId": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_officesUpdateNull(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/offices/{}".format(office["id"]), data = {}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_officeEnable(self):
		self.office()
		self.authenticate()

		with self.ctx:
			self.authenticate()

			office = self.createOffice()
			officeService.disable(office)
			assert not office.isEnabled()

			rv = self.app.post("/offices/{}/enable".format(office.id), follow_redirects = True)
			assert rv.status == self.ok
			assert office.isEnabled()

	def test_officeEnableNotFound(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/offices/{}/enable".format(0))
			assert rv.status == self.notFound

	def test_officesDisable(self):
		self.office()
		self.authenticate()

		with self.ctx:
			office = self.createOffice()
			assert office.isEnabled()

			rv = self.app.post("/offices/{}/disable".format(office.id), follow_redirects = True)
			assert rv.status == self.ok
			assert not office.isEnabled()

	def test_officesDisableNotFound(self):
		office = self.office()
		self.authenticate()

		with self.ctx:
			rv = self.app.post("/offices/{}/disable".format(0))
			assert rv.status == self.notFound

	def test_officesDelete(self):
		self.office()
		self.authenticate()

		with self.ctx:
			originalCount = officeService.select().count()

			office = self.createOffice()

			createdCount = officeService.select().count()
			assert createdCount == originalCount + 1

			rv = self.app.post("/offices/{}/delete".format(office.id), follow_redirects = True)
			assert rv.status == self.ok

			deletedCount = officeService.select().count()
			assert originalCount == deletedCount

	def test_officesDeleteNotFound(self):
		self.office()
		self.authenticate()

		with self.ctx:
			self.authenticate()
			rv = self.app.post("/offices/{}/delete".format(0))
			assert rv.status == self.notFound
