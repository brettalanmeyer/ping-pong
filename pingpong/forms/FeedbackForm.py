from pingpong.forms.Form import Form

class FeedbackForm(Form):

	def fields(self):
		return [{
			"name": "name",
			"label": "Name",
			"required": True,
			"type": "string"
		}, {
			"name": "email",
			"label": "Email",
			"required": False,
			"type": "string"
		}, {
			"name": "message",
			"label": "Feedback",
			"required": True,
			"type": "string"
		}]

	def validate(self, form):
		Form.validate(self, form)

		self.flash()

		return self.hasErrors
