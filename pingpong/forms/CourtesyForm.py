from pingpong.forms.Form import Form

class CourtesyForm(Form):

	def fields(self):
		return [{
			"name": "text",
			"label": "Text",
			"required": True,
			"type": "string"
		}]

	def load(self, ism, form):
		if "saying" in form:
			ism.saying = form["saying"]