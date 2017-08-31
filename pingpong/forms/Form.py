from flask import flash

class Form():

	def __init__(self):
		self.errors = []
		self.hasErrors = False

	def fields(self):
		return []

	def validate(self, form):
		self.errors = []
		self.hasErrors = False

		fields = self.fields()

		for field in fields:

			if self.validateRequired(field, form):

				if self.validateInt(field, form):
					self.validateMin(field, form)
					self.validateMax(field, form)

				self.validateMaxlength(field, form)

		self.flash()

		return self.hasErrors

	def flash(self):
		for error in self.errors:
			if not error["flashed"]:
				flash(error["message"], "danger")
				error["flashed"] = True

	def validateRequired(self, field, form):
		if field["required"]:

			if field["name"] not in form:
				message = "'{}' is a required field.".format(field["label"])
				self.hasErrors = True
				self.errors.append(self.error(field, message))
				return False

			elif len(form[field["name"]].strip()) == 0:
				message = "'{}' is a required field.".format(field["label"])
				self.hasErrors = True
				self.errors.append(self.error(field, message))
				return False

		return True

	def validateInt(self, field, form):
		if field["type"] == "int":

			try:
				int(form[field["name"]])
			except:
				message = "'{}' must be an integer.".format(field["label"])
				self.hasErrors = True
				self.errors.append(self.error(field, message))
				return False

		return True

	def validateMin(self, field, form):
		if "min" in field:
			value = float(form[field["name"]])

			if value < field["min"]:
				message = "'{}' must be a value greater than or equal to {}.".format(field["label"], field["min"])
				self.hasErrors = True
				self.errors.append(self.error(field, message))
				return False

		return True

	def validateMax(self, field, form):
		if "max" in field:
			value = float(form[field["name"]])

			if value > field["max"]:
				message = "'{}' must be a value less than or equal to {}.".format(field["label"], field["max"])
				self.hasErrors = True
				self.errors.append(self.error(field, message))
				return False

		return True

	def validateMaxlength(self, field, form):
		if "maxlength" in field:
			value = form[field["name"]]

			if len(value) > field["maxlength"]:
				message = "'{}' cannot be longer than {} characters.".format(field["label"], field["maxlength"])
				self.hasErrors = True
				self.errors.append(self.error(field, message))
				return False

		return True

	def addError(self, field, message):
		self.hasErrors = True
		self.errors.append(self.error(field, message))
		self.flash()

	def error(self, field, message):
		return {
			"name": field["name"],
			"label": field["label"],
			"message": message,
			"flashed": False
		}

	def getErrors(self):
		return self.errors