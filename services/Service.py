from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import ConfigParser

class Service():

	def __init__(self, session):
		self.session = session
		self.matchTypes = ["singles", "doubles", "nines"]
