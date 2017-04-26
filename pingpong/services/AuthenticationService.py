from flask import current_app as app
from flask import request
from flask_login import UserMixin
import hashlib

class AuthenticationService():

	def authenticate(self, form):
		app.logger.info("Authenticating Administrator")

		if "username" not in form:
			app.logger.info("Username field does not exist")
			return False

		if "password" not in form:
			app.logger.info("Password field does not exist")
			return False

		username = form["username"]
		password = form["password"]

		passwordHash = hashlib.sha224(password).hexdigest()

		if passwordHash != app.config["ADMIN_PASSWORD"]:
			app.logger.info("Invalid Password")
			return False

		if username != app.config["ADMIN_USERNAME"]:
			app.logger.info("Invalid Username")
			return False

		return True

	def admin(self):
		return Admin()

class Admin(UserMixin):

	def __init__(self):
		self.id = 0
		self.name = "BemAdmin"
		self.password = self.name + "_secret"

	def __repr__(self):
		return "%d/%s/%s" % (self.id, self.name, self.password)
