from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def setupSession(app):
	engine = create_engine("mysql+mysqldb://" + app.config["MYSQL_USERNAME"] + ":" + app.config["MYSQL_PASSWORD"] + "@" + app.config["MYSQL_HOST"] + "/" + app.config["MYSQL_DATABASE"], pool_recycle = 3600)
	db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
	Session = sessionmaker(bind = engine)
	return Session()
