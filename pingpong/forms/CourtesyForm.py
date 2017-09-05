from pingpong.forms.Form import Form

class CourtesyForm(Form):

	def fields(self):
		return [{
			"name": "text",
			"label": "Text",
			"required": True,
			"type": "string",
			"maxlength": 255
		}, {
			"name": "language",
			"label": "Language",
			"required": True,
			"type": "string",
			"maxlength": 255
		}, {
			"name": "slow",
			"label": "Make Speech Slow",
			"required": True,
			"type": "int",
			"min": 0,
			"max": 1
		}]

	def load(self, ism, form):
		if "saying" in form:
			ism.saying = form["saying"]
