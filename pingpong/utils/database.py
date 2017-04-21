from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import ConfigParser
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser.ConfigParser()
config.read("{}/../dbconfig.cfg".format(path))

username = config.get("db", "mysql_username")
password = config.get("db", "mysql_password")
host = config.get("db", "mysql_host")
database = config.get("db", "mysql_database")

pool_recycle = int(config.get("db", "pool_recycle"))
autocommit = config.get("db", "autocommit") == "True"
autoflush = config.get("db", "autoflush") == "True"

url = "mysql+mysqldb://{}:{}@{}/{}?use_unicode=1&charset=utf8".format(username, password, host, database)

engine = create_engine(url, pool_recycle = pool_recycle)
session = scoped_session(sessionmaker(autocommit = autocommit, autoflush = autoflush, bind = engine))

Base = declarative_base()