from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import ConfigParser

class Service():

	def __init__(self, session, model):
		self.session = session
		self.model = model
		self.matchTypes = ["singles", "doubles", "nines"]
