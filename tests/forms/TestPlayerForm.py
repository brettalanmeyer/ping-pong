from BaseTest import BaseTest
from pingpong.forms.PlayerForm import PlayerForm
from pingpong.services.PlayerService import PlayerService

playerForm = PlayerForm()
playerService = PlayerService()

class TestPlayerForm(BaseTest):

	def test_null(self):
		with self.request:
			office = self.office()
			form = {}
			hasErrors = playerForm.validate(None, office["id"], form)
			errors = playerForm.getErrors()

			assert hasErrors
			assert len(errors) == 1
			for error in errors:
				assert error["flashed"]

	def test_empty(self):
		with self.request:
			office = self.office()
			form = {
				"name": ""
			}
			hasErrors = playerForm.validate(None, office["id"], form)
			errors = playerForm.getErrors()

			assert hasErrors
			assert len(errors) == 1
			for error in errors:
				assert error["flashed"]

	def test_valid(self):
		with self.request:
			office = self.office()
			form = {
				"name": "Tim"
			}
			hasErrors = playerForm.validate(None, office["id"], form)
			errors = playerForm.getErrors()

			assert not hasErrors
			assert len(errors) == 0

	def test_load(self):
		with self.request:
			data = {
				"name": "Sparticus"
			}
			player = playerService.new()
			playerForm.load(player, data)
			assert player.name == data["name"]
