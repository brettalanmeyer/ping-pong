from pingpong.forms.Form import Form

class MatchEntryForm(Form):

	def fields(self):
		return [{
			"name": "matchType",
			"label": "Match Type",
			"required": True,
			"type": "string"
		}, {
			"name": "numOfGames",
			"label": "Best Of",
			"required": True,
			"type": "string"
		}, {
			"name": "playerId",
			"label": "Players",
			"required": True,
			"type": "string"
		}, {
			"name": "set",
			"label": "Sets",
			"required": True,
			"type": "string"
		}]

	def validate(self, form):
		Form.validate(self, form)

		if not self.hasErrors:

			sets = form.getlist("set")
			if len(sets) != int(form["numOfGames"]) * 2:
				self.hasErrors = True
				self.errors.append(self.error({
					"name": "set",
					"label": "Sets"
				}, "Not enough sets"))

			playerIds = form.getlist("playerId")
			if form["matchType"] == "singles" and len(playerIds) != 2:
				self.hasErrors = True
				self.errors.append(self.error({
					"name": "playerId",
					"label": "Players"
				}, "2 players must be selected"))

			if form["matchType"] != "singles" and len(playerIds) != 4:
				self.hasErrors = True
				self.errors.append(self.error({
					"name": "playerId",
					"label": "Players"
				}, "4 players must be selected"))

			self.flash()

		return self.hasErrors

	def foundNameError(self, players, form):
		if players.count() > 0:
			message = "The name '{}' is already taken. Please specify a unique name.".format(form["name"])
			self.hasErrors = True
			self.errors.append(self.error({
				"name": "name",
				"label": "Name"
			}, message))
