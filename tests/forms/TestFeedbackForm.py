from BaseTest import BaseTest
from pingpong.forms.FeedbackForm import FeedbackForm

feedbackForm = FeedbackForm()

class TestFeedbackForm(BaseTest):

	def test_null(self):
		with self.request:
			form = {}
			hasErrors = feedbackForm.validate(form)
			errors = feedbackForm.getErrors()

			assert hasErrors
			assert len(errors) == 2
			for error in errors:
				assert error["flashed"]

	def test_empty(self):
		with self.request:
			form = {
				"name": "",
				"email": "",
				"message": ""
			}
			hasErrors = feedbackForm.validate(form)
			errors = feedbackForm.getErrors()

			assert hasErrors
			assert len(errors) == 2
			for error in errors:
				assert error["flashed"]

	def test_valid(self):
		with self.request:
			form = {
				"name": "Johnny",
				"email": "Johnny@Johnny.com	",
				"message": "Oh Johnny"
			}
			hasErrors = feedbackForm.validate(form)
			errors = feedbackForm.getErrors()

			assert not hasErrors
			assert len(errors) == 0
