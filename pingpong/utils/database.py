from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("mysql+mysqldb://brett:r45ftthry@localhost/ping-pong", pool_recycle = 3600)
session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
