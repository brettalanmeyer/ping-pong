from pingpong.forms.Form import Form

class OfficeForm(Form):

	def fields(self):
		return [{
			"name": "city",
			"label": "City",
			"required": True,
			"type": "string"
		}, {
			"name": "state",
			"label": "State",
			"required": True,
			"type": "string"
		}, {
			"name": "skypeChatId",
			"label": "Skype Chat ID",
			"required": False,
			"type": "string"
		}]

	def load(self, office, form):
		if "city" in form:
			office.city = form["city"]
		if "state" in form:
			office.state = form["state"]
		if "skypeChatId" in form:
			office.skypeChatId = form["skypeChatId"]