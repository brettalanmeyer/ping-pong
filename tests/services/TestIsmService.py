from BaseTest import BaseTest
from pingpong.services.IsmService import IsmService
import uuid

ismService = IsmService()

class TestIsmService(BaseTest):

	def test_select(self):
		with self.ctx:
			ismService.create({
				"saying": "saying",
				"left": 1,
				"right": 1
			})

			isms = ismService.select()
			assert isms.count() > 0

	def test_selectById(self):
		with self.ctx:
			ismOne = ismService.select().first()
			ismTwo = ismService.selectById(ismOne.id)
			assert ismOne == ismTwo

	def test_new(self):
		with self.ctx:
			ism = ismService.new()
			assert ism.id == None
			assert ism.left == 0
			assert ism.right == 0
			assert ism.saying == ""
			assert ism.approved == False
			assert ism.createdAt == None
			assert ism.modifiedAt == None

	def test_create(self):
		saying = "This is a saying"
		left = 231
		right = 631

		with self.ctx:
			ism = ismService.create({
				"saying": saying,
				"left": left,
				"right": right
			})

			assert ism.id != None
			assert ism.saying == saying
			assert ism.left == left
			assert ism.right == right

			anotherIsm = ismService.selectById(ism.id)

			assert anotherIsm.id == ism.id
			assert anotherIsm.saying == saying
			assert anotherIsm.left == left
			assert anotherIsm.right == right

	def test_update(self):
		saying = str(uuid.uuid4())
		left = 71
		right = 32

		with self.ctx:
			ism = ismService.select().first()
			oldSaying = ism.saying

			updatedIsm = ismService.update(ism.id, {
				"saying": saying,
				"left": left,
				"right"	: right
			})

			assert updatedIsm.saying == saying
			assert updatedIsm.left == left
			assert updatedIsm.right == right

			assert updatedIsm.saying != oldSaying

	def test_delete(self):
		with self.ctx:
			ism = ismService.select().first()
			ismService.delete(ism.id)
			deletedIsm = ismService.selectById(ism.id)
			assert deletedIsm == None

	def test_serialize(self):
		string = '[{"saying": "No, I am your father.", "right": 11, "id": 5, "left": 38}]'

		with self.ctx:

			ism = ismService.new()
			ism.id = 5
			ism.right = 11
			ism.left = 38
			ism.saying = "No, I am your father."

			assert ismService.serialize([ism]) == string
