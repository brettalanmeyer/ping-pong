from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import ConfigParser

class Service():

	def __init__(self, model):
		self.configuration()
		self.session = self.makeDatabaseConnection()
		self.model = model

	def configuration(self):
		config = ConfigParser.ConfigParser()
		config.read("db-config.cfg")

		self.mysql_username = config.get("default", "MYSQL_USERNAME")
		self.mysql_password = config.get("default", "MYSQL_PASSWORD")
		self.mysql_host = config.get("default", "MYSQL_HOST")
		self.mysql_database = config.get("default", "MYSQL_DATABASE")

	def makeDatabaseConnection(self):
		engine = create_engine("mysql+mysqldb://" + self.mysql_username + ":" + self.mysql_password + "@" + self.mysql_host + "/" + self.mysql_database, pool_recycle = 3600)
		db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
		Session = sessionmaker(bind = engine)

		return Session()

	def close(self):
		self.session.close()
