import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pingpong.app import app
from pingpong.utils.database import database as db
import unittest

class BaseTest(unittest.TestCase):

	ok = "200 OK"
	badRequest = "400 BAD REQUEST"
	notFound = "404 NOT FOUND"

	def setUp(self):
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		self.ctx = app.app_context()
		self.app = app.test_client()
		pass

	def tearDown(self):
		pass
