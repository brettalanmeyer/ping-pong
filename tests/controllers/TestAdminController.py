from BaseTest import BaseTest
from flask_login import login_user
from flask_login import login_user
from pingpong.models.AdminModel import AdminModel

class TestAdminController(BaseTest):

	def test_admin_unauthenticated(self):
		rv = self.app.get("/admin")
		assert rv.status == self.found

	def test_admin_authenticated(self):
		self.authenticate()
		rv = self.app.get("/admin")
		assert rv.status == self.ok

	def test_admin_unauthenticated(self):
		rv = self.app.get("/admin")
		assert rv.status == self.found

	def test_admin_copy_remote_data(self):
		rv = self.app.post("/admin/copy-remote-data")
		assert rv.status == self.found

	def test_admin_delete_all(self):
		rv = self.app.post("/admin/delete-all")
		assert rv.status == self.found

	def test_admin_matches_delete_all(self):
		rv = self.app.post("/admin/matches/delete-all")
		assert rv.status == self.found

	def test_admin_players_delete_all(self):
		rv = self.app.post("/admin/players/delete-all")
		assert rv.status == self.found
