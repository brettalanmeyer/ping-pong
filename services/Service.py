from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class Service():

	def __init__(self, model):
		self.session = self.makeDatabaseConnection()
		self.model = model

	def makeDatabaseConnection(self):
		MYSQL_USERNAME = ''
		MYSQL_PASSWORD = ''
		MYSQL_HOST = ''
		MYSQL_DATABASE = ''

		engine = create_engine("mysql+mysqldb://" + MYSQL_USERNAME + ":" + MYSQL_PASSWORD + "@" + MYSQL_HOST + "/" + MYSQL_DATABASE, pool_recycle = 3600)
		db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
		Session = sessionmaker(bind = engine)

		return Session()

	def close(self):
		self.session.close()
