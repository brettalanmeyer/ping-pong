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
		}, {
			"name": "seasonYear",
			"label": "Season Starting Year",
			"required": True,
			"type": "int"
		}, {
			"name": "seasonMonth",
			"label": "Season Starting Month",
			"required": True,
			"type": "int"
		}]

	def load(self, office, form):
		if "city" in form:
			office.city = form["city"]
		if "state" in form:
			office.state = form["state"]
		if "seasonYear" in form:
			office.seasonYear = form["seasonYear"]
		if "seasonMonth" in form:
			office.seasonMonth = form["seasonMonth"]
		if "skypeChatId" in form:
			office.skypeChatId = form["skypeChatId"]