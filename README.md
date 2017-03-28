# Ping Pong

## Installation

Install dependencies by running `sudo pip install -r requirements.txt`

## Game Types
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
		1. Select score to: (default is 9)
		2. Show table with player selector at each corner

## Configuration

	create config.cfg

		DEBUG = False
		ASSETS_DEBUG = False
		HOST = '0.0.0.0'
		PORT = 5000
		SECRET_KEY = ''
		MYSQL_USERNAME = ''
		MYSQL_PASSWORD = ''
		MYSQL_HOST = ''
		MYSQL_DATABASE = ''
		LOG_FILE_APPLICATION = 'logs/app.log'
		LOG_FILE_ACCESS = 'logs/access.log'
		LOG_FORMAT = '%(asctime)s %(levelname)s %(process)d %(message)s %(pathname)s:%(lineno)d:%(funcName)s()'
		LOG_WHEN = 'midnight'
		LOG_INTERVAL = 1
		LOG_BACKUP_COUNT = 14


## Raspberry pi

* run script `/home/pi/ping-pong/ping-pong-controls.py`


TODO

Create player from player selection page
animate scoring so you know your button has been pressed

Delegate Python Process
		screen python run.py
		Ctrl-a then d
	List Screen Processes
		screen -ls
	Kill Screen Process
		screen -X -S PID quit
