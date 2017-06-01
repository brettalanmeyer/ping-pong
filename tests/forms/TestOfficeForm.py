from BaseTest import BaseTest
from pingpong.forms.Form import Form
from pingpong.forms.OfficeForm import OfficeForm
from pingpong.services.OfficeService import OfficeService

officeForm = OfficeForm()
officeService = OfficeService()

class TestOfficeForm(BaseTest):

	def test_base(self):
		form = Form()
		fields = form.fields()
		hasErrors = form.validate({})

		assert len(fields) == 0
		assert not hasErrors

	def test_null(self):
		with self.request:
			form = {}
			hasErrors = officeForm.validate(form)
			errors = officeForm.getErrors()

			assert hasErrors
			assert len(errors) == 4
			for error in errors:
				assert error["flashed"]

	def test_empty(self):
		with self.request:
			form = {
				"city": "",
				"state": "",
				"skypeChatId": "",
				"seasonYear": "",
				"seasonMonth": ""
			}
			hasErrors = officeForm.validate(form)
			errors = officeForm.getErrors()

			assert hasErrors
			assert len(errors) == 4
			for error in errors:
				assert error["flashed"]

	def test_valid(self):
		with self.request:
			form = {
				"city": "Springfield",
				"state": "Yes",
				"skypeChatId": "",
				"seasonYear": "2015",
				"seasonMonth": "4"
			}
			hasErrors = officeForm.validate(form)
			errors = officeForm.getErrors()

			assert not hasErrors
			assert len(errors) == 0

	def test_load(self):
		with self.request:
			data = {
				"city": "Springfield",
				"state": "Yes",
				"skypeChatId": "123abc",
				"seasonYear": 2011,
				"seasonMonth": 3
			}
			office = officeService.new()
			officeForm.load(office, data)
			assert office.city == data["city"]
			assert office.state == data["state"]
			assert office.skypeChatId == data["skypeChatId"]
			assert office.seasonYear == data["seasonYear"]
			assert office.seasonMonth == data["seasonMonth"]
