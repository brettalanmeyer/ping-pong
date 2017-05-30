from BaseTest import BaseTest
from pingpong.services.OfficeService import OfficeService
import uuid

officeService = OfficeService()

class TestOfficeService(BaseTest):

	def createOffice(self):
		return officeService.create({
			"city": "Ames",
			"state": "Iowa",
			"skypeChatId": "123abc"
		})

	def test_select(self):
		with self.ctx:
			self.createOffice()

			offices = officeService.select()
			assert offices.count() > 0

	def test_selectById(self):
		with self.ctx:
			officeOne = officeService.select().first()
			officeTwo = officeService.selectById(officeOne.id)
			assert officeOne == officeTwo

	def test_new(self):
		with self.ctx:
			office = officeService.new()
			assert office.id == None
			assert office.city == ""
			assert office.state == ""
			assert office.key != None
			assert office.skypeChatId == ""
			assert office.enabled == True
			assert office.createdAt == None
			assert office.modifiedAt == None

	def test_create(self):
		city = "ABCD"
		state = "EFGH"
		skypeChatId = "987654qwerasdf"

		with self.ctx:
			office = officeService.create({
				"city": city,
				"state": state,
				"skypeChatId": skypeChatId
			})

			assert office.id != None
			assert office.city == city
			assert office.state == state
			assert office.skypeChatId == skypeChatId

			anotherOffice = officeService.selectById(office.id)

			assert anotherOffice.id == office.id
			assert anotherOffice.city == city
			assert anotherOffice.state == state
			assert anotherOffice.skypeChatId == skypeChatId

	def test_update(self):
		city = str(uuid.uuid4())
		state = str(uuid.uuid4())
		skypeChatId = str(uuid.uuid4())

		with self.ctx:
			office = self.createOffice()
			oldCity = office.city
			oldState = office.state
			oldSkypeChatId = office.skypeChatId
			oldKey = office.key

			updatedOffice = officeService.update(office.id, {
				"city": city,
				"state": state,
				"skypeChatId": skypeChatId
			})

			assert updatedOffice.city == city
			assert updatedOffice.state == state
			assert updatedOffice.skypeChatId == skypeChatId

			assert updatedOffice.city != oldCity
			assert updatedOffice.state != oldState
			assert updatedOffice.skypeChatId != oldSkypeChatId
			assert updatedOffice.key == oldKey

	def test_delete(self):
		with self.ctx:
			office = self.createOffice()

			officeService.delete(office)
			deletedOffice = officeService.selectById(office.id)
			assert deletedOffice == None

	def test_deleteById(self):
		with self.ctx:
			office = self.createOffice()

			officeService.deleteById(office.id)
			deletedOffice = officeService.selectById(office.id)
			assert deletedOffice == None

	def test_load(self):
		with self.ctx:
			office = self.createOffice()
			offices = officeService.select()
			loadedOffices = officeService.load()

			assert offices.count() == len(loadedOffices)

			assert offices[0].id == loadedOffices[0]["id"]
			assert offices[0].city == loadedOffices[0]["city"]
			assert offices[0].state == loadedOffices[0]["state"]
			assert offices[0].enabled == loadedOffices[0]["enabled"]
			assert offices[0].createdAt == loadedOffices[0]["createdAt"]
			assert offices[0].modifiedAt == loadedOffices[0]["modifiedAt"]
