import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pingpong.app import app
from pingpong.services.OfficeService import OfficeService
from pingpong.utils.database import database as db
import flask
import re
import unittest

officeService = OfficeService()

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
		app.config["ADMIN_PASSWORD"] = "d63dc919e201d7bc4c825630d2cf25fdc93d4b2f0d46706d29038d01"

		app.config["TEST_CONFIG"] = ""

		self.ctx = app.app_context()
		self.app = app.test_client()
		self.request = app.test_request_context("http://localhost")

	def tearDown(self):
		pass

	def createOffice(self):
		return officeService.create({
			"city": "Des Moines",
			"state": "Iowa",
			"skypeChatId": "123abc",
			"seasonYear": "2017",
			"seasonMonth": "1"
		})

	def office(self, primary = False):
		office = None

		with self.app:
			with self.app.session_transaction() as sess:
				if primary:
					office = officeService.selectById(1)

				if office == None:
					offices = officeService.selectActive()

					if offices.count() > 0:
						for item in offices:
							if item.id != 1:
								office = item
								break
					else:
						office = self.createOffice()

				data = {
					"id": office.id,
					"city": office.city,
					"state": office.state,
					"key": office.key
				}

				sess["office"] = data
				return data

	def authenticate(self):
		return self.app.post("/login", data = {
			"username": self.username,
			"password": self.password
		}, follow_redirects = True)

	def redirects(self, rv, url):
		path = rv.location.replace("http://localhost", "")
		match = re.search(url, path)

		group = None
		if len(match.groups()) >= 1:
			group = match.group(1)

		return bool(match), group