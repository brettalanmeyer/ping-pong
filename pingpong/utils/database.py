from pingpong.app import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

with app.app_context():
	username = app.config["DB_USERNAME"]
	password = app.config["DB_PASSWORD"]
	host = app.config["DB_HOST"]
	database = app.config["DB_DATABASE"]
	pool_recycle = app.config["DB_POOL_RECYCLE"]
	autocommit = app.config["DB_AUTOCOMMIT"]
	autoflush = app.config["DB_AUTOFLUSH"]

url = "mysql+mysqldb://{}:{}@{}/{}?use_unicode=1&charset=utf8".format(username, password, host, database)
engine = create_engine(url, pool_recycle = pool_recycle)
session = scoped_session(sessionmaker(autocommit = autocommit, autoflush = autoflush, bind = engine))

Base = declarative_base()
