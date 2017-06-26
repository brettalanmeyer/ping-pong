from pingpong.forms.Form import Form

class MatchForm(Form):

	def validateNew(self, form):
		Form.validate(self, form)

		if "matchType" not in form:
			self.addError({
				"name": "matchType",
				"label": "Match Type"
			}, "Please select a valid match type.")

		if not self.hasErrors:
			if form["matchType"] not in ["singles", "doubles", "nines"]:
				self.addError({
					"name": "matchType",
					"label": "Match Type"
				}, "Please select a valid match type.")

		return self.hasErrors

	def validatePlayTo(self, form):
		Form.validate(self, form)

		if "playTo" not in form:
			self.addError({
				"name": "playTo",
				"label": "Points"
			}, "Please select valid number of points.")

		if not self.hasErrors:
			if form["playTo"] not in ["11", "21"]:
				self.addError({
					"name": "playTo",
					"label": "Points"
				}, "Please select valid number of points.")

		return self.hasErrors

	def validateGames(self, form):
		Form.validate(self, form)

		if "numOfGames" not in form:
			self.addError({
				"name": "numOfGames",
				"label": "Sets"
			}, "Please select a valid number of sets.")

		if not self.hasErrors:
			if form["numOfGames"] not in ["1", "3", "5", "7"]:
				self.addError({
					"name": "numOfGames",
					"label": "Sets"
				}, "Please select a valid number of sets.")

		return self.hasErrors
