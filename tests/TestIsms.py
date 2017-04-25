from BaseTest import BaseTest
from pingpong.services.IsmService import IsmService

ismService = IsmService()

class TestIsms(BaseTest):

	def test_isms(self):
		rv = self.app.get("/isms")
		assert rv.status == self.ok

	def test_isms_new(self):
		rv = self.app.get("/isms/new")
		assert rv.status == self.ok

	def test_isms_create(self):
		rv = self.app.post("/isms", data = {
			"saying": "A New Saying",
			"left": 9,
			"right": 11
		}, follow_redirects = True)
		assert rv.status == self.ok

	def test_isms_create_empty(self):
		rv = self.app.post("/isms", data = {
			"saying": "",
			"left": "",
			"right": ""
		})
		assert rv.status == self.badRequest

	def test_isms_create_null(self):
		rv = self.app.post("/isms", data = {})
		assert rv.status == self.badRequest

	def test_isms_edit(self):
		with self.ctx:
			ism = ismService.select().first()

			rv = self.app.get("/isms/{}/edit".format(ism.id))
			assert rv.status == self.ok

	def test_isms_update(self):
		newSaying = "Another Saying"
		newLeft = 4
		newRight = 342

		with self.ctx:
			ism = ismService.select().first()
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

	def test_isms_update_empty(self):
		with self.ctx:
			ism = ismService.select().first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {
				"saying": "",
				"left": "",
				"right": ""
			}, follow_redirects = True)
			assert rv.status == self.badRequest

	def test_isms_update_null(self):
		with self.ctx:
			ism = ismService.select().first()
			rv = self.app.post("/isms/{}".format(ism.id), data = {}, follow_redirects = True)
			assert rv.status == self.badRequest

