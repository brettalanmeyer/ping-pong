from pingpong.forms.Form import Form

class IsmForm(Form):

	def fields(self):
		return [{
			"name": "left",
			"label": "Left",
			"required": True,
			"type": "int",
			"max": 50,
			"min": 0
		}, {
			"name": "right",
			"label": "Right",
			"required": True,
			"type": "int",
			"max": 50,
			"min": 0
		}, {
			"name": "saying",
			"label": "Saying",
			"required": True,
			"type": "string"
		}]

	def load(self, ism, form):
		if "left" in form:
			ism.left = form["left"]
		if "right" in form:
			ism.right = form["right"]
		if "saying" in form:
			ism.saying = form["saying"]