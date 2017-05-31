from BaseTest import BaseTest
from pingpong.services.OfficeService import OfficeService
import uuid

officeService = OfficeService()

class TestOfficeService(BaseTest):

	def createOffice(self):
		return officeService.create({
			"city": "Ames",
			"state": "Iowa",
			"skypeChatId": "123abc",
			"seasonYear": "2016",
			"seasonMonth": "1"
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
			assert office.seasonYear == ""
			assert office.seasonMonth == ""
			assert office.key != None
			assert office.skypeChatId == ""
			assert office.enabled == True
			assert office.createdAt == None
			assert office.modifiedAt == None

	def test_create(self):
		city = "ABCD"
		state = "EFGH"
		skypeChatId = "987654qwerasdf"
		seasonYear = 2015
		seasonMonth = 4

		with self.ctx:
			office = officeService.create({
				"city": city,
				"state": state,
				"skypeChatId": skypeChatId,
				"seasonYear": seasonYear,
				"seasonMonth": seasonMonth
			})

			assert office.id != None
			assert office.city == city
			assert office.state == state
			assert office.seasonYear == seasonYear
			assert office.seasonMonth == seasonMonth
			assert office.skypeChatId == skypeChatId

			anotherOffice = officeService.selectById(office.id)

			assert anotherOffice.id == office.id
			assert anotherOffice.city == city
			assert anotherOffice.state == state
			assert anotherOffice.seasonYear == seasonYear
			assert anotherOffice.seasonMonth == seasonMonth
			assert anotherOffice.skypeChatId == skypeChatId

	def test_update(self):
		city = str(uuid.uuid4())
		state = str(uuid.uuid4())
		skypeChatId = str(uuid.uuid4())
		seasonYear = 2015
		seasonMonth = 3

		with self.ctx:
			office = self.createOffice()
			oldCity = office.city
			oldState = office.state
			oldSeasonYear = office.seasonYear
			oldSeasonMonth = office.seasonMonth
			oldSkypeChatId = office.skypeChatId
			oldKey = office.key

			updatedOffice = officeService.update(office.id, {
				"city": city,
				"state": state,
				"skypeChatId": skypeChatId,
				"seasonYear": seasonYear,
				"seasonMonth": seasonMonth
			})

			assert updatedOffice.city == city
			assert updatedOffice.state == state
			assert updatedOffice.seasonYear == seasonYear
			assert updatedOffice.seasonMonth == seasonMonth
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
			offices = officeService.selectActive()
			loadedOffices = officeService.load()

			assert offices.count() == len(loadedOffices)

			assert offices[0].id == loadedOffices[0]["id"]
			assert offices[0].city == loadedOffices[0]["city"]
			assert offices[0].state == loadedOffices[0]["state"]
