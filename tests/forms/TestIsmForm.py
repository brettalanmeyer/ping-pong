from BaseTest import BaseTest
from pingpong.forms.IsmForm import IsmForm
from pingpong.services.IsmService import IsmService

ismForm = IsmForm()
ismService = IsmService()

class TestIsmForm(BaseTest):

	def test_null(self):
		with self.request:
			form = {}
			hasErrors = ismForm.validate(form)
			errors = ismForm.getErrors()

			assert hasErrors
			assert len(errors) == 3
			for error in errors:
				assert error["flashed"]

	def test_empty(self):
		with self.request:
			form = {
				"left": "",
				"right": "",
				"saying": ""
			}
			hasErrors = ismForm.validate(form)
			errors = ismForm.getErrors()

			assert hasErrors
			assert len(errors) == 3
			for error in errors:
				assert error["flashed"]

	def test_invalid(self):
		with self.request:
			form = {
				"left": "three",
				"right": "four",
				"saying": "Hello There"
			}
			hasErrors = ismForm.validate(form)
			errors = ismForm.getErrors()

			assert hasErrors
			assert len(errors) == 2

	def test_valid(self):
		with self.request:
			form = {
				"left": "3",
				"right": "4",
				"saying": "Hello There"
			}
			hasErrors = ismForm.validate(form)
			errors = ismForm.getErrors()

			assert not hasErrors
			assert len(errors) == 0

	def test_minmax(self):
		with self.request:
			form = {
				"left": "-1",
				"right": "51",
				"saying": "Some Saying"
			}
			hasErrors = ismForm.validate(form)
			errors = ismForm.getErrors()

			assert hasErrors
			assert len(errors) == 2

	def test_load(self):
		with self.request:
			data = {
				"left": "8",
				"right": "9",
				"saying": "Howdy"
			}
			ism = ismService.new()
			ismForm.load(ism, data)
			assert ism.left == data["left"]
			assert ism.right == data["right"]
			assert ism.saying == data["saying"]
