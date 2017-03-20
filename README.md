# Ping Pong

# Installation

Install dependencies

run `sudo pip install -r requirements.txt`

# Game Types
	Singles
	Doubles
	9's

	Singles
		1. Select number of games (Best of 1, 3, or 5)
		2. Select score to: (default is 21, must win by 2 pts)
		3. Show table with player selector at each end

	Doubles
		1. Select number of games (Best of 1, 3, or 5)
		2. Select score to: (default is 21, must win by 2 pts)
		3. Show table with player selector at each corner

	9's

# Configuration

	create config.cfg

		DEBUG = True
		HOST = '0.0.0.0'
		PORT = 5000
		SECRET_KEY = ''
		MYSQL_USERNAME = ''
		MYSQL_PASSWORD = ''
		MYSQL_HOST = ''
		MYSQL_DATABASE = ''


	Windows
		Download get-pip.py
		python get-pip.py
		pip install Flask
		pip install Flask-Assets
		pip install flask-socketio
		pip install SQLAlchemy
		pip install mysqlclient==1.3.4
		pip install jsmin
		pip install cssmin
		pip install gevent-websocket


/home/pi/ping-pong

