import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pingpong.app import app
from pingpong.utils.database import database as db
import unittest

class BaseTest(unittest.TestCase):

	ok = "200 OK"
	found = "302 FOUND"
	badRequest = "400 BAD REQUEST"
	unauthorized = "401 UNAUTHORIZED"
	notFound = "404 NOT FOUND"
	internalServerError = "500 INTERNAL SERVER ERROR"

	username = "admin"
	password = "password"

	def setUp(self):
		app.config["TESTING"] = True
		app.config["DEBUG"] = False

		app.config["ADMIN_USERNAME"] = "admin"
		app.config["ADMIN_PASSWORD"] = "d63dc919e201d7bc4c825630d2cf25fdc93d4b2f0d46706d29038d01" # password

		self.ctx = app.app_context()
		self.app = app.test_client()
		pass

	def tearDown(self):
		pass

	def authenticate(self):
		return self.app.post("/login", data = {
			"username": self.username,
			"password": self.password
		}, follow_redirects = True)
