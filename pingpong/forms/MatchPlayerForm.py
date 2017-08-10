from pingpong.forms.Form import Form

class MatchPlayerForm(Form):

	def validate(self, matchType, form):
		Form.validate(self, form)

		ids = form.getlist("playerId")

		if matchType == None or ids == None:
			self.addError({
				"name": "playerId",
				"label": "Player"
			}, "Players are required.")

		elif matchType.isSingles():
			if len(ids) != 2:
				self.addError({
				"name": "playerId",
				"label": "Player"
			}, "Please select 2 players.")

		elif matchType.isDoubles() or matchType.isNines():
			if len(ids) != 4:
				self.addError({
				"name": "playerId",
				"label": "Player"
			}, "Please select 4 players.")

		else:
			self.addError({
				"name": "playerId",
				"label": "Player"
			}, "Players are required.")

		return self.hasErrors
