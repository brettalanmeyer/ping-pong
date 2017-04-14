from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("dbconfig.cfg")

username = config.get("db", "mysql_username")
password = config.get("db", "mysql_password")
host = config.get("db", "mysql_host")
database = config.get("db", "mysql_database")

pool_recycle = int(config.get("db", "pool_recycle"))
autocommit = config.get("db", "autocommit") == "True"
autoflush = config.get("db", "autoflush") == "True"

url = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, host, database)

engine = create_engine(url, pool_recycle = pool_recycle)
session = scoped_session(sessionmaker(autocommit = autocommit, autoflush = autoflush, bind = engine))
